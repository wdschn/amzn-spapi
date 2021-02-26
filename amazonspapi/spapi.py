import hmac
import hashlib
import datetime

import boto3
from requests import request
from django.core.cache import cache
from . import settings  as spapi_settings
from .response import SPRespone
from .utils import (
    dict_to_url_params,
    dict_to_request_data_str
)


class SPAPI():
    authorization_header_template = 'AWS4-HMAC-SHA256 Credential={access_key_id}/{credential_scope}, SignedHeaders={credential_sign_headers}, Signature={sign}'

    domain = 'https://sellingpartnerapi-na.amazon.com'

    aws_app_client_id = ''
    aws_app_client_secret = ''
    aws_iam_user_key_id = ''
    aws_iam_user_access_key = ''
    aws_iam_role_arn = ''
    region_name = 'us-east-1'
    service_name = 'execute-api'

    def __init__(self,
                 aws_app_client_id,
                 aws_app_client_secret,
                 aws_iam_user_key_id,
                 aws_iam_user_access_key,
                 aws_iam_role_arn,
                 refresh_token,
                 region_name='us-east-1',
                 service_name='execute-api'):
        """

        :param aws_app_client_id:
        :param aws_app_client_secret:
        :param aws_iam_user_key_id:
        :param aws_iam_user_access_key:
        :param aws_iam_role_arn:
        :param refresh_token:
        :param region_name:
        :param service_name:
        """

        self.aws_app_client_id = aws_app_client_id
        self.aws_app_client_secret = aws_app_client_secret
        self.aws_iam_user_key_id = aws_iam_user_key_id
        self.aws_iam_user_access_key = aws_iam_user_access_key
        self.aws_iam_role_arn = aws_iam_role_arn
        self.refresh_token = refresh_token
        self.region_name = region_name
        self.service_name = service_name

    def sign(self, key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    def get_aws_sts_token(self, ):
        aws_sts = cache.get('aws_sts')
        if aws_sts is None:
            client = boto3.client('sts', aws_access_key_id=self.aws_iam_user_key_id, aws_secret_access_key=self.aws_iam_user_access_key)
            response = client.assume_role(RoleArn=self.aws_iam_role_arn, RoleSessionName='weyspapi', )
            if response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
                aws_sts = response.get('Credentials')
            cache.set('aws_sts', aws_sts, 60 * 59)
        return aws_sts

    def get_token(self):
        k = 'accessToken_' + hashlib.md5(self.refresh_token.encode()).hexdigest()
        token = cache.get(k)
        if token is None:
            url = spapi_settings.api_url.get('token')
            data = {
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token,
                'client_id': self.aws_app_client_id,
                'client_secret': self.aws_app_client_secret,
            }
            resp = request('POST', url=url, data=data)  # requests.post(url=url, data=data)
            resp_dict = resp.json()
            token = resp_dict.get('access_token')
            cache.set(k, token, resp_dict.get('expires_in') - 20)
        return token

    def get_canonical_request(self, http_method, headers, uri, params, data):
        canonical_headers = ''
        for he in sorted(headers.keys()):
            canonical_headers += '%s:%s\n' % (he.lower(), headers[he])

        sign_headers = ';'.join([x.lower() for x in sorted(headers.keys())])
        requestPayload = hashlib.sha256(data.encode()).hexdigest()
        canonical_request = http_method + '\n' + uri + '\n' + params + '\n' + canonical_headers + '\n' + sign_headers + '\n' + requestPayload
        return hashlib.sha256(canonical_request.encode()).hexdigest(), sign_headers

    def get_default_headers(self, datetime_str):
        return {
            'host': self.domain.replace('https://', ''),
            'x-amz-access-token': self.get_token(),
            'x-amz-date': datetime_str,
            'user-agent': 'Wey/v1.0 (Language=python/3.8.5; Host=king.weylei.com)',
        }

    def get_signature_key(self, key, dateStamp):
        kDate = self.sign(("AWS4" + key).encode("utf-8"), dateStamp)
        kRegion = self.sign(kDate, self.region_name)
        kService = self.sign(kRegion, self.service_name)
        kSigning = self.sign(kService, "aws4_request")
        return kSigning

    def get_sign(self, sign_key, string_to_sign):
        return hmac.new(sign_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

    def make_request(self, uri='/', params=None, data=None, method='GET'):
        # params = dict_to_url_params(params)
        params = dict_to_url_params(params)
        data = dict_to_request_data_str(data)

        dt = datetime.datetime.utcnow()
        dtf = dt.strftime('%Y%m%dT%H%M%SZ')
        dtod = dt.strftime('%Y%m%d')
        # 凭证范围
        credential_scope = dtod + '/' + self.region_name + '/' + self.service_name + '/aws4_request'

        headers = self.get_default_headers(dtf)
        canonical_request_hash, credential_sign_headers = self.get_canonical_request(http_method=method, headers=headers, uri=uri, params=params, data=data)

        ams_sts_token = self.get_aws_sts_token()
        string_to_sign = 'AWS4-HMAC-SHA256' + '\n' + dtf + '\n' + credential_scope + '\n' + canonical_request_hash
        sign_key = self.get_signature_key(ams_sts_token.get('SecretAccessKey'), dtod)
        sign = self.get_sign(sign_key, string_to_sign)

        authorization_header = self.authorization_header_template.format(
            access_key_id=ams_sts_token.get('AccessKeyId'),
            credential_scope=credential_scope,
            credential_sign_headers=credential_sign_headers,
            sign=sign
        )

        headers['Authorization'] = authorization_header
        headers['x-amz-security-token'] = ams_sts_token.get('SessionToken')

        full_url = self.domain + (uri if params == '' else (uri + '?' + params))

        resp = request(method, url=full_url, data=data, headers=headers)

        return SPRespone(resp)

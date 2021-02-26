import requests
from .spapi import SPAPI
from .utils import ase_cbc_decryptor, gzip_uncompress


class ReportUtils(SPAPI):

    def get_reports(self,
                    report_types=None,
                    processing_statuss=None,
                    marketplace_ids=None,
                    page_size=None,
                    created_since=None,
                    created_until=None,
                    next_token=None
                    ):
        uri = '/reports/2020-09-04/reports'
        params = {
            'reportTypes': report_types,
            'processingStatuss': processing_statuss,
            'marketplaceIds': marketplace_ids,
            'pageSize': page_size,
            'createdSince': created_since,
            'createdUntil': created_until,
        }
        if next_token:
            params = {
                'nextToken': next_token,
            }

        return self.make_request(params=params, uri=uri, method='GET')

    def create_report(self, report_type=None, data_start_time=None, data_end_time=None, marketplace_ids=None, report_options=None):
        uri = '/reports/2020-09-04/reports'
        data = {
            'reportOptions': report_options,
            'reportType': report_type,
            'dataStartTime': data_start_time,
            'dataEndTime': data_end_time,
            'marketplaceIds': marketplace_ids,
        }
        return self.make_request(data=data, uri=uri, method='POST')

    def get_report(self, report_id):
        uri = '/reports/2020-09-04/reports/{reportId}'.format(reportId=report_id)
        return self.make_request(uri=uri, method='GET')

    def get_report_documents(self, report_document_id):
        uri = '/reports/2020-09-04/documents/{reportDocumentId}'.format(reportDocumentId=report_document_id)
        return self.make_request(uri=uri, method='GET')

    def cancle_report(self, report_id):
        uri = '/reports/2020-09-04/reports/{reportId}'.format(reportId=report_id)
        return self.make_request(uri=uri, method='DELETE')

    def _decrypt_report_content(self, key, iv, encryption):
        return ase_cbc_decryptor(key=key, iv=iv, encryption=encryption)

    def get_report_document_content(self, key, iv, url, compression_type=None):
        resp = requests.get(url=url)
        resp_content = resp.content

        decrypted_content = self._decrypt_report_content(key=key, iv=iv, encryption=resp_content)

        if compression_type == 'GZIP':
            decrypted_content = gzip_uncompress(decrypted_content)

        # 处理编码
        code = 'utf-8'
        if 'cp1252' in resp.headers.get('Content-Type', '').lower():
            code = 'Cp1252'
        return decrypted_content.decode(code)

    def get_report_schedules(self, report_types):
        uri = '/reports/2020-09-04/schedules'
        if isinstance(report_types, str):
            report_types = [report_types, ]

        assert len(report_types) <= 10, 'The length of report_types should be less than 10'

        params = {
            'reportTypes': report_types
        }
        return self.make_request(uri=uri, params=params, method='GET')

    def create_report_schedule(self, report_type, marketplace_ids, report_options, period, next_report_creation_time):
        """
        :param report_type:
        :param marketplace_ids:
        :param report_options:
        :param period: https://github.com/amzn/selling-partner-api-docs/blob/main/references/reports-api/reports_2020-09-04.md#period
        :param next_report_creation_time:
        :return:
        """
        uri = '/reports/2020-09-04/schedules'
        data = {
            'reportType': report_type,
            'marketplaceIds': marketplace_ids,
            'reportOptions': report_options,
            'period': period,
            'nextReportCreationTime': next_report_creation_time
        }
        return self.make_request(uri=uri, data=data, method='POST')

    def get_report_schedule(self, report_schedule_id):
        uri = '/reports/2020-09-04/schedules/{reportScheduleId}'.format(reportScheduleId=report_schedule_id)
        return self.make_request(uri=uri, method='GET')

    def cancel_report_schedule(self, report_schedule_id):
        uri = '/reports/2020-09-04/schedules/{reportScheduleId}'.format(reportScheduleId=report_schedule_id)
        return self.make_request(uri=uri, method='DELETE')

import gzip
import base64
import json
import datetime
from urllib.parse import quote

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def remove_empty(dict_):
    """
    Returns dict_ with all empty values removed.
    """
    return {k: v for k, v in dict_.items() if v}


def processing_data(data):
    data = remove_empty(data)
    for key, value in data.items():
        if isinstance(value, (datetime.datetime, datetime.date)):
            # data[key] = value.replace(microsecond=0).isoformat()
            data[key] = value.isoformat()
    return data


def dict_to_url_params(data):
    if isinstance(data, dict):
        data = processing_data(data=data)
        ps = ''
        for k in sorted(data):
            value = ','.join(sorted(data[k])) if isinstance(data[k], list) else str(data[k])
            ps += '&{}={}'.format(k, quote(value, safe='-_.~'))
        return ps[1:]
    elif isinstance(data, str):
        return data
    else:
        return ''


def dict_to_request_data_str(data):
    if isinstance(data, dict):
        data = processing_data(data)
        return json.dumps(data, sort_keys=True)
    elif isinstance(data, str):
        return data
    else:
        return ''


def ase_cbc_decryptor(key, iv, encryption):
    """
    1、使用 aes 解密
    2、取消补位
    :param key:bytes aes key
    :param iv:bytes aes iv
    :param encryption:bytes crypted data
    :return: bytes decrypted data
    """
    cipher = Cipher(algorithms.AES(base64.b64decode(key)), modes.CBC(base64.b64decode(iv)))
    decryptor = cipher.decryptor()
    decrypted_text = decryptor.update(encryption)
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpaded_text = unpadder.update(decrypted_text)
    return unpaded_text + unpadder.finalize()


def gzip_uncompress(data):
    return gzip.decompress(data)

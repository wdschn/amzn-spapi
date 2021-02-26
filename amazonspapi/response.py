class SPRespone(object):
    def __init__(self, http_response):
        self.original = http_response
        self.status_code = http_response.status_code

    @property
    def data(self):
        if self.original.headers.get('Content-Type') == 'application/json':
            # return self.original.content.decode('utf8')
            try:
                return self.original.json()
            except Exception:
                return eval(self.original.content.decode('utf8'))
        return

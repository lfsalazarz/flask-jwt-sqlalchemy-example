from werkzeug.wrappers import Request, Response
from json import dumps


class MaxContentLength:
    def __init__(self, app, max_length):
        self.app = app
        self.max_length = max_length

    def __call__(self, environ, start_response):
        request = Request(environ)
        if request.content_length is not None and request.content_length > self.max_length:
            res = Response(dumps({"message": "Payload Too Large"}), content_type="application/json", status=413)
            return res(environ, start_response)
        return self.app(environ, start_response)

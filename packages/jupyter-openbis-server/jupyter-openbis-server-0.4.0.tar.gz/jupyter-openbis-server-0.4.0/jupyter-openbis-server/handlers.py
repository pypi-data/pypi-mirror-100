import tornado
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin, ExtensionHandlerJinjaMixin


class ConnectionHandler(
    ExtensionHandlerMixin,
    ExtensionHandlerJinjaMixin,
    JupyterHandler
):
    @tornado.web.authenticated
    def get(self):
        pass

    @tornado.web.authenticated
    def post(self):
        pass

    @tornado.web.authenticated
    def put(self):
        pass
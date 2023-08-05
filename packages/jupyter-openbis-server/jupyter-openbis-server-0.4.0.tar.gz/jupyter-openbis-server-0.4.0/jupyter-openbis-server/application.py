import os, jinja2
import jupyter_server
from traitlets import Unicode

from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.extension.handler import ExtensionHandlerMixin
import tornado
print("------------------------HELLO------------")

class OpenbisServerHandler(JupyterHandler):

    @tornado.web.authenticated
    def get(self):
        self.write({
            'status'       : 200,
            'connections'  : ['all your connections'],
            'notebook_dir' : ['your notebook dir']
        })
        return
    
    @tornado.web.authenticated
    def post(self):
        pass
        

def _load_jupyter_server_extension(serverapp: jupyter_server.serverapp.ServerApp):
    """
    This function is called when the extension is loaded.
    """
    handlers = [
        ('/openbis/hello', OpenbisServerHandler)
    ]

    serverapp.web_app.add_handlers('.*$', handlers)
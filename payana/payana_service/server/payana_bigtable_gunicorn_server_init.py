from subprocess import run

import multiprocessing

import gunicorn.app.base


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

def gunicorn_init_app(port, server, workers, payana_flask_app):
    
    options = {
        'bind': '%s:%s' % (server, port),
        'workers': workers,
        'timeout': 300,
    }
    gunicorn_payana = StandaloneApplication(payana_flask_app, options)
    return gunicorn_payana

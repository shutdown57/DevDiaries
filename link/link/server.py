import cherrypy
from flask_migrate import Migrate, upgrade

from factory import create_app
from common.extensions import db


app = create_app('product')
db.init_app(app)
migrate = Migrate(app, db)
upgrade()

if __name__ == '__main__':
    cherrypy.tree.graft(app, "/")
    cherrypy.server.unsubscribe()

    server = cherrypy._cpserver.Server()
    server.socket_host = "0.0.0.0"
    server.socket_port = 5000
    server.thread_pool = 30

    server.subscribe()

    cherrypy.engine.start()
    cherrypy.engine.block()

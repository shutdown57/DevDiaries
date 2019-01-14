from factory import create_app
from common.extensions import db

def setup():
    app = create_app('product')
    db.init_app(app)
    return app

application = setup()

if __name__ == '__main__':
    application.run()

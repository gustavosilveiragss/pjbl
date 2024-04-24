from models import db
from utils.create_db import create_db
from controllers.app_controller import create_app

if __name__ == '__main__':
    app = create_app()
    #create_db(app)
    app.run(host='127.0.0.1', port=5000)
from controllers.app_controller import create_app
from models.db import createDB
import utils.consts as consts

if __name__ == "__main__":
    socketio, app = create_app()
    # createDB(app)
    socketio.run(app=app, host=consts.ADDRESS, port=consts.PORT)
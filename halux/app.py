from controllers.app_controller import create_app
from models.db import createDB
import utils.consts as consts

if __name__ == "__main__":
    app = create_app()
    # createDB(app)
    app.run(host='127.0.0.1', port=consts.PORT)
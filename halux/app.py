from controllers.app_controller import create_app
import utils.consts as consts

if __name__ == '__main__':
    app = create_app()
    #create_db(app)
    app.run(host=consts.ADDRESS, port=consts.PORT)
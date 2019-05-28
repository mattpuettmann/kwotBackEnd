from flask import Flask, g, abort
from flask_login import LoginManager
import models
from flask_cors import CORS
from resources.quotes import quotes_api
from resources.users import users_api
from flask_login import current_user
import config

login_manager = LoginManager()

app = Flask(__name__)

app.secret_key = config.SECRET_KEY

login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id==userid)
    except models.DoesNotExist:
        return None



CORS(quotes_api, origins=["http://localhost:3000"], supports_credentials=True)
CORS(users_api, origins= ["http://localhost:3000"], supports_credentials=True)
app.register_blueprint(quotes_api, url_prefix='/api/v1')
app.register_blueprint(users_api, url_prefix='/users')



@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'hi'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)










from flask import Flask
from flask_login import LoginManager
import models
from flask_cors import CORS

DEBUG = True
PORT = 8000



CORS(users_api, origins= ["http://localhost:3000"], supports_credentials=True)
app.register_blueprint(users_api, url_prefix='/users')




@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'hi'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)










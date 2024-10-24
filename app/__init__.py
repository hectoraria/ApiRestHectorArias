from flask import Flask
from flask_jwt_extended import JWTManager

from app.directores.routes import directoresBP
from app.supermercados.routes import supermercadosBP

from users.routes import usersBP
import string
import secrets

alphabet = string.ascii_letters + string.digits
password = ''.join(secrets.choice(alphabet) for i in range(8))

app = Flask(__name__)

app.register_blueprint(directoresBP, url_prefix='/directores')
app.register_blueprint(supermercadosBP, url_prefix='/supermercados')
app.register_blueprint(usersBP, url_prefix='/users')

app.config['SECRET_KEY'] = password

jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5351)
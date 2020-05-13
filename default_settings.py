import os

# https://flask.palletsprojects.com/en/1.1.x/config/#
ENV = "development"
DEBUG = True
SECRET_KEY = os.environ.get("APP_SECRET_KEY")
MAX_CONTENT_LENGTH = 3 * 1024 * 1024

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///data.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True

# https://flask-jwt-extended.readthedocs.io/en/latest/options.html
# https://pyjwt.readthedocs.io/en/latest/algorithms.html
JWT_ALGORITHM = "RS256"
JWT_PUBLIC_KEY = open("./certs/pubkey.pem").read()
JWT_PRIVATE_KEY = open("./certs/localhost.key").read()

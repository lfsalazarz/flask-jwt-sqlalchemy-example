import os


DEBUG = True
MAX_CONTENT_LENGTH = 3 * 1024 * 1024
SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///data.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True

# https://flask-jwt-extended.readthedocs.io/en/latest/options.html
# https://pyjwt.readthedocs.io/en/latest/algorithms.html
JWT_ALGORITHM = "RS256"
JWT_PUBLIC_KEY = open("./certs/pubkey.pem").read()
JWT_PRIVATE_KEY = open("./certs/localhost.key").read()

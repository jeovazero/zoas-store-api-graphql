from flask import Flask
from flaskr.graphqlr.view import ZoasGraphQLView
from flask_cors import CORS
from .graphqlr import schema
from .database import seed
import os


# Flags
TESTING = os.getenv("FLASK_TESTING", False)
ENV = os.getenv("FLASK_ENV", "production")
DEVELOPMENT = ENV == "development"


# Deciding to seed
if TESTING or DEVELOPMENT:
    seed()


# The app instance
app = Flask(__name__)


# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
CORS(
    app,
    supports_credentials=True,
    resources={r"/graphql": {"origins": CORS_ORIGINS}},
)


# Aditional config
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "W1r+xoQVRHUeQowoaPysNq6vO3badR1tOPTHwlA46rZKSVLjok8jiG3ue3vE3VU2G/M=",
)
app.config["SESSION_COOKIE_NAME"] = "80l4ch4"


# GraphQL
app.add_url_rule(
    "/graphql",
    view_func=ZoasGraphQLView.as_view(
        "graphql", schema=schema, graphiql=DEVELOPMENT
    ),
)


if __name__ == "__main__":
    app.run()

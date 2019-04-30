from flask import Flask
from flask_graphql import GraphQLView
from flask_cors import CORS
from .graphqlr import schema
from .database import seed
import os


TESTING = os.getenv("FLASK_TESTING", False)
ENV = os.getenv("FLASK_ENV", "production")

if TESTING or ENV == "development":
    seed()

is_graphiql = ENV == "development"

app = Flask(__name__)

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
CORS(app, resources={r"/graphql": {"origins": CORS_ORIGINS}})

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "W1r+xoQVRHUeQowoaPysNq6vO3badR1tOPTHwlA46rZKSVLjok8jiG3ue3vE3VU2G/M=",
)

app.config["SESSION_COOKIE_NAME"] = "80l4ch4"

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql", schema=schema, graphiql=is_graphiql
    ),
)

if __name__ == "__main__":
    app.run()

from flask import Flask
from flask_graphql import GraphQLView
from .graphqlr import schema
from .database import seed
import os


TESTING = os.getenv("FLASK_TESTING", False)
ENV = os.getenv("FLASK_ENV", "production")

if TESTING or ENV == "development":
    seed()

is_graphiql = ENV == "development"

app = Flask(__name__)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql", schema=schema, graphiql=is_graphiql
    ),
)

if __name__ == "__main__":
    app.run()

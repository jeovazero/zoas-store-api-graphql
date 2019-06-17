from flask import Flask
from flaskr.graphqlr.view import ZoasGraphQLView
from flask_cors import CORS
from .graphqlr import schema
from .database import seed


def create_app(env="Production"):
    """Application factory
    :param env: one of [Production | Develpment | Testing]
    """
    configName = "flaskr.config.{}".format(env.capitalize())

    # The app instance
    app = Flask(__name__)
    app.config.from_object(configName)

    # Seed temporary
    # TODO: move it to a script
    seed()

    # CORS
    CORS_ORIGINS = app.config["CORS_ORIGINS"]
    CORS(
        app,
        supports_credentials=True,
        resources={r"/graphql": {"origins": CORS_ORIGINS}},
    )

    # GraphQL
    SHOW_GRAPHIQL = app.env != "production"
    app.add_url_rule(
        "/graphql",
        view_func=ZoasGraphQLView.as_view(
            "graphql", schema=schema, graphiql=SHOW_GRAPHIQL
        ),
    )

    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()


def create_app(env="Production"):
    """Application factory
    :param env: one of [Production | Develpment | Testing]
    """
    configName = "flaskr.config.{}".format(env.capitalize())

    # The app instance
    app = Flask(__name__)
    app.config.from_object(configName)

    # Database
    db.init_app(app)

    # to avoid circular dependencies
    from .graphqlr.view import ZoasGraphQLView
    from .graphqlr.schema import schema

    # add seed-db command
    from .seed import seed_command

    app.cli.add_command(seed_command)

    # CORS
    CORS_ORIGINS = app.config["CORS_ORIGINS"]
    CORS(
        app,
        supports_credentials=True,  # important for cookies
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

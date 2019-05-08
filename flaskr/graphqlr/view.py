from flask_graphql import GraphQLView
from graphql.error.located_error import GraphQLLocatedError
from .errors import ZoasError


class ZoasGraphQLView(GraphQLView):
    @staticmethod
    def format_error(error):
        try:
            if isinstance(error, GraphQLLocatedError):
                return format_located_error(error)
        except Exception as error:
            return GraphQLView.format_error(error)
        else:
            return GraphQLView.format_error(error)


def format_located_error(error):
    if isinstance(error.original_error, GraphQLLocatedError):
        return format_located_error(error.original_error)
    if isinstance(error.original_error, ZoasError):
        return {
            "message": error.original_error.message,
            "code": error.original_error.code,
        }
    return GraphQLView.format_error(error)

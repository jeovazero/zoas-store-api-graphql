from .schema import schema
from graphql.utils import schema_printer
from os import path

GRAPHQLR_FOLDER = path.dirname(path.abspath(__file__))
schema_filename = path.join(GRAPHQLR_FOLDER, "schema.graphql")

if __name__ == "__main__":
    schema_str = schema_printer.print_schema(schema)

    with open(schema_filename, "w") as writer:
        writer.write(schema_str)

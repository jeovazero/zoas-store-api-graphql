import sys
from os import path
from graphql.utils import schema_printer

root = path.dirname(path.dirname(path.realpath(__file__)))  # noqa: E402
sys.path += [root]  # noqa: E402
from flaskr.graphqlr.schema import schema


graphqlr_dir = path.join(root, "flaskr/graphqlr")
schema_filename = path.join(graphqlr_dir, "schema.graphql")

schema_str = schema_printer.print_schema(schema)

if __name__ == "__main__":
    with open(schema_filename, "w") as writer:
        writer.write(schema_str)
        print("generated on: ", schema_filename)

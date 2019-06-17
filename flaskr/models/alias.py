from flaskr import db
from typing import Any

# to avoid mypy error: Invalid base class
# https://github.com/python/mypy/issues/3587
Base = db.Model  # type: Any

Column = db.Column
Integer = db.Integer
Float = db.Float
Boolean = db.Boolean
String = db.String
relationship = db.relationship
PrimaryKeyConstraint = db.PrimaryKeyConstraint
ForeignKey = db.ForeignKey

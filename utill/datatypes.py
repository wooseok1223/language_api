from datetime import datetime
from sqlalchemy import inspect
from sqlalchemy.orm import class_mapper


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

def convert_to_query_dict(obj):
    return [u.__dict__ for u in obj]


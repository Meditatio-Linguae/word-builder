from sqlalchemy.inspection import inspect


def autoclone(obj):
    cls = type(obj)
    mapper = inspect(cls)
    return cls(**{
        column.key: getattr(obj, column.key)
        for column in mapper.columns
        if not column.primary_key
    })

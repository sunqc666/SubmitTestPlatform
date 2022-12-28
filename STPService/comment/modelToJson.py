"""

======================

@author:sunqiucheng

@time:2022/10/11:10:28 上午

======================

"""
def serialize(model):
    from sqlalchemy.orm import class_mapper
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)
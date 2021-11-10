from .meta import MetaClass

class AsyModel(dict,metaclass=MetaClass):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'Model' object has no attribute {key}")
    
    def __setattr__(self, key, value):
        self[key] = value

    class Query:
        def __init__(self, select):
            self.cur_sql = select

        def to_sql(self):
            return self.cur_sql

    @classmethod
    def query(cls, *field_names):
        return cls.Query(cls.__select__(field_names=field_names))


    def save(self):
        pass
class Field(object):
    def __init__(self, column_type, primary_key, default):
        self.name = None  # meta进行修改
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)


class StringField(Field):
    def __init__(self,length=100,primary_key=False, default=""):
        super().__init__(f'varchar({length})', primary_key, default)


class BooleanField(Field):
    def __init__(self, default=False):
        super().__init__('boolean', False, default)


class IntegerField(Field):
    def __init__(self, primary_key=False, default=0):
        super().__init__('bigint', primary_key, default)


class FloatField(Field):
    def __init__(self, primary_key=False, default=0.0):
        super().__init__('real', primary_key, default)


class TextField(Field):
    def __init__(self, default=""):
        super().__init__('text', False, default)

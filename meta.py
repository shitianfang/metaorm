from .fields import Field
from functools import partial


class MetaClass(type):

    def __select__(tablename, primarykey, field_names):
        if field_names:
            return f'SELECT {primarykey},{",".join(field_names)} FROM {tablename}'
        else:
            return f'SELECT * FROM {tablename}'

    def __insert__(tablename, field_names):
        return f'INSERT INTO {tablename} ({",".join(field_names)}) VALUES ({",".join(map(lambda name: f"${name}",field_names))})'

    def __update__(tablename, field_names):
        return f'UPDATE {tablename} SET {",".join(f"{name} = {tmpl}" for name,tmpl in zip(field_names,map(lambda name: f"${name}",field_names)) )}'

    def __new__(cls, name, bases, attrs):

        # 排除对AsyModel类的修改
        if name == "AsyModel":
            return type.__new__(cls, name, bases, attrs)

        # 保存所有字段
        mappings = {}
        field_names = []
        primarykey = None
        tablename = attrs.get("__tablename__", None) or name.lower()

        for key, value in attrs.items():
            # print(key,value)
            if isinstance(value, Field):
                mappings[key] = value
                value.name = key
                if value.primary_key == True:
                    if not primarykey:
                        primarykey = key
                    else:
                        raise Exception(
                            f'Duplicate primary key for field: {key}')
                else:
                    field_names.append(key)

        if not primarykey:
            raise Exception('Primary key not found')

        # 删除子类属性，防止干扰
        for key in mappings.keys():
            attrs.pop(key)

        # escaped_field_names=list(map(lambda field_name:f"{field_name}",field_names))
        # template_field_names=list(map(lambda field_name:f"${field_name}",escaped_field_names))

        attrs["__mappings__"] = mappings
        attrs["__tablename__"] = tablename
        attrs["__primarykey__"] = primarykey
        attrs["__fields__"] = field_names

        attrs['__select__'] = partial(
            cls.__select__, tablename=tablename, primarykey=primarykey)
        attrs['__insert__'] = partial(cls.__insert__, tablename=tablename)
        attrs['__update__'] = partial(cls.__update__, tablename=tablename)
        attrs['__delete__'] = f'DELETE FROM {tablename}'

        # where手动写入
        # attrs['__where__'] =
        return type.__new__(cls, name, bases, attrs)






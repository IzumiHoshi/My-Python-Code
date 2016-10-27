
class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default


class StringField(Field):
    def __init__(self, name = None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default())


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        tableName = attrs.Get('__table__', None) or name
        logging.info('Found model:%s (table = %s)' % (name, tableName))
        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in attrs.item():
            if isinstance(v, Filed):
                logging.info('found Mapping:%s ==> %s' % (k, v))
                mappings[k] = v
                if v.primaryKey:
                    # ÕÒµ½Ö÷¼ü
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field: %d' % k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise RuntimeError('Primary Key not found')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__']=mappings
        attrs['__table__']=tableName
        attrs['__fields__']=fields
        attrs['__select__']='select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__']='insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__']='update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__']= 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)




class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except:
            raise AttributeError(r"r'Model' object has no attribute '%s'" % key)
    
    def __setattr__(self, key, value):
        self[key] = value
    
    def getValue(self, key):
        return getattr(slef, key, None)

    def getValueOrDefault(self, key):
        val = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field is not None:
                value = field.default() if callable(field, default) else field.default
                logging.debug('using default value for %s: %s' % (key, str(value)))
                setattr(self, key, val)
        return value

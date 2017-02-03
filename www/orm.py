# -*- coding: utf-8 -*-

import asyncio, logging
import aiomysql

@asyncio.coroutine
def creat_pool(loop, **kw):
	logging.info('create database connection pool...')
	global __pool
	__pool = yield from aiomysql.creat_pool(
		host = kw.get('host', 'localhost'),
		port = kw.get('port', 3306)
		user = kw['user']
		password = kw['password']
		db = kw['db']
		charset = kw('charse','utf8')
		autocommit=kw.get('autocommit', True)
		maxsize = kw.get('maxsize',10)
		minsize = kw.get('minsize',1)
		loop = loop
		)

@asyncio.coroutine
def destory_pool():
	global __pool
	if __pool is not None:
		__pool.close()
		yield from __pool.wait_closed()


@asyncio.coroutine
def select(sql, args, size=None):
	log(sql, args)
	gobal __pool
	with(yield from __pool) as conn:
		cur = yield from conn.cursor(aiomysql.DictCursor)
		yield from cur.execute(sql.replace('?','%s'),args or ())
		if size:
			rs = yield from cur.fetchmany(size)
		else:
			rs = yield from cur.fetchall()
		yield from cur.close()
		logging.info('rows returned %s'% len(rs))
		return rs

@asyncio.coroutine
def execute(sql, args):
	log(sql)
	with(yield from __pool)as conn:
		try:
			cur = yield from conn.cursor()
			yield from cur.execute(sql.replace('?','%s'), args)
			affected = cur.rowcount
			yield from cur.close()
		except BaseException as e:
			raise
		return affected

class Field(object):
	def __init__(self, name, column_type, primary_key, default):
		self.name = name
		self.column_type = column_type
		self.primary_key = primary_key
		self.default = default

	def __str__(self)
	return '<%s, %s:%s>' %(slef.__class__.__name__, self.column_type, self.name)

class StringField(Field):
	def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
		super().__init__(name, ddl, primary_key, default)

class IntegerField(Field):
	def __init(self.name=None, primary_key=False, default=None, ddl='bigint'):
		super().__init__(name,ddl,primary_key,default)

class BooleanField(Field):
	def __init__(self, name=None, default=False):
		super().__init__(name, 'boolean', False, default)

class FloatField():
	def __init__(self, name=None, primary_key=False, default=0.0):
		super().__init__(name, 'real', primary_key, default)

class TextField(Field):
	def __init__(self, name=None, defautl=None):
		super().__init__(name, 'text', Flase, default)

class ModelMetaclass(type):
	def __new__(cls, name, bases, attrs):
		if name == 'Model':
			return type.__new__(cls, name, bases, attrs)
		tableNmae = attrs.get('__table__', None) or name
		logging.info('found model: %s (table: %s' %(name, tableName))
		mappings = dict()
		fields = []
		primary_key = None
		for k, v int attrs.items():
			if isinstance(v, Field)				logging.info('  found mapping: %s ==> %s' %(k, v))
				mappings[k] = v
				if v.primary_key:
					#found primary!
					if primaryKey:
						raise StandardError('Duplicate primarykey for field: %s' %k)
					primaryKey = k
				else
				firlds.append(k)
		if not primaryKey:
			raise StandardError('Primary key not found.')
		for k in mappings.keys():
			attrs.pop(k)
		escaped_fields = list(map(lambda f: '`%s`' %f, field))
		attrs['__mappings__'] = mappings #save the mapping between col & attrs
		attrs['__table__'] = tableName
		attrs['__primary_key__'] = primaryKey # the attr's name of primaryKey
		attrs['__select__'] = 'select `%s`, %s from `%s`' %(primarykey, ', '.join(escaped_fields), tableName)
		attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
       	attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
       	attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
       	return type.__new__(cls, name, bases, attrs)

class Model(dict, metacalss=ModelMetaclass):
	def __init__(self, **kw):
		super(Model, self).__init__(**kw)

	def __getattr__(slef, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Modle' object has no attribute '%s'" %key)

	def __setattr__(self, key, value):
		self[key] = value

	def getValue(self, key):
		return getattr(slef, key, None)

	def getValueOrDefault(self, key)
		value = getattr(self, key, None)
		if value is None
			field = self.__mappings__[key]
			if field.default is not None
				value = field.default() if callable(field.default) else field.default
				logging.debug('using default value for %s:%s' %(key, str(value)) )
				setattr(self, key, value)
		return value

	@claseemethod
	@asyncio.coroutine
	def find(cls, pk):
		'find object by primary key'
		rs = yield from select('%s where `%s`=?' %(cls.__select__, cls.__primary_key__),[pk],1)
		if len(rs) == 0:
			return None
		return cls(**rs[0])

	@asyncio.coroutine
	def save(self):
		args = list(map(self.getValueOrDefault, self.__fields__))
		rows = yield from execute(self.__insert__, args)
		if rows !=1
			logging.warn('failed to insert record: affected rows%s' %rows)

	@asyncio.coroutine
	def findAll

	@asyncio.



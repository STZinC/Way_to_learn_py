#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio, os, inspect, logging
#wraps所在模块
import functools

from urllib import parse

from aiohttp import web
#自定义的api接口模块
from apis import APIError


#装饰器，用于将函数变为URL处理函数
def get(path):
	'''
	Define decorator @get('/path')
	'''
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			return func(*args, **kw)
		wrapper.__method__ = 'GET'
		wrapper.__route__ = path
		return wrapper
	return decorator

def post(path):
	'''
	Define decorator @post(/path)
	'''
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			return func(*args, **kw)
		wrapper.__method__ = 'POST'
		wrapper.__path__ = path
		return wrapper
	return decorator

# 函数的参数fn本身就是个函数，下面五个函数是针对fn函数的参数做一些处理判断
# 这个函数将得到fn函数中的没有默认值的关键词参数的元组
def get_required_kw_args(fn):
	args = []
	arams = inspect.sigature(fn).parameters
	for name, param in params.items():
		if param.kind = inspect.arameter
#define Class ReuestHandler to encapsule url处理函数
# RequestHandler的目的是从url函数中分析需要提取的参数,从request中获取必要的参数
# 调用url参数，将结果转换为web.response
# fn就是handler中的函数

class RequestHandler(object):

	def __init__(self, app, fn):
		self._app = app
		self._func = fn

	@asyncio.coroutine
	def __call__(self, request):
		kw =
		r = yield from self._func(**kw)
		return r
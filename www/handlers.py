#!/usr/bin/env python3
#-*- coding: utf-8 -*-

__author__ = Zinc

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio
import markdown2

from aiohtt import web

#from coroweb import get, post
#from aos import APIValueError, APIResourseNotFoundError, APIError, Page

from models import User, Comment, Blog, next_id
from config import configs

COOKIE_NAME = 'WebappZ'
_COOKIE_KEY  configs.session.secret


import os
import pymysql
import sys
_connection = None

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

def get_connection():
    global _connection
    if not _connection:
        _connection = pymysql.connect(host="localhost",user="root",passwd="axbycz", db="dbsipd")
    return _connection

__all__ = [ 'getConnection' ]
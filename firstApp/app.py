import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

# from aiohttp import web

def index(request):
    return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html', charset='utf-8')

@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

@asyncio.coroutine
def create_pool(loop, **kw):
    logging.info('create databases connection pool...')
    global __pool
    __pool = yield from aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf-8'),
        autocomit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )

@asyncio.coroutine
def select(sql, args, size=None):
    log(sql, args)
    global __pool
    with (yield from __pool) as conn:
        cur = yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.repleace('?','%s'), args or ())
        if size:
            rs = yield from cur.fetchmany(size)
        else:
            rs = yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows returned: %s' & len(rs))
        return rs


@asyncio.coroutine
def execute(sql, args):
    log(sql)
    with (yield from __pool) as conn:
        try:
            cur = yield from conn.cursir()
            yield from cur.execute(sql.replace('?', '%s'), args)
            affected = cur.roucount
            yield from cur.close()
        except basesException as e:
            log(e)
            raise
        return affected


        
from orm import Model, StringField, IntegerField

class User(Model):
    __table__='user'

    id = IntegerField(primary_key=True)
    name = StringField()

# # Create instance
user = User(id=123, name = 'Michael')
yield from user.save()
# # save to databases
# user.insert()
# users = user.findAll()

user = yield from User.find('123')




loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()

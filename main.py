from aiohttp import web
import aioredis


bd = {"RUR": 1}


async def main():
    app = web.Application()
    app.add_routes([web.get('/convert', convert)])
    app.add_routes([web.post("/database", database)])
    app['redis'] = await aioredis.create_redis(("redis", 6379), encoding="UTF-8", db=1)
    return app


async def convert(request):
    r = request.app['redis']
    param_from = request.rel_url.query['from']
    param_to = request.rel_url.query['to']
    param_amount = request.rel_url.query['amount']
    value_from = await r.mget(param_from)
    value_to = await r.mget(param_to)
    tmp = int(value_from[0]) * int(param_amount)
    answer = tmp * int(value_to[0]) ** -1
    return web.Response(text=str(answer))


async def database(request):
    r = request.app['redis']
    param_merge = request.rel_url.query.get('merge')
    if param_merge == '0':
        print(121)
        await r.flushdb()
        return {"status": 200}
    else:
        data = await request.json()
        await r.mset(data)


if __name__ == '__main__':
    web.run_app(main())

from aiohttp import web
import aioredis


async def is_digit(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


async def start_server():
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
    value_from, value_to = await r.mget(param_from, param_to)
    if value_from is None or value_to is None:
        return web.json_response({"status": 404, "response": "Not found"})
    tmp = float(value_from) * float(param_amount)
    answer = tmp * float(value_to) ** -1
    return web.json_response({"status": 200, "response": answer})


async def database(request):
    r = request.app['redis']
    param_merge = request.rel_url.query.get('merge')
    if param_merge == '0':
        await r.flushdb()
        return web.json_response({"status": 200})
    elif param_merge == '1':
        data_tmp = await request.json()
        data = {}
        for key, value in data_tmp.items():
            if await is_digit(value):
                data[key] = value
            else:
                return web.json_response({"status": 400, "response": f"{key} is not a digit"})
        await r.mset(data)
        return web.json_response({"status": 200})
    else:
        return web.json_response({'status': 400, "response": "unknown merge argument"})


if __name__ == '__main__':
    web.run_app(start_server())

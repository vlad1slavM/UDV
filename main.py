from aiohttp import web
import aioredis

bd = {"RUR": 1}


async def is_digit(str):
    try:
        float(str[0])
        return True
    except ValueError:
        return False


async def convert_handler(value_from, value_to, param_amount):
    if await is_digit(value_from) is False and await is_digit(value_to) is False:
        return web.json_response({"status": 400, "response": "both values are not a digit"})
    elif await is_digit(value_from) is False:
        return web.json_response({"status": 400, "response": "value from it`s not digit"})
    elif await is_digit(value_to) is False:
        return web.json_response({"status": 400, "response": "value to it`s not digit"})
    else:
        tmp = float(value_from[0]) * float(param_amount)
        answer = tmp * float(value_to[0]) ** -1
        return answer


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
    value_from = await r.mget(param_from)
    value_to = await r.mget(param_to)
    answer = await convert_handler(value_from, value_to, param_amount)
    return web.Response(text=str(answer))


async def database(request):
    r = request.app['redis']
    param_merge = request.rel_url.query.get('merge')
    if param_merge == '0':
        await r.flushdb()
        return web.json_response({"status": 200})
    elif param_merge == '1':
        data = await request.json()
        await r.mset(data)
        return web.json_response({"status": 200})
    else:
        return web.json_response({'status': 400, "response": "unknown merge argument"})


if __name__ == '__main__':
    web.run_app(start_server())

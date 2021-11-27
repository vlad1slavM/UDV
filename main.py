from aiohttp import web
import aioredis


bd = {"RUR": 1}


async def main():
    r = aioredis.from_url("redis://redis", encoding='UTF-8')
    app = web.Application()
    app.add_routes([web.get('/convert', convert)])
    app.add_routes([web.post("/database", database)])
    app['redis'] = r
    return app


async def convert(request):
    r = request.app['redis']
    param_from = request.rel_url.query['from']
    param_to = request.rel_url.query['to']
    param_amount = request.rel_url.query['amount']
    print(f"param_from = {param_from}")
    print(f"param_to = {param_to}")
    value_from = await r.get(param_from)
    value_to = await r.get(param_to)
    print(value_to)
    print(value_from)
    tmp = value_from ** -1 * int(param_amount)
    answer = tmp * value_to
    return web.Response(text=str(answer))


async def database(request):
    r = request.app['redis']

    param_merge = request.rel_url.query['merge']
    if int(param_merge) == 0:
        r.flushdb()
    else:
        param_currency = request.rel_url.query['currency']
        param_amount = request.rel_url.query['amount']
        await r.set(param_currency, 1 / int(param_amount))
        print(f"param pam pam = {await r.get(param_currency)}")
        print(type(param_currency), param_currency)
        print(f"param pam pam = {await r.get(param_currency)}")


if __name__ == '__main__':
    web.run_app(main())
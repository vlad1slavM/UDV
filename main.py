from aiohttp import web
import redis
"GET /convert?from=USD&to=RU&amount=42"


bd = {"RUR": 1}
r = redis.Redis()


async def convert(request):
    param_from = request.rel_url.query['from']
    param_to = request.rel_url.query['to']
    param_amount = request.rel_url.query['amount']
    tmp = bd[param_from] ** -1 * int(param_amount)
    answer = tmp * bd[param_to]
    return web.Response(text=str(answer))


async def database(request):
    param_merge = request.rel_url.query['merge']
    if int(param_merge) == 0:
        bd.clear()
        r.flushdb()
    else:
        param_currency = request.rel_url.query['currency']
        param_amount = request.rel_url.query['amount']
        r.set(param_currency, 1 / int(param_amount))
        bd[param_currency] = 1 / int(param_amount)
        print(bd)

app = web.Application()
app.add_routes([web.get('/convert', convert)])
app.add_routes([web.post("/database", database)])
web.run_app(app)

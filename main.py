from aiohttp import web
"GET /convert?from=RUR&to=USD&amount=42"


async def convert(request):
    param_from = request.rel_url.query['from']
    param_to = request.rel_url.query['to']
    param_amount = request.rel_url.query['amount']
    result = f"from : {param_from} to : {param_to} amount : {param_amount}"
    return web.Response(text=str(result))

app = web.Application()
app.add_routes([web.get('/convert', convert)])
web.run_app(app)

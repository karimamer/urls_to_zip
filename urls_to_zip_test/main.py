import json
import zipfile
import io
import asyncio
import aiohttp
from aiohttp import web
import aiohttp_cors
import requests
from aiohttp.web import middleware
from aiojobs.aiohttp import setup, spawn
import aiojobs



async def health_check(request):
    return web.Response(text="servie is up and running")

async def aysnc_coro(lst):
    for data in lst:
        gif = requests.get(data["url"]).content
        gif_stream = io.BytesIO(gif)
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, "a", zipfile.ZIP_DEFLATED, False,compresslevel=1) as zf:
            zf.writestr(data["filename"], gif_stream.getvalue())
    return memory_file

@aiojobs.aiohttp.atomic
async def archive_img(request):
    data = await request.json()
    memory_file = await aysnc_coro(data)
    resp = web.StreamResponse()
    resp.headers['Content-Type'] = "application/zip"
    await resp.prepare(request)
    await resp.write(memory_file.getvalue())
    return resp

routes_list = [
    web.get("/health-check", health_check),
    web.get("/archive", archive_img),

]


app = web.Application()
app.add_routes(routes_list)


# Configure default CORS settings.
cors = aiohttp_cors.setup(
    app,
    defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True, expose_headers="*", allow_headers="*",
        )
    },
)

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)
setup(app, limit=1000)
web.run_app(app)

import asyncio
import io
import zipfile

import aiohttp
import aiohttp_cors
from aiohttp import web


async def health_check(_request):
    return web.Response(text="service is up and running")


async def fetch_compress(session: aiohttp.ClientSession, zf: zipfile.ZipFile, resp ,buffer , url: str, name: str):
    # the code here is not thread safe. I hacked away around passing the buffer around in single thread becouse
    # python zipfile lib is not asyncio compatabilbe
    async with session.get(url) as response:
        zf.writestr(name, await response.read())
        # copy buffer into response
        await resp.write(buffer.getvalue())
        # flush buffer
        buffer.truncate(0)
       

async def archive_img(request):
    data = await request.json()
    assert isinstance(data, list)

    # Initialize stream response 
    resp = web.StreamResponse()
    resp.content_type = "application/zip"
    await resp.prepare(request)

    # Initialize buffer
    outfile = io.BytesIO()
    async with aiohttp.ClientSession() as session:
        with zipfile.ZipFile(outfile, "w") as zf:
            await asyncio.gather(*(fetch_compress(session, zf,resp ,outfile ,item["url"], item["filename"]) for item in data))

    await resp.write_eof()
    return resp

routes_list = [
    web.get("/health-check", health_check),
    web.post("/archive", archive_img),

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
web.run_app(app)
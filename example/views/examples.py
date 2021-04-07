"""Bellow just some more examples"""

import muffin

from example import app


@app.route('/html')
async def html(request):
    """Return html response."""
    return 'HTML content'


@app.route('/json')
async def json(request):
    """Return JSON response."""
    return {'json': 'here'}


@app.on_error(muffin.ASGINotFound)
async def handle404(request):
    """Setup custom 404 page."""
    return muffin.Response('Custom 404 Page', status_code=404)


@app.route('/api/example', '/api/example/{example}')
class Example(muffin.Handler):
    """ Custom handler in REST-like style. """

    async def get(self, request):
        return {'simple': 'rest', 'example': request.path_params.get('example')}

    async def post(self, request):
        return [1, 2, 3]


@app.route('/stream')
async def response_stream(request):
    """Stream response."""
    from asgi_tools.utils import aio_sleep  # only to support both asyncio/trio

    async def stream():
        for n in range(10):
            yield str(n)
            await aio_sleep(1)
            print(n)

    return muffin.ResponseStream(stream(), content_type='text/plain')

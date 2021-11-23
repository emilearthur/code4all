# WSGI  - Web Service Gateway Interface 

# WSGI 
def request(environ, start_response):
    r = start_response(environ)
    # ...
    return r 


# ASGI 
async def app(scope, receive, send):
    r = await receive(scope)
    # ... 
    return await send(r, scope)
    
from typing import Optional

import fastapi
import uvicorn 

api = fastapi.FastAPI()

@api.get('/')
def index():
    body = "<html>" \
        "<body style='padding: 10px;'>"\
        "<h1>Welcome to the API</h1>" \
        "<div>"\
        "Try it: <a href='/api/calculate?x=7&y=11'>/api/calculate?x=7&y=11</a>"\
        "</div>"\
        "</body>" \
        "</html>"

    return fastapi.responses.HTMLResponse(content=body)

error_dict = {"error":" ERROR: Z cannot be zero."}
@api.get('/api/calculate')
def calculate(x: int, y: int, z: Optional[int] = None):
    if z is not None and z == 0:
        return fastapi.responses.JSONResponse(
            content=error_dict,
            #media_type="application/json",
            status_code=400)
    
    value = x + y
    if z is not None:
        value /= z

    #return {
    #    'x': x,
    #    'y': y, 
    #    'z': z,
    #    'value': value
    #}
    return value

# running code 
uvicorn.run(api, host="127.0.0.1", port=8080)
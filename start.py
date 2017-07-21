from flask import Flask, render_template, request, abort, Response, redirect
from util.config import *
import requests
import http.client
from util import httpCodes

app = Flask(__name__)
HOSTS = {

"static_provider": "127.0.0.1:8888",

"authenticator": "127.0.0.1:10000",
"user": "127.0.0.1:20000"

}
#
CHUNK_SIZE = 1024

@app.route('/', methods=['GET'])
def provider():
    url = 'http://'+HOSTS.get('static_provider')
    return redirect(url)

@app.route('/<path:url>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(url):
    r = route(url, request)
    headers = dict(r.headers)
    def generate():
        if(r.status_code != httpCodes.FORBIDDEN):
            for chunk in r.iter_content(CHUNK_SIZE):
                yield chunk
    return Response(generate(), r.status_code)


def route(url, request):
    try:
        pathUri = url.split('/')
        url = 'http://'+HOSTS.get(pathUri[0])+'/'+pathUri[1]
    except Exception as error:
        return(Response('Service not registered', httpCodes.FORBIDDEN))

    if(request.method == 'GET'):
        return requests.get(url, stream=True , params=request.args, headers=request.headers)

    elif(request.method == 'POST'):
        return requests.post(url, stream=True , params=request.args, headers=request.headers)

    elif(request.method == 'PUT'):
        return requests.put(url, stream=True , params=request.args, headers=request.headers)

    elif(request.method == 'DELETE'):
        return requests.delete(url, stream=True , params=request.args, headers=request.headers)

    else:
        return(httpCodes.NOT_FOUND)


if(__name__ == '__main__'):
    app.run(host=ADRESS, port=PORT, debug=DEBUG)

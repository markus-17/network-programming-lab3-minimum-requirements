from flask import Flask, request, make_response

datastore = {}
app = Flask(__name__)


@app.route("/<key>", methods=['POST'])
def create(key):
    content_type = request.headers.get('Content-Type', type=str)
    response = make_response()
    if key in datastore:
        response.status_code = 409
    else:
        body = request.get_data()
        datastore[key] = {
            "type": content_type,
            "value": body
        }
        response.status_code = 201
        response.headers.add('Location', f'/{key}')
    return response


@app.route("/<key>", methods=['GET'])
def read(key):
    response = make_response()
    if key in datastore:
        response.status_code = 200
        response.headers.add('Content-Type', datastore[key]['type'])
        response.set_data(datastore[key]['value'])
    else:
        response.status_code = 404
    return response


@app.route("/<key>", methods=['PUT'])
def update(key):
    content_type = request.headers.get('Content-Type', type=str)
    response = make_response()
    if key in datastore:
        response.status_code = 204
    else:
        response.status_code = 201
        response.headers.add('Location', f'/{key}')
    body = request.get_data()
    datastore[key] = {
        "type": content_type,
        "value": body
    }
    return response


@app.route("/<key>", methods=['DELETE'])
def delete(key):
    response = make_response()
    if key in datastore:
        response.status_code = 200
        response.headers.add('Content-Type', datastore[key]['type'])
        response.set_data(datastore[key]['value'])
        del datastore[key]
    else:
        response.status_code = 404
    return response


if __name__ == '__main__':
    app.run('localhost', 8080, False, False)

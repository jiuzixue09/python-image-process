import base64
from io import BytesIO

from flask import Flask, request

from phash import Phash as p, HttpClientTools as http

app = Flask(__name__)


@app.route('/phash/bytes', methods=['POST'])
def im_byte_io_to_phash():
    byte_array = request.data
    img = BytesIO(byte_array)
    im_hash = p.image_to_hash(img)

    return im_hash


@app.route('/phash/base64', methods=['POST'])
def im_base64_to_phash():
    content = request.data
    try:
        img = BytesIO(base64.b64decode(content))
        im_hash = p.image_to_hash(img)
    except Exception as e:
        return '-1'

    return im_hash


@app.route('/phash')
def im_url_to_phash():
    url = request.args.get("url")
    try:
        byte_array = http.do_get(url)
        if byte_array is None:
            return '-1'
        img = BytesIO(byte_array)
        im_hash = p.image_to_hash(img)
    except Exception as e:
        return '-1'

    return im_hash


if __name__ == "__main__":
    app.run(host='0.0.0.0')

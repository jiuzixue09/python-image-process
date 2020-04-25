import base64
from io import BytesIO

from flask import Flask, request

from image_socre.aesthetics import Aesthetics
from phash import HttpClientTools as http

app = Flask(__name__)


aesthetic = Aesthetics()


@app.route('/score/bytes', methods=['POST'])
def im_byte_io_score():
    byte_array = request.data
    try:
        img = BytesIO(byte_array)
        score = float(aesthetic.aesthetic_score(img))
    except Exception as _:
        return '-1'

    return str(score)


@app.route('/score/base64', methods=['POST'])
def im_base64_score():
    content = request.data
    try:
        img = BytesIO(base64.b64decode(content))
        score = float(aesthetic.aesthetic_score(img))
    except Exception as _:
        return '-1'

    return str(score)


@app.route('/score')
def im_url_score():
    url = request.args.get("url")
    try:
        byte_array = http.do_get(url)
        if byte_array is None:
            return '-1'
        img = BytesIO(byte_array)
        score = float(aesthetic.aesthetic_score(img))
    except Exception as _:
        return '-1'

    return str(score)


if __name__ == "__main__":
    app.run(host='0.0.0.0')


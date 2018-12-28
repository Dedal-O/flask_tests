from flask import Flask, request
from datetime import datetime

app = Flask(__name__)


@app.route('/echo/', methods=['GET', 'POST'])
def test_receive():
    if request.method == 'POST':
        app.logger.info(f"{datetime.now()} ECHO Received POST. Containes: {request.get_data()}")
        return f"""<html><head><title></title></head>
                <body>
                Thanks for you data
                </body>
                </html>
                """

    if request.method == 'GET':
        app.logger.info(f"{datetime.now()} ECHO Received GET. Containes:(will be later)'")
        return f"""<html><head><title></title></head>
                <body>
                Thanks for visit
                </body>
                </html>
                """


@app.route("/")
def hello():
    return f"""
    Welcome to Index Page<br/>
    """


if __name__ == "__main__":
    app.run()

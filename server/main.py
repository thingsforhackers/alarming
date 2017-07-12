"""
Server side of alarm project
"""
from flask import Flask

import common.constants as const

app = Flask(const.APP_NAME,
            static_folder=const.SERVER_STATIC_DIR)

@app.route("/")
def hello_world():
    return "Hello World"


if __name__ == "__main__":
    app.run()

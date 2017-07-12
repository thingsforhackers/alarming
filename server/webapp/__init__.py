from flask import Flask

from webapp.hello.views import hello
import common.constants as const


app = Flask(const.APP_NAME,
            static_folder=const.SERVER_STATIC_DIR)
app.register_blueprint(hello)

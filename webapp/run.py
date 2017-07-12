import os
from flask import Flask

from webapp.hello.views import hello
import common.constants as const

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask(const.APP_NAME,
            static_folder=const.SERVER_STATIC_DIR,
            template_folder=os.path.join(dir_path, "templates"))
app.register_blueprint(hello)

app.run(debug=True)

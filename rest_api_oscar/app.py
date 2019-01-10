import logging.config

import os,sys
from flask import Flask, Blueprint, send_from_directory
from rest_api_oscar import settings
from rest_api_oscar.api.oscar.endpoints.stations import ns as stations_namespace
from rest_api_oscar.api.oscar.endpoints.auth import ns as auth_namespace
from rest_api_oscar.api.restplus import api

app = Flask(__name__)

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.INFO)
#logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
#logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

@app.route("/")
def static_index():
    return send_from_directory("static", "index.html")

def configure_app(flask_app):
    print("config")
    log.info("configuring app")

    #flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

    flask_app.config['OSCAR_URL'] = settings.OSCAR_URL
    
def initialize_app(flask_app):
    print("init")
    log.info("initializing app")
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(stations_namespace)
    flask_app.register_blueprint(blueprint)
    
    
def main():
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)

initialize_app(app)

if __name__ == "__main__":
    main()
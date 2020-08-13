import os
from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Todo: SECRET_KEY should be overridden with a random value when deploying, e.g. a long random string of bytes
    app.config.from_mapping(
        # for signing session cookies or any other security related needs by extensions or your application
        # set to 'dev' for development convenience
        SECRET_KEY='dev',
        # Path to database file
        DATABASE=os.path.join(app.instance_path, 'webapp.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a hello page for testing
    @app.route('/hello')
    def hello():
        return "Hello World!"

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/signup')
    def signup():
        return render_template('signup.html')

    from . import db
    db.init_app(app)

    return app

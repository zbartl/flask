import os

from flask import Flask, jsonify, request
from open_flask_auth import OpenFlaskAuth


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from flaskr import db
    db.init_app(app)

    # oauth setup
    oauth_provider = OpenFlaskAuth(app, "secret")
    oauth_provider.register_routes()

    @app.route('/hello')
    @oauth_provider.require_oauth('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/posts')
    @oauth_provider.require_oauth('/posts')
    def list_posts():
        data = []
        posts = blog.list_posts()
        for row in posts:
            data.append((list(row)))
        return jsonify(posts=data)

    # apply the blueprints to the app
    from flaskr import auth, blog, oauth
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    # apply oauth blueprint
    oauth = oauth.OAuth(oauth_provider)
    app.register_blueprint(oauth.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app

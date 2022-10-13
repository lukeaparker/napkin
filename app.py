import os
from os import environ
from flask import Flask, Blueprint, request, jsonify, redirect, session, g, render_template
from flask_session import Session
from database import database
import redis 
from flask_cors import CORS

def create_app(mode='default'):
    """Creates a napkin instance."""
    # Create a new Flask app
    app = Flask(__name__, template_folder="napkin/views/templates",
                static_folder="napkin/views/static")
    


    # Configure database with current app context
    with app.app_context():
        database.load_app()
        app.secret_key = 'the random string'


        # Register manager blueprint
        from napkin.views.views import views as views_blueprint
        app.register_blueprint(views_blueprint, url_prefix="")

        # Register api blueprint
        from napkin.api.api import api as api_blueprint
        app.register_blueprint(api_blueprint, url_prefix="/api")

        # Register Error Pages
        @app.errorhandler(404)
        def err404(e):
            return render_template('/errors/404.html', showStackTrace = True, stackTrace = str(e), errorCode = 404)

        @app.errorhandler(500)
        def err404(e):
            return render_template('/errors/500.html', showStackTrace = True, stackTrace = str(e), errorCode = 500)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host=os.environ.get('HOST'), port=os.environ.get('FLASK_RUN_PORT'))

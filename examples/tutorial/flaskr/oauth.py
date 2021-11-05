from flask import (
    Blueprint, g, render_template, abort
)
from open_flask_auth import EnrollmentError

from flaskr.auth import login_required


class OAuth:
    def __init__(self, oauth_provider):
        self.oauth_provider = oauth_provider
        self.bp = self.register_blueprint()

    def register_blueprint(self):
        bp = Blueprint('oauth', __name__, url_prefix="/oauth")

        @bp.route('/enroll', methods=['POST'])
        @login_required
        def enroll():
            try:
                public, secret = self.oauth_provider.enroll(g.user['id'])
            except EnrollmentError:
                abort(400)

            return render_template('oauth/enroll.html', public_key=public, secret_key=secret)

        return bp

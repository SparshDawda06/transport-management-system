from flask import render_template, jsonify
from . import bp
from ..auth import login_required, get_current_user


@bp.route("/")
@login_required
def index():
    return render_template("index.html", username=get_current_user())


@bp.route("/health")
def health():
    return jsonify({"status": "ok"})

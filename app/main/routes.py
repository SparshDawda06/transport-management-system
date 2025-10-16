from flask import render_template, jsonify, current_app
from . import bp
from ..auth import login_required, get_current_user
import logging

logger = logging.getLogger(__name__)


@bp.route("/")
@login_required
def index():
    try:
        username = get_current_user()
        return render_template("index.html", username=username)
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        return render_template("index.html", username="Unknown"), 500


@bp.route("/health")
def health():
    try:
        return jsonify({"status": "ok", "message": "Transport Management System is running"})
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

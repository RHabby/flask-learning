from flask import Blueprint, render_template

from app import db

blueprint = Blueprint("errors", __name__)


@blueprint.app_errorhandler(404)
def not_found_error(error):
    title = "404 | File not found"
    return render_template("errors/404.html"), 404


@blueprint.app_errorhandler(500)
def internal_server_error(error):
    title = "An unexpected error has occured"
    db.session.rollback()
    return render_template("errors/500.html"), 500

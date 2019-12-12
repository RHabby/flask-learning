from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

# from app.collection.forms import LinkForm
from app.collection.models import Collections
from app.db import db
from app.user.models import User

blueprint = Blueprint("collection", __name__, url_prefix="/collection")


@login_required
@blueprint.route("/")
def index():
    # collection = User.query.filter_by(current_user.username).all()
    return render_template("collection/index.html")

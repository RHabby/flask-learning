from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.collection.forms import UrlForm
from app.collection.models import Collections
from app.collection.url_extractor.url_extractor import (extract_open_graph,
                                                        find_base_url)
from app.collection.url_extractor.utils import save_bookmark
from app.db import db
from app.user.models import User

blueprint = Blueprint("collection", __name__, url_prefix="/collection")


@blueprint.route("/<string:username>")
@login_required
def index(username):
    title = f"Полка | {current_user.username}"
    url_form = UrlForm()
    collection = Collections.query.order_by(
        Collections.created.desc()).filter(Collections.user_id == current_user.id ).all()
    return render_template("collection/index.html", collection=collection, url_form=url_form, title=title)


@blueprint.route("/process-collecting", methods=["POST"])
def process_collecting():
    url_form = UrlForm()
    if url_form.validate_on_submit():
        bookmark_url = url_form.url.data
        og_url_info = extract_open_graph(bookmark_url)
        base_url = find_base_url(bookmark_url)
        bookmark = Collections(title=og_url_info["og:title"], image=og_url_info["og:image"], url=og_url_info["og:url"],
                               base_url=base_url, description=og_url_info["og:description"], content_type=og_url_info["og:type"], user_id=current_user.id)
        flash("Сделано!")
        return redirect(url_for("collection.index", username=current_user.username))
    else:
        for field, errors in url_form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": {}'.format(
                    getattr(url_form, field).label.text, error))
        return redirect(url_for("collection.index", username=current_user.username))

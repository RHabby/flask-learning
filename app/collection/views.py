from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.collection.forms import UrlForm
from app.collection.models import Collections
from app.collection.url_extractor.url_extractor import (extract_open_graph,
                                                        extract_url_info,
                                                        find_base_url)
from app.db import db
from app.user.models import User

blueprint = Blueprint("collection", __name__, url_prefix="/collection")


@blueprint.route("/")
def get_followed_bookmarks():
    url_form = UrlForm()
    title = f"Главная | Полка"
    bookmarks = current_user.followed_bookmarks().all()
    return render_template("collection/followed_bookmarks.html", url_form=url_form, user=current_user, bookmarks=bookmarks, title=title)


@blueprint.route("user/<string:username>/")
@login_required
def index(username):
    url_form = UrlForm()
    user = User.query.filter_by(username=username).first_or_404()
    collection = Collections.query.order_by(
        Collections.created.desc()).filter(Collections.user_id == user.id).all()
    title = f"Полка | {user.username}"

    return render_template("collection/index.html", user=user, collection=collection, url_form=url_form, title=title)


@blueprint.route("/process-collecting", methods=["POST"])
def process_collecting():
    url_form = UrlForm()
    if url_form.validate_on_submit():
        bookmark_url = url_form.url.data
        base_url = find_base_url(bookmark_url)

        og_url_info = extract_open_graph(bookmark_url)

        # temporary decision
        if len(og_url_info) < 2:
            url_info = extract_url_info(bookmark_url)
            print(url_info)
            bookmark = Collections(title=url_info["title"], url=url_info["url"],
                                   base_url=base_url, user_id=current_user.id)
        else:
            bookmark = Collections(title=og_url_info["og:title"], image_url=og_url_info["og:image"],
                                   url=og_url_info["og:url"], base_url=base_url,
                                   description=og_url_info["og:description"], content_type=og_url_info["og:type"],
                                   user_id=current_user.id)

        db.session.add(bookmark)
        db.session.commit()

        flash("Сделано!")
        return redirect(url_for("collection.index", username=current_user.username))
    else:
        for field, errors in url_form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": {}'.format(
                    getattr(url_form, field).label.text, error))
        return redirect(url_for("collection.index", username=current_user.username))

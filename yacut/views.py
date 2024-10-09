import random

from flask import flash, redirect, render_template

from . import app, db
from .forms import UrlMapForm
from .models import URLMap
from .constants import LENGTH_STRING, SYMBOLS


def check_unique_short_id(short_id):
    if URLMap.query.filter(URLMap.short == short_id).first() is None:
        return True
    return False


def get_unique_short_id():
    short_id = ''.join(random.choice(SYMBOLS) for i in range(LENGTH_STRING))
    if check_unique_short_id(short_id):
        return short_id
    return get_unique_short_id()


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if not custom_id:
            custom_id = get_unique_short_id()
        elif not check_unique_short_id(custom_id):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        new_url = URLMap(
            original=form.original_link.data,
            short=custom_id
        )
        db.session.add(new_url)
        db.session.commit()
        return render_template('index.html', url=new_url, form=form)
    return render_template('index.html', form=form)


@app.route('/<short_id>')
def new_link(short_id):
    Url = URLMap.query.filter(URLMap.short == short_id).first_or_404()
    original_url = Url.original
    return redirect(original_url)

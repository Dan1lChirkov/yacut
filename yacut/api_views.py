import re

from flask import jsonify, request
from http import HTTPStatus

from . import app, db
from .models import URLMap
from .error_handlers import InvaldiAPIUsage
from .views import check_unique_short_id, get_unique_short_id
from .constants import LINK_REGEX


@app.route('/api/id/', methods=['POST'])
def creare_short_link():
    data = request.get_json(silent=True)
    if not data:
        raise InvaldiAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvaldiAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' in data:
        custom_id = data.get('custom_id')
        if not check_unique_short_id(custom_id):
            raise InvaldiAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
        if custom_id == '' or custom_id is None:
            data['custom_id'] = get_unique_short_id()
        elif not re.match(LINK_REGEX, custom_id):
            raise InvaldiAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
    else:
        data['custom_id'] = get_unique_short_id()
    new_url = URLMap()
    new_url.from_dict(data)
    db.session.add(new_url)
    db.session.commit()
    return jsonify(new_url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    url_obj = URLMap.query.filter(URLMap.short == short_id).first()
    if not url_obj:
        raise InvaldiAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    original_url = url_obj.original
    return jsonify({'url': original_url}), HTTPStatus.OK

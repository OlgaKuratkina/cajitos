import os

from flask import request, current_app, jsonify, send_from_directory
from flask_login import login_required
from werkzeug.exceptions import BadRequest

from cajitos_site.service import service
from cajitos_site.utils.translate_utils import translate_text


@service.route('/translate', methods=['POST'])
@login_required
def translate_data():
    data = request.json
    current_app.logger.info(f'Recieved data for translation: {data}')
    if 'dest_language' not in data or 'text' not in data:
        return BadRequest()
    return jsonify(
        translate_text(target=data['dest_language'],text=data['text'])
    )


@service.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'favicon.ico', mimetype='vnd.microsoft.icon')


@service.route('/robots.txt')
def robots():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'robots.txt', mimetype='plain_text')


@service.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(current_app.root_path, 'static'),
                               'sitemap.xml')

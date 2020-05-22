from flask import jsonify, request
from flask_login import login_required

from cajitos_site.service import service
from cajitos_site.utils.translate_utils import translate_text


@service.route('/translate', methods=['POST'])
@login_required
def translate_data():
    return jsonify({'text': translate_text(request.form['text'],
                                           request.form['dest_language'])})

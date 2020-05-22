from flask import jsonify, request, current_app
from flask_login import login_required

from cajitos_site.service import service
from cajitos_site.utils.translate_utils import translate_text


@service.route('/translate', methods=['POST'])
@login_required
def translate_data():
    current_app.logger.info('Recieved data for translation:')
    current_app.logger.info(request.form['text'])
    current_app.logger.info(request.form['dest_language'])
    return jsonify({
        'text': translate_text(target=request.form['dest_language'],
                               text=request.form['text'])
    })

from flask import request, current_app, Response
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
    return Response(
        translate_text(target=data['dest_language'],text=data['text'])
    )

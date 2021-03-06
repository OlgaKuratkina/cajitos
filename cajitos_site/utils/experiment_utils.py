import json
import os

file_url = "https://cajitos-my-test.s3.amazonaws.com/check/requirements.txt"
local_url = "/tmp/misc/requirements.txt"
local_config = "/tmp/misc/app_config.json"

# <script>
#         function translate(sourceElem, destElem, destLang) {
#             $(destElem).html('<img src="{{ url_for('static', filename='images/loading.gif') }}">');
#             $.post('/service/translate', {
#                 text: $(sourceElem).text(),
#                 dest_language: destLang
#             }).done(function(response) {
#                 $(destElem).text(response['text'])
#             }).fail(function() {
#                 $(destElem).text("{{ _('Error: Could not contact server.') }}");
#             });
#         }
#     </script>

def check_file_works():
    result = []
    if os.path.exists(local_url):
        with open(local_url, "r") as f:
            result.append(f.readline())

    if os.path.exists(local_config):
        with open(local_config) as json_file:
            data = json.load(json_file)
            result.append(data)
    return result


def check_where_we_are():
    current = os.path.abspath(os.getcwd())
    result = [current]
    for root, dirs, files in os.walk(".", topdown=True):
        for name in files:
            result.append(os.path.join(root, name))
        for name in dirs:
            result.append(os.path.join(root, name))
    return result

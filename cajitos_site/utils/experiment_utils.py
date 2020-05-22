import json
import os

file_url = "https://cajitos-my-test.s3.amazonaws.com/check/requirements.txt"
local_url = "/tmp/misc/requirements.txt"
local_config = "/tmp/misc/app_config.json"


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

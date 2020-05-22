import os

file_url = "https://cajitos-my-test.s3.amazonaws.com/check/requirements.txt"
local_url = "/tmp/misc/requirements.txt"


def check_file_works():
    if os.path.exists(local_url):
        with open(local_url, "r") as f:
            return f.readline()
    return 'No file'

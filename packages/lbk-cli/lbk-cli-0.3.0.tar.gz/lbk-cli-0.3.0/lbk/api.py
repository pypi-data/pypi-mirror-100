import json
from base64 import b64encode
from http.client import HTTPSConnection

from .config import get_config


def send(context, message):
    """
    Send the given message to the specified context.
    :param context: the context
    :param message: the log message
    :return: True if the server accepted the message, otherwise False
    """
    server_url, username, password = get_config()

    credentials = bytes(f"{username}:{password}", encoding='UTF-8')
    user_and_pass = b64encode(credentials).decode("ascii")

    headers = {
        'Authorization': f'Basic {user_and_pass}',
        'Content-Type': 'application/json'
    }

    body = json.dumps({
        'context': context,
        'message': message
    })

    conn = HTTPSConnection(server_url)
    conn.request('POST', '/api/logs', body, headers=headers)
    response = conn.getresponse()

    return response.status == 200

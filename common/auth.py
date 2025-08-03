import base64

def decode_auth_header(auth_header: str):
    encoded_auth_header = auth_header.split(" ")[1]
    decoded_auth_header = base64.b64decode(encoded_auth_header).decode("utf-8")
    username, password = decoded_auth_header.split(":")
    return username, password
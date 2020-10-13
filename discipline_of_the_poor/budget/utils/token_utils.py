"""
Module used to store functions to handle the auth token
"""
import jwt


def payload_from_token(token):
    token_info = jwt.decode(token, verify=False)
    return token_info


def payload_from_auth_header(header):
    token = header.split()[1]
    return payload_from_token(token)

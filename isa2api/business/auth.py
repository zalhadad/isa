#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import (BadSignature, SignatureExpired, base64_decode,
                          base64_encode)
from passlib.hash import pbkdf2_sha512 as pwd_hash

from isa2api.database import select
from isa2api.settings import RESTPLUS_SUPER_SECRET, RESTPLUS_TOKEN_EXPIRE

permissions = []


def loadPermissions():
    global permissions
    permissions = select(
        ' SELECT login,s.id as server,role,admin FROM (SELECT * FROM permissions p RIGHT JOIN users u ON u.login=p.user) AS u LEFT JOIN servers s ON u.service=s.service')


class Auth:

    """
    Auth business class
    """

    def __init__(self):
        self.s = Serializer(RESTPLUS_SUPER_SECRET,
                            RESTPLUS_TOKEN_EXPIRE)
        loadPermissions()

    def encode(self, user):
        return self.s.dumps(user).decode('utf-8')

    def whoIs(self):
        if request and request.headers:
            header = request.headers.get('X-API-KEY')
        token = header or request.args.get('token', None)
        return self.s.loads(token)

    def login(self, user):
        if user.username and user.password:
            p = {'login': user.username}
            res = select(
                'select login,password from users where login=%(login)s', p)
            if(len(res)):
                if(pwd_hash.verify(user.password, res[0].get("password"))):
                    return {'token': self.encode({"username": user.username})}
        return None

    def isAuthorised(
        self,
        user,
        server,
        write=False,
    ):
        found = next((item for item in permissions if item.get('login')
                      == user and item.get('admin')), None)
        if not found:
            if not server is None:
                found = next((item for item in permissions
                              if item.get('login') == user
                              and item.get('server') == int(server)
                              and (write is False or item.get('role')
                                   == 'manager')), None)
        return found != None

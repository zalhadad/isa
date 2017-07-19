from flask import request, make_response
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature, base64_decode, base64_encode
from functools import wraps

from isa2api.settings import RESTPLUS_API_PREFIX, RESTPLUS_SUPER_SECRET, RESTPLUS_TOKEN_EXPIRE
from isa2api.business.auth import Auth


s = Serializer(RESTPLUS_SUPER_SECRET, RESTPLUS_TOKEN_EXPIRE)
auth = Auth()


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not isAuthReq() and not isDoc():
            t = getToken()
            if t == None:
                return make_response('No token', 401)
            try:
                t = s.loads(t)
                user = t["username"]
                server = request.args.get("server", None)
                if(not (auth.isAuthorised(user, server, request.method != 'GET') or isMe())):
                    return make_response('Forbidden', 403)
            except SignatureExpired:
                # invalid token
                return make_response('Token signature expired', 401)
            except BadSignature:
                # valid token, but expired
                return make_response('Bad token signature', 401)

        return f(*args, **kwargs)

    return decorated


def getLevels():
    levels = list(filter(None, request.path.replace(
        RESTPLUS_API_PREFIX, "").split('/')))
    return {'size': len(levels), 'names': levels}


def isAuthReq():
    levels = getLevels()
    return request.method == 'POST' and levels["size"] == 1 and levels["names"][0] == 'auth'


def isMe():
    levels = getLevels()
    return request.method == 'GET' and levels["size"] == 1 and levels["names"][0] == 'auth'


def isDoc():
    levels = getLevels()
    return levels["size"] == 0 or levels["names"][0] == "swagger.json"


def getToken():
    if request and request.headers:
        header = request.headers.get('X-API-KEY')
    return header or request.args.get('token', None)

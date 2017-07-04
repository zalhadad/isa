from flask import request,make_response
from functools import wraps

from isa2api.settings import RESTPLUS_API_PREFIX
from isa2api.business.users import User

u = User()

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not isAuthReq() and not isDoc():
            t = u.decodeToken()
            if t == None:
                return make_response('No token',401)
            if t == 400:
                return make_response('Bad token signature',401)
            if t == 401:
                return make_response('Token signature expired',401)
        return f(*args, **kwargs)
        
    return decorated



def getLevels():
    levels = list(filter(None,request.path.replace(RESTPLUS_API_PREFIX,"").split('/')))
    return { 'size' : len(levels), 'names' : levels}




def isAuthReq():
    levels = getLevels()
    return request.method == 'POST' and levels["size"] == 2 and levels["names"][0] == 'users' and levels["names"][1] == 'authenticate'
def isDoc():
    levels = getLevels()
    return levels["size"] > 0  and (levels["names"][0] == 'doc' or  levels["names"][0] == "swagger.json")

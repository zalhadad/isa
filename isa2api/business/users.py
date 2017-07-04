from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,SignatureExpired,BadSignature,base64_decode,base64_encode
from flask import request
from isa2api.settings import RESTPLUS_SUPER_SECRET 
from isa2api.settings import RESTPLUS_TOKEN_EXPIRE 


class User:

    def __init__(self):
        self.s = Serializer(RESTPLUS_SUPER_SECRET,RESTPLUS_TOKEN_EXPIRE)
    
    def decodeToken(self):
        token = self.getToken()
        decoded = None
        if(token):
            try:
                decoded = self.s.loads(token)
            except SignatureExpired:
                decoded = 401 # valid token, but expired
            except BadSignature:
                decoded = 400 # invalid token
        return decoded

    def encode(self,user):
        return self.s.dumps(user).decode("utf-8")

    def getToken(self): 
        if request and request.headers:
            header = request.headers.get('X-API-KEY')
        return header  or request.args.get('token',None)
    
    def login(self,user):
        if( user.username == user.password ):
            del user["password"]
            return { 'token' : self.encode(user) } 
        return None
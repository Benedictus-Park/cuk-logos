import jwt
from functools import wraps
from flask_cors import CORS
from config import JWT_SECRET_KEY
from flask import Flask, request, g, Response

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("authorization")

        if token is None:
            return Response(status = 400)
        else:
            try:
                payload = jwt.decode(token, JWT_SECRET_KEY, 'HS256')
            except Exception:
                return Response(response="Invalid Token", staus=401)
            
            g.uid = payload['uid']
            g.username = payload['username']
            g.email = payload['email']
            g.is_manager = payload['is_manager']

        return f(*args, **kwargs)
    return wrapper

app = Flask(__name__)
CORS(app)
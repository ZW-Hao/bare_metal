# security.py
from flask import request, g
from functools import wraps
import jwt


def check_jwt_token(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1]

        if not token:
            return {"msg": "Missing Authorization Header"}, 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            g.user = data['sub']  # 存储用户信息（例如用户名）到 Flask 的全局对象 g 中
        except Exception as e:
            return {"msg": "Invalid token", "error": str(e)}, 401

        return f(*args, **kwargs)

    return wrapper
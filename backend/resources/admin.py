from flask import request
from flask_restx import Namespace, Resource, fields
from utils.jwt_utils import decode_token
from functools import wraps
from database import SessionLocal
from models import User
from passlib.hash import pbkdf2_sha256

admin_ns = Namespace("admin", description="Admin endpoints")

def require_role(role="superadmin"):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth = request.headers.get("Authorization")
            if not auth or not auth.startswith("Bearer "):
                return {"message":"Missing token"}, 401
            token = auth.split(" ")[1]
            try:
                payload = decode_token(token)
            except Exception:
                return {"message":"Invalid/expired token"}, 401
            if payload.get("role") != role:
                return {"message":"Forbidden"}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

@admin_ns.route("/users")
class ManageUsers(Resource):
    @require_role("superadmin")
    def get(self):
        session = SessionLocal()
        users = session.query(User).all()
        res = []
        for u in users:
            res.append({"id": u.id, "email": u.email, "first_name": u.first_name, "last_name": u.last_name, "role": u.role, "is_active": u.is_active})
        session.close()
        return {"users": res}

    @require_role("superadmin")
    def post(self):
        data = request.json
        session = SessionLocal()
        if session.query(User).filter_by(email=data["email"]).first():
            session.close()
            return {"message":"User already exists"}, 400
        hashed = pbkdf2_sha256.hash(data["password"])
        user = User(first_name=data.get("first_name"), last_name=data.get("last_name"),
                    email=data["email"], hashed_password=hashed, role=data.get("role", "user"), is_active=True)
        session.add(user)
        session.commit()
        session.close()
        return {"message":"User created"}, 201

@admin_ns.route("/users/<int:user_id>")
class SingleUser(Resource):
    @require_role("superadmin")
    def put(self, user_id):
        data = request.json
        session = SessionLocal()
        u = session.query(User).get(user_id)
        if not u:
            session.close()
            return {"message":"Not found"}, 404
        if "password" in data:
            u.hashed_password = pbkdf2_sha256.hash(data["password"])
        for key in ["first_name", "last_name", "role", "is_active", "mobile"]:
            if key in data:
                setattr(u, key, data[key])
        session.commit()
        session.close()
        return {"message":"Updated"}

    @require_role("superadmin")
    def delete(self, user_id):
        session = SessionLocal()
        u = session.query(User).get(user_id)
        if not u:
            session.close()
            return {"message":"Not found"}, 404
        session.delete(u)
        session.commit()
        session.close()
        return {"message":"Deleted"}

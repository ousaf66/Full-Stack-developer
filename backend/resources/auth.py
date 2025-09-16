from flask import request
from flask_restx import Namespace, Resource, fields
from database import SessionLocal
from models import User, OTP, RefreshToken
from passlib.hash import pbkdf2_sha256
from utils.email_utils import send_email
from utils.jwt_utils import create_access_token, create_refresh_token, decode_token
from datetime import datetime, timedelta
import random, string, os
from config import Config

auth_ns = Namespace("auth", description="Authentication endpoints")

register_model = auth_ns.model("Register", {
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
    "mobile": fields.String(required=False),
})

login_model = auth_ns.model("Login", {
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})

def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(register_model)
    def post(self):
        data = request.form.to_dict() or request.json or {}
        session = SessionLocal()
        email = data.get("email")
        if session.query(User).filter_by(email=email).first():
            session.close()
            return {"message":"User already exists"}, 400
        # handle file upload
        file = request.files.get("profile_pic")
        pic_path = None
        if file:
            filename = f"{int(datetime.utcnow().timestamp())}_{file.filename}"
            save_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(save_path)
            pic_path = filename

        hashed = pbkdf2_sha256.hash(data["password"])
        user = User(first_name=data.get("first_name"),
                    last_name=data.get("last_name"),
                    email=email,
                    hashed_password=hashed,
                    mobile=data.get("mobile"),
                    profile_pic=pic_path,
                    is_active=False)
        session.add(user)
        session.commit()

        # create OTP
        code = generate_otp()
        otp = OTP(email=email, otp_code=code, expires_at=datetime.utcnow()+timedelta(minutes=10))
        session.add(otp)
        session.commit()
        session.close()

        # send email
        body = f"<p>Your OTP for Galvan registration is <b>{code}</b>. It expires in 10 minutes.</p>"
        send_email("Galvan Registration OTP", body, email)
        return {"message":"Registered — OTP sent to email"}, 201

@auth_ns.route("/verify-otp")
class VerifyOTP(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        code = data.get("otp")
        session = SessionLocal()
        otp = session.query(OTP).filter_by(email=email, otp_code=code, used=False).first()
        if not otp or otp.expires_at < datetime.utcnow():
            session.close()
            return {"message":"Invalid or expired OTP"}, 400
        otp.used = True
        user = session.query(User).filter_by(email=email).first()
        user.is_active = True
        session.commit()
        session.close()
        return {"message":"OTP verified, account activated"}, 200

@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.json
        session = SessionLocal()
        user = session.query(User).filter_by(email=data["email"]).first()
        if not user:
            session.close()
            return {"message":"Invalid credentials"}, 401
        if not user.is_active:
            session.close()
            return {"message":"Account not activated — verify email OTP"}, 403
        if not pbkdf2_sha256.verify(data["password"], user.hashed_password):
            session.close()
            return {"message":"Invalid credentials"}, 401

        access = create_access_token({"sub": user.id, "email": user.email, "role": user.role})
        refresh = create_refresh_token({"sub": user.id})
        # Store refresh token in DB
        rt = RefreshToken(user_id=user.id, token=refresh, expires_at=datetime.utcnow()+timedelta(seconds=Config.REFRESH_EXPIRES_SECONDS))
        session.add(rt)
        session.commit()
        session.close()
        return {"access_token": access, "refresh_token": refresh, "user": {"email": user.email, "role": user.role}}, 200

@auth_ns.route("/refresh")
class Refresh(Resource):
    def post(self):
        data = request.json
        token = data.get("refresh_token")
        session = SessionLocal()
        try:
            payload = decode_token(token)
            if payload.get("type") != "refresh":
                raise Exception("Not a refresh token")
            # check DB token
            rt = session.query(RefreshToken).filter_by(token=token, revoked=False).first()
            if not rt or rt.expires_at < datetime.utcnow():
                session.close()
                return {"message":"Refresh token invalid or expired"}, 401
            user = session.query(User).filter_by(id=payload["sub"]).first()
            access = create_access_token({"sub": user.id, "email": user.email, "role": user.role})
            # rotate refresh token:
            session.delete(rt)
            new_refresh = create_refresh_token({"sub": user.id})
            rt_new = RefreshToken(user_id=user.id, token=new_refresh, expires_at=datetime.utcnow()+timedelta(seconds=Config.REFRESH_EXPIRES_SECONDS))
            session.add(rt_new)
            session.commit()
            session.close()
            return {"access_token": access, "refresh_token": new_refresh}
        except Exception as e:
            session.close()
            return {"message":"Invalid token"}, 401

@auth_ns.route("/forgot-password")
class ForgotPassword(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        session = SessionLocal()
        user = session.query(User).filter_by(email=email).first()
        if not user:
            session.close()
            return {"message":"If account exists, a reset link will be sent"}  # don't reveal
        token = create_access_token({"sub": user.id, "action": "reset-password", "email": user.email})
        reset_link = f"{Config.FRONTEND_URL}/reset-password?token={token}"
        body = f"<p>Click the link to reset password (valid 15 minutes): <a href='{reset_link}'>Reset password</a></p>"
        send_email("Galvan Password Reset", body, email)
        session.close()
        return {"message":"If account exists, a reset link will be sent"}

@auth_ns.route("/reset-password")
class ResetPassword(Resource):
    def post(self):
        data = request.json
        token = data.get("token")
        new_password = data.get("password")
        try:
            payload = decode_token(token)
            if payload.get("action") != "reset-password":
                return {"message":"Invalid token"}, 400
            user_id = payload.get("sub")
        except Exception:
            return {"message":"Invalid or expired token"}, 400
        session = SessionLocal()
        user = session.query(User).filter_by(id=user_id).first()
        user.hashed_password = pbkdf2_sha256.hash(new_password)
        session.commit()
        session.close()
        return {"message":"Password reset successful"}

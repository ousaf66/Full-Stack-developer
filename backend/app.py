from flask import Flask, send_from_directory
from flask_restx import Api
from flask_cors import CORS
from config import Config
from database import init_db
from resources.auth import auth_ns
from resources.admin import admin_ns
import database, os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, supports_credentials=True)
    api = Api(app, title="Galvan Auth API", version="1.0", description="Auth API for coding task")
    api.add_namespace(auth_ns, path="/api/auth")
    api.add_namespace(admin_ns, path="/api/admin")

    @app.route("/uploads/<path:filename>")
    def uploaded_file(filename):
        return send_from_directory(Config.UPLOAD_FOLDER, filename)
    return app

if __name__ == "__main__":
    init_db()
    # create superadmin if not exist
    from database import SessionLocal
    from models import User
    from passlib.hash import pbkdf2_sha256
    session = SessionLocal()
    sa = session.query(User).filter_by(email=Config.SUPERADMIN_EMAIL).first()
    if not sa:
        sa = User(email=Config.SUPERADMIN_EMAIL, first_name="Super", last_name="Admin",
                  hashed_password=pbkdf2_sha256.hash(Config.SUPERADMIN_PASSWORD),
                  is_active=True, role="superadmin")
        session.add(sa)
        session.commit()
        print("Created Super Admin:", Config.SUPERADMIN_EMAIL)
    session.close()
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

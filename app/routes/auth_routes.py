from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from app.models import User
from app.utils.security import hash_password, verify_password, create_jwt_token
from app.db import get_db
from app.schemas import RegisterSchema, LoginSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    db: Session = next(get_db())
    data = request.json

    try:
        # Validate request data
        errors = RegisterSchema().validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        # Check if the user already exists
        existing_user = db.query(User).filter_by(username=data["username"]).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 400

        # Create and save new user
        new_user = User(username=data["username"], password=hash_password(data["password"]))
        db.add(new_user)
        db.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except IntegrityError:
        db.rollback()  # Rollback in case of a database integrity issue
        return jsonify({"message": "Database integrity error. Possibly a duplicate entry."}), 400

    except SQLAlchemyError as e:
        db.rollback()  # Rollback for any other database-related error
        return jsonify({"message": "Database error", "error": str(e)}), 500

    except Exception as e:
        return jsonify({"message": "An unexpected error occurred", "error": str(e)}), 500

    finally:
        db.close()  # Ensure the session is closed


@auth_bp.route("/login", methods=["POST"])
def login():
    db: Session = next(get_db())
    data = request.json
    try:
        errors = LoginSchema().validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        user = db.query(User).filter_by(username=data["username"]).first()
        if not user or not verify_password(data["password"], user.password):
            return jsonify({"message": "Invalid credentials"}), 401
        
        access_token = create_jwt_token(str(user.id))
        return jsonify(access_token=access_token), 200
    except IntegrityError:
        db.rollback()  # Rollback in case of a database integrity issue
        return jsonify({"message": "Database integrity error. Possibly a duplicate entry."}), 400

    except SQLAlchemyError as e:
        db.rollback()  # Rollback for any other database-related error
        return jsonify({"message": "Database error", "error": str(e)}), 500

    except Exception as e:
        return jsonify({"message": "An unexpected error occurred", "error": str(e)}), 500

    finally:
        db.close()  # Ensure the session is closed
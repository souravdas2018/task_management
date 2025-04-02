from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from app.models import Task, TaskStatus
from app.db import get_db
from app.schemas import TaskSchema, TaskUpdateSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

task_bp = Blueprint("task", __name__)

@task_bp.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    data = request.get_json(silent=True)  # Safe parsing
    db: Session = next(get_db())
    try:
        if not data:
            return jsonify({"error": "Invalid JSON or missing body"}), 400

        errors = TaskSchema().validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        user_id = get_jwt_identity()

        new_task = Task(
            title=data["title"], 
            description=data.get("description"), 
            user_id=user_id
        )

        db.add(new_task)
        db.commit()

        return jsonify({
            "message": "Task created successfully",
            "task": TaskSchema().dump(new_task)
            }), 201
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

@task_bp.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    db: Session = next(get_db())
    user_id = get_jwt_identity()
    try:
        tasks = db.query(Task).filter_by(user_id=user_id).all()
        return jsonify(TaskSchema(many=True).dump(tasks)), 200
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

@task_bp.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task_by_id(task_id):
    db: Session = next(get_db())
    try:
        task = db.query(Task).filter_by(id=task_id).first()
        if not task:
            return jsonify({"message": "Task not found"}), 404

        return jsonify(TaskSchema().dump(task)), 200
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

@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    db: Session = next(get_db())
    data = request.json
    try:
        errors = TaskUpdateSchema().validate(data)
        if errors:
            return jsonify({"errors": errors}), 400

        task = db.query(Task).filter_by(id=task_id).first()
        if not task:
            return jsonify({"message": "Task not found"}), 404

        if "title" in data:
            task.title = data["title"]
        if "description" in data:
            task.description = data["description"]
        if "status" in data:
            task.status = data["status"]

        db.commit()
        return jsonify({
            "message": "Task updated successfully",
            "task": TaskSchema().dump(task)
        }), 200
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

@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    db: Session = next(get_db())
    try:
        task = db.query(Task).filter_by(id=task_id).first()
        if not task:
            return jsonify({"message": "Task not found"}), 404
        
        db.delete(task)
        db.commit()
        return jsonify({"message": "Task deleted"}), 200
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

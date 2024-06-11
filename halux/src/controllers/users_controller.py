from flask import Blueprint, request, jsonify
from utils import utils
from models.mqtt_logs import MqttLogs
from datetime import datetime
from models.db import db
from models.user import User
import utils.consts as consts

users = Blueprint(
    name="users",
    import_name=__name__,
    root_path="./",
    static_folder="./static/",
    template_folder="./templates/",
)


@users.route("/")
def users_route():
    utils.data["active_page"] = "users"
    users = db.session.query(User).all()
    return utils.render_template_if_admin("users.jinja", users=users)


@users.route("/new")
def user_device():
    utils.data["active_page"] = "users"
    return utils.render_template_if_admin("new_user.jinja")


@users.route("/<int:user_id>")
def edit_user_route(user_id):
    utils.data["active_page"] = "users"

    u = db.session.query(User).filter(User.user_id == user_id).first()
    if u is None:
        return redirect("/")

    return utils.render_template_if_admin("edit_user.jinja", user=u)


@users.route("/new_user", methods=["POST"])
def create_user():
    if request.json["username"] == "admin":
        return (
            jsonify({"status": "Cannot create a user with the username 'admin'"}),
            400,
        )

    u = User(
        role=request.json["role"],
        username=request.json["username"],
        password=request.json["password"],
    )
    db.session.add(u)
    db.session.flush()

    log = MqttLogs(
        created_at=datetime.now(),
        topic=consts.TOP_USER,
        subtopic=consts.CRUD,
        device_id=1,
        operation=consts.WRITE,
        payload=f"User ({u.user_id}) created",
    )
    db.session.add(log)

    db.session.commit()

    return jsonify({"status": "OK"})


@users.route("/edit_user", methods=["PUT"])
def edit_user():
    user_id = request.json["user_id"]
    username = request.json["username"]
    password = request.json["password"]

    u = db.session.query(User).filter(User.user_id == user_id).first()
    if u is None:
        return jsonify({"status": "User not found"}), 400

    log = MqttLogs(
        created_at=datetime.now(),
        topic=consts.TOP_USER,
        subtopic=consts.CRUD,
        device_id=1,
        operation=consts.WRITE,
        payload=f"User ({u.user_id}) updated",
    )

    u.username = username
    u.password = password

    db.session.add(log)
    db.session.commit()

    return jsonify({"status": "OK"})


@users.route("/delete_user", methods=["DELETE"])
def delete_user():
    user_id = request.json["user_id"]
    if user_id == 1:
        return jsonify({"status": "Cannot delete the admin user"}), 400

    log = MqttLogs(
        created_at=datetime.now(),
        topic=consts.TOP_USER,
        subtopic=consts.CRUD,
        device_id=1,
        operation=consts.DELETE,
        payload=f"User ({user_id}) deleted",
    )

    db.session.query(User).filter(User.user_id == user_id).delete()

    db.session.add(log)
    db.session.commit()

    if user_id == request.cookies["user_id"]:
        request.cookies.pop("user_id")

    return jsonify({"status": "OK"})

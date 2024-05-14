from flask import Blueprint, request, jsonify
from utils import utils
from models.fake_db import *

users = Blueprint(
    name="users",
    import_name=__name__,
    root_path="./",
    static_folder="./static/",
    template_folder="./templates/",
)


@users.route("/")
def users_route():
    return utils.render_template_if_admin("users.jinja", users=user)


@users.route("/new")
def user_device():
    utils.data["active_page"] = "users"
    return utils.render_template_if_admin("new_user.jinja")


@users.route("/new_user", methods=["POST"])
def create_user():
    username = request.json["username"]
    password = request.json["password"]

    user_id = len(user) + 1
    user.users.nd(
        dict(
            user_id=user_id,
            username=username,
            password=password,
            created_at=datetime.now(),
        )
    )

    return jsonify({"status": "OK"})


@users.route("/<int:user_id>")
def edit_user_route(user_id):
    utils.data["active_page"] = "users"

    u = None
    for u_db in user:
        if u_db["user_id"] == user_id:
            u = u_db
            break
    if u is None:
        return utils.render_template_if_admin("users.jinja")

    return utils.render_template_if_admin("edit_user.jinja", user=u)


@users.route("/edit_user", methods=["PUT"])
def edit_user():
    user_id = request.json["user_id"]

    username = request.json["username"]
    password = request.json["password"]

    u = None
    for u_db in user:
        if u_db["user_id"] == user_id:
            u = u_db
            break
    if u is None:
        return jsonify({"status": "User not found"}), 400

    u["username"] = username
    u["password"] = password

    return jsonify({"status": "OK"})


@users.route("/delete_user", methods=["DELETE"])
def delete_user():
    user_id = request.json["user_id"]
    if user_id == 1:
        return jsonify({"status": "Cannot delete the admin user"}), 400

    u = None
    for u_db in user:
        if u_db["user_id"] == user_id:
            u = u_db
            break
    if u is None:
        return jsonify({"status": "User not found"}), 400

    user.remove(u)
    if user_id == request.cookies["user_id"]:
        request.cookies.pop("user_id")

    return jsonify({"status": "OK"})

from typing import Any

from flask import request
from flask_restx import abort, Namespace, Resource, reqparse

from dao.tools.security import auth_required, ItemNotFound, admin_required, login_user
from implemented import user_service
from service.user import UsersService
from setup_db import db

users_ns = Namespace("users")
parser = reqparse.RequestParser()
parser.add_argument('page', type=int)


@users_ns.route("/")
class DirectorsView(Resource):
    @users_ns.expect(parser)
    @auth_required
    @users_ns.response(200, "OK")
    def get(self):
        """Get all users"""
        page = parser.parse_arg().get("page")
        if page:
            return UsersService(db.session).get_limit_users(page)
        else:
            return UsersService(db.session).get_all_users()


@users_ns.route("/<int:user_id>")
class UserView(Resource):
    @auth_required
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    def get(self, user_id: int):
        """Get director by id"""
        try:
            return UsersService(db.session).get_item_by_id(user_id)
        except ItemNotFound:
            abort(404, message="User not found")

    def post(self):
        req_json = request.json
        if not req_json:
            abort(400, message="Bad request")
        try:
            user = user_service.create(req_json)
            return "", 200
        except ItemNotFound:
            abort(404, message="Error, ошибка автоматизации")
    # def post(self):
    #     req_json = request.json
    #     if not req_json:
    #         abort(400, message="Bad request")
    #     try:
    #         user = UsersService(db.session).get_item_by_username(username=req_json.get("username"))
    #         tokens = login_user(request.json, user)
    #         return tokens, 200
    #     except ItemNotFound:
    #         abort(404, message="Error, ошибка автоматизации")

    """частичное изменение"""

    @admin_required
    def patch(self, user_id: int):
        req_json = request.json
        if not req_json:
            abort(400, message="Bad request")
        if not req_json('id'):
            req_json['id'] = id
        try:
            return UsersService(db.session).update(user_id)
        except ItemNotFound:
            abort(404, message="User not found")


class UserPatchView(Resource):
    @admin_required
    @users_ns.response(200, "OK")
    @users_ns.response(404, "User not found")
    def put(self, user_id: int):
        """частичное изменение"""
        req_json = request.json
        if not req_json:
            abort(400, message="Bad request")
        if not req_json('password'):
            req_json['password'] = 'password'
        try:
            return UsersService(db.session).update(req_json)
        except ItemNotFound:
            abort(404, message="User not found")

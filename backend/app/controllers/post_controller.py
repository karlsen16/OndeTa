from flask import request, jsonify
from app.services.post_service import PostService
from app.schemas.post_schema import FeedRequestSchema, PinsRequestSchema, PostResponseSchema, PinResponseSchema, PostCreateSchema
from app.controllers.auth_controller import AuthController

feed_schema = FeedRequestSchema()
pins_schema = PinsRequestSchema()
post_response = PostResponseSchema()
pins_response = PinResponseSchema(many=True)
post_create_schema = PostCreateSchema()


class PostController:
    @staticmethod
    def create_post():
        user = AuthController.authenticate_and_authorize(lean=True)
        data = post_create_schema.load(request.get_json())
        post = PostService.create_post(data, user.id)
        return jsonify(post_response.dump(post)), 201


    @staticmethod
    def get_feed():
        params = feed_schema.load(request.args)
        pagination_metadata, posts = PostService.get_feed(params)

        return jsonify({
            "posts": post_response.dump(posts, many=True),
            "meta": pagination_metadata
        }), 200


    @staticmethod
    def get_pins():
        params = pins_schema.load(request.args)
        pins = PostService.get_pins(params)
        return jsonify(pins_response.dump(pins)), 200


    @staticmethod
    def get_post(post_id, auth=False, admin=False):
        user = None
        if auth or admin:
            user = AuthController.authenticate_and_authorize(admin_required=admin, lean=True)
        post = PostService.get_post(post_id, user)
        return jsonify(post_response.dump(post)), 200

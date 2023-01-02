from flask import Blueprint, request, send_file
from flask_restful import Api, Resource
import logging

from services.image.logics.manager.image_manager import ImageManager

logging.basicConfig(filename='image_tagging.log', level=logging.DEBUG)

image_blueprint = Blueprint('image', __name__, url_prefix='/api/v1.0/image')
image_api = Api(image_blueprint)


class ImageController(Resource):
    """
    This controller acts as a RESTFul API endpoint for all actions corresponding to the document
    """
    def post(self):
        """
        This method receives the POST request and persists the document to the database
        :return: Success response
        """
        request_data = request.form.to_dict()
        file = request.files['file']
        tags = request_data.get('tags')
        username = request.headers.get('username')
        password = request.headers.get('password')
        user_id = ImageManager().check_user_auth(username, password)
        # TODO: request validation
        response = ImageManager().save_document(file, tags, user_id)
        logging.info("Request data is: %s, %s", str(tags), str(file))
        # TODO: handle different error responses
        return response

    def get(self, image_id):
        """
        This method receives the GET request and provides the document content back to requestor
        :param image_id: unique id of the image uploaded in database
        :return: document as byte object
        """
        username = request.headers.get('username')
        password = request.headers.get('password')
        # TODO: store password in db in secure manner - sha2 maybe
        ImageManager().check_user_auth(username, password)
        response = ImageManager().get_document(image_id)
        # TODO: store mime type in table and use it while sending the response
        return send_file(response['document_content'], mimetype='image/png')

    def delete(self, image_id):
        """
        This method receives the DELETE request and deletes all the details related to the corresponding image
        :param image_id: unique id of the image uploaded in database
        :return:
        """
        username = request.headers.get('username')
        password = request.headers.get('password')
        ImageManager().check_user_auth(username, password)
        response = ImageManager().delete_document(image_id)
        return response


image_api.add_resource(ImageController, '/', '/<string:image_id>')


class TagsController(Resource):
    """
    This controller acts as a RESTFul API endpoint for all actions corresponding to the document tags
    """
    def post(self, tag_name):
        """
        This method receives the POST request and adds the tag to the image
        :param tag_name: name of the image tag
        :return: success response
        """
        request_data = request.get_json()
        username = request.headers.get('username')
        password = request.headers.get('password')
        ImageManager().check_user_auth(username, password)
        response = ImageManager().update_tag(request_data['image_id'], tag_name)
        return response

    def get(self, tag_name):
        """
        This method get the list of images which are tagged under the given name
        :param tag_name: name of the image tag
        :return: list of unique document ids
        """
        request_data = request.get_json()
        username = request.headers.get('username')
        password = request.headers.get('password')
        ImageManager().check_user_auth(username, password)
        response = ImageManager().get_image_with_tag(tag_name, request_data['created_date'])
        # TODO: have logic for pagination if the result set is huge
        return response

    def delete(self, tag_name):
        """
        This method deletes the tag which is updated
        :param tag_name: name of the tag
        :return: success response
        """
        request_data = request.get_json()
        username = request.headers.get('username')
        password = request.headers.get('password')
        ImageManager().check_user_auth(username, password)
        response = ImageManager().delete_tag(request_data['image_id'], tag_name)
        return response


image_api.add_resource(TagsController, '/tag/', '/tag/<string:tag_name>')

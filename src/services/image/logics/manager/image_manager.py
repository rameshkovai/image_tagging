import uuid

from services.image.custom_exceptions import AccessDenied, ResourceDoesNotExist
from services.image.models.image_dao import ImageDao
from services.image.logics.entity.document_entity import Document


class ImageManager:
    """
    This class exposes all the methods required for the controller and helps with the data needed for Data Access
    Objects(DAO)
    """
    def __init__(self):
        self.dao_obj = ImageDao()
        self.document_obj = Document()

    def __extract_document_metadata(self, file):
        """
        This private method is called to extract metadata from document
        :param file: document object
        """
        self.document_obj.document_content = file.stream.read()
        self.document_obj.document_name = file.filename
        self.document_obj.document_type = file.filename.split('.')[-1]
        self.document_obj.document_size = len(self.document_obj.document_content)

    def check_user_auth(self, username, password):
        """
        This method checks the user authentication and returns the user_id in case auth is successful
        :param username: username of the client
        :param password: password of the client
        :return: user_id
        """
        user_id = self.dao_obj.check_user(username, password)
        if not user_id:
            raise AccessDenied()
        return user_id[0]['user_id']

    def save_document(self, file, tags, user_id):
        """
        This method calls the required methods to get the data needed to store the document to database
        :param file: file object
        :param tags: name of the image tag
        :param user_id: user_id
        :return: success/failure response
        """
        try:
            self.document_obj.unique_document_id = str(uuid.uuid4())
            self.document_obj.uploaded_by = user_id
            self.__extract_document_metadata(file)
            self.dao_obj.save_document_info(self.document_obj)
            self.dao_obj.save_document_attributes(self.document_obj)
            if tags:
                self.dao_obj.save_document_tag(self.document_obj, tags)
            self.dao_obj.mysql_conn.commit()
            return {'response': "200 OK"}
        except Exception:
            raise
        finally:
            self.dao_obj.mysql_conn.close()

    def __get_document_details(self, unique_document_id):
        """
        This private method get the document details from backend and store the details in the entity object
        :param unique_document_id: unique id for the document
        """
        document_details = self.dao_obj.get_document_info(unique_document_id)
        for key, value in document_details.items():
            setattr(self.document_obj, key, value)

    def get_document(self, unique_document_id):
        """
        This method is called to get the document content
        :param unique_document_id: unique id for the document
        :return: document content as bytes
        """
        doc_content = self.dao_obj.get_document(unique_document_id)
        if not doc_content:
            raise ResourceDoesNotExist()
        return {'document_content': (doc_content[0]['document_content'])}

    def delete_document(self, unique_document_id):
        """
        This method is called to gather the details required and delete all the image related information in database
        :param unique_document_id: unique id for the document
        :return: success/failure response
        """
        try:
            self.__get_document_details(unique_document_id)
            self.dao_obj.delete_document_tag(self.document_obj)
            self.dao_obj.delete_document_attributes(self.document_obj)
            self.dao_obj.delete_document_info(self.document_obj)
            self.dao_obj.mysql_conn.commit()
            return {'response': "200 OK"}
        except Exception:
            raise
        finally:
            self.dao_obj.mysql_conn.close()

    def update_tag(self, unique_document_id, tag_name):
        """
        This method is called to update the tag for existing image
        :param unique_document_id: unique id for the document
        :param tag_name: name of the image tag
        :return: success/failure response
        """
        try:
            result = self.dao_obj.get_document(unique_document_id)
            if result:
                self.dao_obj.save_document_tag(unique_document_id, tag_name)
            self.dao_obj.mysql_conn.commit()
            return {'response': "200 OK"}
        except Exception:
            raise
        finally:
            self.dao_obj.mysql_conn.close()

    def delete_tag(self, unique_document_id, tag_name):
        """
        This method is called to delete the document tag
        :param unique_document_id: unique id of the document
        :param tag_name: name of the image tag
        :return: success/failure response
        """
        try:
            result = self.dao_obj.get_document(unique_document_id)
            if result:
                self.dao_obj.delete_document_tag_details_by_tag(unique_document_id, tag_name)
            self.dao_obj.mysql_conn.commit()
            return {'response': "200 OK"}
        except Exception:
            raise
        finally:
            self.dao_obj.mysql_conn.close()

    def get_image_with_tag(self, tag_name, date=None):
        """
        This method is called to get all the images which has matching tag and it also works based on additional input
         based on date
        :param tag_name: name of the image tag
        :param date: tag created date
        :return: list of unique id of documents
        """
        try:
            result = self.dao_obj.get_document_by_tag_name(tag_name, date)
            document_details = [doc_id['unique_document_id'] for doc_id in result]
            return {'response': document_details}
        except Exception:
            raise
        finally:
            self.dao_obj.mysql_conn.close()


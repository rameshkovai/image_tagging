from services.image.config.config import MYSQL_USERNAME, MYSQL_HOST, MYSQL_DATABASE, MYSQL_PASSWORD
from services.image.logics.utils.MysqlConnector import MysqlConnector


class ImageDao:
    """
    This class acts as a Data Access Object which will interact directly with the database connector
    """
    def __init__(self):
        self.mysql_conn = MysqlConnector(MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE)

    def save_document_info(self, document_obj):
        """
        This method inserts the records to document table
        :param document_obj: document entity object
        """
        query = "insert into document (unique_document_id, document_content) values (%s, %s)"
        args = (document_obj.unique_document_id, document_obj.document_content)
        document_obj.document_id = self.mysql_conn.process_query(query, args, get_primary_key=True)

    def save_document_attributes(self, document_obj):
        """
        This method inserts the record into document_attributes table
        :param document_obj: document entity object
        """
        query = "insert into document_attributes (document_id, document_name, uploaded_by, document_type, " \
                "document_size, uploaded_date) values (%s, %s, %s, %s, %s, now())"
        args = (document_obj.document_id, document_obj.document_name, document_obj.uploaded_by,
                document_obj.document_type, document_obj.document_size)
        self.mysql_conn.process_query(query, args, get_primary_key=True)

    def save_document_tag(self, unique_document_id, tag_name):
        """
        This method inserts the record into document_tag table
        :param unique_document_id: unique id of the document
        :param tag_name: name of the image tag
        """
        query = "insert into document_tag (unique_document_id, tag_name, created_datetime) values (%s, %s, now())"
        args = (unique_document_id, tag_name)
        self.mysql_conn.process_query(query, args, get_primary_key=True)

    def check_user(self, username, password):
        """
        This method checks if the username and password are valid and return the matching user_id
        :param username: username
        :param password: password
        :return: user_id
        """
        query = "select user_id from user where username=%s and password=%s and is_valid=1"
        args = (username, password)
        result = self.mysql_conn.process_query(query, args)
        return result

    def delete_document_tag_details_by_tag(self, unique_document_id, tag_name):
        """
        This method is called to delete the tags updated for an image
        :param unique_document_id: unique id for the document
        :param tag_name: name of the image tag
        """
        query = "delete from document_tag where unique_document_id=%s and tag_name=%s"
        args = (unique_document_id, tag_name)
        self.mysql_conn.process_query(query, args, get_primary_key=True)

    def delete_document_tag(self, document_obj):
        """
        This method is called to delete the entries in document_tag table
        :param document_obj: document entity object
        """
        query = "delete from document_tag where unique_document_id=%s"
        args = (document_obj.unique_document_id,)
        self.mysql_conn.process_query(query, args, get_primary_key=True)

    def delete_document_info(self, document_obj):
        """
        This method is called to delete the entries in document table
        :param document_obj: document entity object
        """
        query = "delete from document where document_id= %s"
        args = (document_obj.document_id,)
        self.mysql_conn.process_query(query, args, get_primary_key=True)

    def delete_document_attributes(self, document_obj):
        """
        This method deletes the entries from document_attributes table
        :param document_obj: document entity object
        """
        query = "delete from document_attributes where document_id= %s"
        args = (document_obj.document_id,)
        self.mysql_conn.process_query(query, args, get_primary_key=True)

    def get_document_info(self, unique_document_id):
        """
        This method provides all the information related the document and its metadata
        :param unique_document_id: unique id for the document
        :return: document details
        """
        query = "select * from document where unique_document_id= %s"
        args = (unique_document_id,)
        result = self.mysql_conn.process_query(query, args)
        if result:
            query = "select * from document_attributes where document_id=%s"
            args = (result[0]['document_id'],)
            attributes_result = self.mysql_conn.process_query(query, args)
            result[0].update(attributes_result[0])
        return result[0]

    def get_document_by_tag_name(self, tag_name, created_date=None):
        """
        This method provides the details of images matching tag and created_date
        :param tag_name: name of the image tag
        :param created_date: tag created date
        :return: matching image unique id
        """
        query = "select distinct unique_document_id from document_tag where tag_name= %s"
        args = [tag_name, ]
        if created_date:
            query += " and date(created_datetime)=%s"
            args += [created_date, ]
        result = self.mysql_conn.process_query(query, args)
        return result

    def get_document(self, unique_document_id):
        """
        This method retrieves the document related information from database
        :param unique_document_id: unique id for the document
        :return: document information
        """
        query = "select * from document where unique_document_id= %s"
        args = (unique_document_id,)
        result = self.mysql_conn.process_query(query, args)
        return result

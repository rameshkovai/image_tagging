from services.image.config.config import IMAGE_EXTENSIONS


class Document:
    """
    This acts as an entity where we will keep the validations at code level and transformations before hitting the
    database
    """
    def __init__(self):
        self.__document_id = None
        self.__unique_document_id = None
        self.__document_content = None
        self.__document_name = None
        self.__document_size = None
        self.__document_type = None
        self.__uploaded_by = None

    @property
    def document_id(self):
        return self.__document_id

    @document_id.setter
    def document_id(self, value):
        self.__document_id = value

    @property
    def unique_document_id(self):
        return self.__unique_document_id

    @unique_document_id.setter
    def unique_document_id(self, value):
        self.__unique_document_id = value

    @property
    def document_content(self):
        return self.__document_content

    @document_content.setter
    def document_content(self, value):
        self.__document_content = value

    @property
    def document_name(self):
        return self.__document_name

    @document_name.setter
    def document_name(self, value):
        self.__document_name = value

    @property
    def document_size(self):
        return self.__document_size

    @document_size.setter
    def document_size(self, value):
        self.__document_size = value

    @property
    def document_type(self):
        return self.__document_type

    @document_type.setter
    def document_type(self, value):
        self.__document_type = 'unknown'
        if value in IMAGE_EXTENSIONS:
            self.__document_type = 'image'

    @property
    def uploaded_by(self):
        return self.__uploaded_by

    @uploaded_by.setter
    def uploaded_by(self, value):
        self.__uploaded_by = value

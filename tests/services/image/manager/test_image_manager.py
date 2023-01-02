import pytest
from _pytest.monkeypatch import MonkeyPatch

from services.image.custom_exceptions import AccessDenied, ResourceDoesNotExist
from services.image.models.image_dao import ImageDao
from services.image.logics.manager.image_manager import ImageManager
from services.image.logics.utils.MysqlConnector import MysqlConnector


class TestImageManager:
    def test_check_user_auth(self, monkeypatch):
        def mock_check_user(self, username, password):
            return [{'user_id': 1}]
        monkeypatch.setattr(ImageDao, 'check_user', mock_check_user)
        assert ImageManager().check_user_auth('testuser', 'testpass') == 1

    def test_check_user_auth_access_denied(self, monkeypatch):
        def mock_check_user(self, username, password):
            return []
        monkeypatch.setattr(ImageDao, 'check_user', mock_check_user)
        with pytest.raises(AccessDenied) as ex:
            ImageManager().check_user_auth('testuser', 'testpass')

    def test_get_document(self, monkeypatch):
        def mock_get_document(self, unique_document_id):
            return [{'document_content': b'xyz'}]
        monkeypatch.setattr(ImageDao, 'get_document', mock_get_document)
        assert ImageManager().get_document('12344') == {'document_content': b'xyz'}

    def test_get_document_does_not_exist(self, monkeypatch):
        def mock_get_document(self, unique_document_id):
            return []
        monkeypatch.setattr(ImageDao, 'get_document', mock_get_document)
        with pytest.raises(ResourceDoesNotExist) as ex:
            ImageManager().get_document('12344')

    def test_delete_document(self, monkeypatch):
        def mock_get_document_info(self, unique_document_id):
            return {'document_id': 1, 'unique_document_id': unique_document_id}
        monkeypatch.setattr(ImageDao, 'get_document_info', mock_get_document_info)

        def mock_delete_document_tag(self, document_obj):
            pass
        monkeypatch.setattr(ImageDao, 'delete_document_tag', mock_delete_document_tag)

        def mock_delete_document_attributes(self, document_obj):
            pass
        monkeypatch.setattr(ImageDao, 'delete_document_attributes', mock_delete_document_attributes)

        def mock_delete_document_info(self, document_obj):
            pass
        monkeypatch.setattr(ImageDao, 'delete_document_info', mock_delete_document_info)

        def mock_commit(self):
            pass
        monkeypatch.setattr(MysqlConnector, 'commit', mock_commit)

        def mock_close(self):
            pass
        monkeypatch.setattr(MysqlConnector, 'close', mock_close)
        assert ImageManager().delete_document('12345') == {'response': "200 OK"}

import uuid

from services.image.logics.entity.document_entity import Document


class TestDocument:
    def test_document_entity(self):
        doc_obj = Document()
        doc_obj.document_id = 1
        assert doc_obj.document_id == 1
        unique_id = str(uuid.uuid4())
        doc_obj.unique_document_id = unique_id
        assert doc_obj.unique_document_id == unique_id
        content = b'xyz'
        doc_obj.document_content = content
        assert doc_obj.document_content == content
        doc_obj.document_size = 123
        assert doc_obj.document_size == 123
        doc_obj.document_type = 'jpg'
        assert doc_obj.document_type == 'image'
        doc_obj.document_type = 'pdf'
        assert doc_obj.document_type == 'unknown'
        doc_obj.uploaded_by = 1
        assert doc_obj.uploaded_by == 1
        doc_obj.document_name = 'test.jpg'
        assert doc_obj.document_name == 'test.jpg'

import json

from genai_stack.genai_platform.services.base_service import BaseService
from genai_stack.genai_server.models.vectordb_models import (
    DocumentType, RetrieverAddDocumentsRequestModel, RetrieverSearchRequestModel, RetrieverAddDocumentsResponseModel,
    RetrieverSearchResponseModel
)
from genai_stack.genai_server.utils import get_current_stack


class VectorDBService(BaseService):

    def add_documents(self, request: RetrieverAddDocumentsRequestModel) -> RetrieverAddDocumentsResponseModel:
        """
        This method adds the documents to the vector database.

            Args
                session_id : int
                documents : List[DocumentType]

            Returns
                bool
        """
        file = open("genai_stack/genai_server/stack_config.json", "r")
        config = json.loads(file.read())
        file.close()
        stack = get_current_stack(
            stack_id=request.stack_id,
            session_id=request.session_id,
            session_indexes={},
            config=config
        )
        stack.vector_db.add_documents(request.documents)
        return RetrieverAddDocumentsResponseModel(documents=[
            DocumentType(
                page_content=document['page_content'],
                metadata=document['metadata']
            ) for document in request.documents
        ])

    def search(self, request: RetrieverSearchRequestModel) -> RetrieverSearchResponseModel:
        """
        This method searches the documents from the vector database.

            Args
                session_id : int
                query : str

            Returns
                documents : List[DocumentType]
        """
        file = open("genai_stack/genai_server/config.json", "r")
        config = json.loads(file.read())
        file.close()
        stack = get_current_stack(
            stack_id=request.stack_id,
            session_id=request.session_id,
            session_indexes={},
            config=config
        )
        documents = stack.vector_db.search(request.query)
        return RetrieverSearchResponseModel(documents=[
            DocumentType(
                page_content=document['page_content'],
                metadata=document['metadata']
            ) for document in documents
        ])

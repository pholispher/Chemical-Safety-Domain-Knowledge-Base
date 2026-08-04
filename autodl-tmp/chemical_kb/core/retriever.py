#组合Retriever
from core.embedding import EmbeddingModel
from core.vector_store import VectorStore
from core.reranker import Reranker



class Retriever:


    def __init__(self):

        self.embedding=EmbeddingModel()

        self.vector_store=VectorStore()

        self.reranker=Reranker()



    def query(
        self,
        question
    ):


        vector=self.embedding.encode(
            question
        )


        docs=self.vector_store.search(
            vector
        )


        results=self.reranker.rerank(
            question,
            docs
        )


        return results
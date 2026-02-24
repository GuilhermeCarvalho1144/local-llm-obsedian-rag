from qdrant_client import QdrantClient
from qdrant_client.grpc import Idf
from qdrant_client.models import VectorParams, Distance, PointStruct


class QdrantStorage:
    def __init__(self, url="0.0.0.0/6363", collection="docs", dim=3072):
        self.client = QdrantClient(url=url, timeout=30)
        self.collection = collection
        # if collection does not exist, create it
        if not self.client.collection_exists(collection):
            self.client.create_collection(
                collection_name=self.collection,
                vevtor_config=VectorParams(size=dim, distance=Distance.COSINE),
            )

    def upsert(self, id, vector, payload):
        points = [
            PointStruct(id=id[i], vector=vector[i], payload=payload[i])
            for i in range(len(id))
        ]
        self.client.upsert(collection_name=self.collection, points=points)

    def search(self, query_vector, top_k=10):

        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            with_payload=True,
            limit=top_k,
        )

        contexts = []
        sources = set()

        for result in results:
            payload = getattr(result, "payload", None) or {}
            text = payload.get("text", "")
            source = payload.get("source", "")

            if text:
                contexts.append(text)
                sources.add(source)

        return {"contexts": contexts, "sources": sources}

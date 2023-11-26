# mongodb.py
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.collection import Collection
from pymongo.results import UpdateResult, DeleteResult
from typing import Dict, Any, Optional

mongo_uri = os.environ.get("MONGO_URI")

client = MongoClient(
    mongo_uri,
    server_api=ServerApi("1"),
    ssl=True,
    tls=True,
    tlsAllowInvalidCertificates=True,
)
db = client.shortsSniper


class MongoDBClientService:
    def __init__(
        self,
        database_name: str = "shortsSniper",
        collection_name: str = "videoTranscriptions",
    ):
        self.client: MongoClient = MongoClient(
            mongo_uri,
            server_api=ServerApi("1"),
            ssl=True,
            tls=True,
            tlsAllowInvalidCertificates=True,
        )
        try:
            client.admin.command("ping")
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        self.database_name: str = database_name
        self.collection_name: str = collection_name
        self._create_database_if_not_exists()
        self._create_collection_if_not_exists()

    def _create_database_if_not_exists(self) -> None:
        """Create the database if it does not exist."""
        if self.database_name not in self.client.list_database_names():
            self.client[self.database_name]  # type: Database
            print(f"Database '{self.database_name}' created.")

    def _create_collection_if_not_exists(self) -> None:
        """Create the collection if it does not exist."""
        if (
            self.collection_name
            not in self.client[self.database_name].list_collection_names()
        ):
            self.client[self.database_name][self.collection_name]  # type: Collection
            print(f"Collection '{self.collection_name}' created.")

        self.collection: Collection = self.client[self.database_name][
            self.collection_name
        ]

    def insert_document(
        self, document: Dict[str, Any], document_id: Optional[Any] = None
    ) -> Optional[Any]:
        """Insert a document into the collection or update if it already exists."""
        if document_id is not None:
            document["_id"] = document_id
        result: UpdateResult = self.collection.replace_one(
            {"_id": document_id}, document, upsert=True
        )
        return result.upserted_id

    def find_document(self, document_id: Any) -> Optional[Dict[str, Any]]:
        """Find a document in the collection based on the document ID."""
        result: Optional[Dict[str, Any]] = self.collection.find_one(
            {"_id": document_id}
        )
        return result

    def update_document(self, document_id: Any, update: Dict[str, Any]) -> int:
        """Update a document in the collection based on the document ID."""
        result: UpdateResult = self.collection.update_one(
            {"_id": document_id}, {"$set": update}
        )
        return result.modified_count

    def delete_document(self, document_id: Any) -> int:
        """Delete a document from the collection based on the document ID."""
        result: DeleteResult = self.collection.delete_one({"_id": document_id})
        return result.deleted_count

    def close_connection(self) -> None:
        """Close the MongoDB connection."""
        self.client.close()

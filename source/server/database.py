import os

from dotenv import load_dotenv
from fastapi import UploadFile
from gridfs import GridFS
from pymongo import ASCENDING, MongoClient

load_dotenv()


class Database:
    client = MongoClient(os.getenv("DB_URI"))
    database = client["development"]
    fileSystem = GridFS(database)

    def getCollection(self, collection: str):
        return self.database[collection]

    def createCollection(self) -> None:
        user = self.getCollection("user")
        user.create_index([("username", ASCENDING)], unique=True)
        user.create_index([("email", ASCENDING)], unique=True)

        dependency = self.getCollection("dependency")
        dependency.insert_one({"_id": 1, "userIncrement": 0, "documentIncrement": 0})

    def dropCollection(self) -> None:
        self.getCollection("user").drop()
        self.getCollection("document").drop()
        self.getCollection("dependency").drop()

    def resetCollection(self) -> None:
        self.dropCollection()
        self.createCollection()

    def newId(self, collection: str) -> int:
        dependency = self.getCollection("dependency")

        documentObject = dependency.find_one({"_id": 1}, {f"{collection}Increment": 1})
        documentObject[f"{collection}Increment"] += 1

        dependency.update_one(
            {"_id": 1},
            {
                "$set": {
                    f"{collection}Increment": documentObject[f"{collection}Increment"]
                }
            },
        )

        return documentObject[f"{collection}Increment"]

    def fileSystemInsert(self, file: UploadFile):
        return str(self.fileSystem.put(file.file, filename=file.filename))


# Database().resetCollection()

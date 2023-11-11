import datetime
import os

from bson import ObjectId
from dotenv import load_dotenv
from fastapi import UploadFile
from gridfs import GridFS, GridOut
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

        user.insert_many(
            [
                {
                    "_id": index,
                    "name": f"admin{index}",
                    "username": f"admin{index}",
                    "email": f"admin{index}@gmail.com",
                    "password": "$2a$12$KM2bHq3QeQ7K018L/5YRBumFQgVIyk7iSyhvN11qw1HwTgVTGRN3K",
                    "role": "admin",
                    "isActive": True,
                    "createdAt": datetime.datetime.now(),
                    "updatedAt": datetime.datetime.now(),
                }
                for index in range(1, 4)
            ]
            + [
                {
                    "_id": index + 3,
                    "name": f"user{index}",
                    "username": f"user{index}",
                    "email": f"user{index}@gmail.com",
                    "password": "$2a$12$KM2bHq3QeQ7K018L/5YRBumFQgVIyk7iSyhvN11qw1HwTgVTGRN3K",
                    "role": "user",
                    "isActive": True,
                    "createdAt": datetime.datetime.now(),
                    "updatedAt": datetime.datetime.now(),
                }
                for index in range(1, 4)
            ]
        )

        dependency = self.getCollection("dependency")
        dependency.insert_one(
            {
                "_id": 1,
                "userIncrement": 6,
                "documentIncrement": 0,
                "accessIncrement": 0,
            }
        )

    def dropCollection(self) -> None:
        self.getCollection("user").drop()
        self.getCollection("document").drop()
        self.getCollection("access").drop()
        self.getCollection("fs.chunks").drop()
        self.getCollection("fs.files").drop()
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

    def fileSystemInsert(self, file: UploadFile) -> str:
        return str(self.fileSystem.put(file.file, filename=file.filename))

    def fileSystemFind(self, id: str) -> GridOut:
        return self.fileSystem.get(ObjectId(id))


# Database().resetCollection()

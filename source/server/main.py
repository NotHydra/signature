import datetime
from io import BytesIO

from click import File
from database import Database
from fastapi import FastAPI, Form, Response, UploadFile, status
from fastapi.responses import StreamingResponse
from model.access import AccessAddModel, AccessPageModel
from model.auth import AuthLoginModel
from model.document import DocumentPageModel
from model.user import (
    UserAddModel,
    UserChangeModel,
    UserChangePasswordModel,
    UserPageModel,
)
from utility import Utility

app = FastAPI()
database = Database()


@app.post("/api/auth/login")
def auth(response: Response, body: AuthLoginModel):
    try:
        userCollection = database.getCollection("user")
        userObject = userCollection.find_one(
            {"username": body.username}, {"_id": 1, "password": 1}
        )

        if userObject != None:
            if Utility.decrypt(body.password, userObject["password"]):
                response.status_code = status.HTTP_202_ACCEPTED

                return Utility.formatResponse(
                    True,
                    response.status_code,
                    "Login Successful",
                    {"_id": userObject["_id"]},
                )

            else:
                response.status_code = status.HTTP_404_NOT_FOUND

                return Utility.formatResponse(
                    False, response.status_code, "Username or Password Incorrect", None
                )

        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False, response.status_code, "Username or Password Incorrect", None
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/user")
def user(response: Response, body: UserPageModel):
    try:
        userArray = list(
            database.getCollection("user")
            .find()
            .skip(body.count * (body.page - 1))
            .limit(body.count)
            if body.count != 0 and body.page != 0
            else database.getCollection("user").find()
        )

        if len(userArray) > 0:
            response.status_code = status.HTTP_200_OK

            return Utility.formatResponse(
                True, response.status_code, "User Found", userArray
            )

        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False, response.status_code, "User Not Found", None
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/user/count")
def userCount(response: Response):
    try:
        response.status_code = status.HTTP_200_OK

        userCollection = database.getCollection("user")
        return Utility.formatResponse(
            True,
            response.status_code,
            "User Count",
            {
                "total": userCollection.count_documents({}),
                "user": userCollection.count_documents({"role": "user"}),
                "admin": userCollection.count_documents({"role": "admin"}),
            },
        )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/user/{id}")
def userFind(response: Response, id: int):
    try:
        userObject = database.getCollection("user").find_one({"_id": id})

        if userObject != None:
            response.status_code = status.HTTP_200_OK

            return Utility.formatResponse(
                True, response.status_code, "User Found", userObject
            )

        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False,
                response.status_code,
                "User Not Found",
                None,
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.post("/api/user/add")
def userAdd(response: Response, body: UserAddModel):
    try:
        if Utility.checkEmail(body.email):
            if len(body.password) >= 8:
                if body.role in ["user", "admin"]:
                    userCollection = database.getCollection("user")
                    newUserObject = {
                        "_id": database.newId("user"),
                        "name": body.name,
                        "username": body.username,
                        "email": body.email,
                        "password": Utility.encrypt(body.password),
                        "role": body.role,
                        "is_active": body.is_active,
                        "created_at": datetime.datetime.now(),
                        "updated_at": datetime.datetime.now(),
                    }
                    insertedUserObject = userCollection.insert_one(newUserObject)

                    if insertedUserObject != None:
                        response.status_code = status.HTTP_201_CREATED

                        return Utility.formatResponse(
                            True, response.status_code, "User Added", newUserObject
                        )

                    else:
                        response.status_code = status.HTTP_400_BAD_REQUEST

                        return Utility.formatResponse(
                            False,
                            response.status_code,
                            "User Failed To Be Added",
                            None,
                        )

                else:
                    response.status_code = status.HTTP_400_BAD_REQUEST

                    return Utility.formatResponse(
                        False,
                        response.status_code,
                        "User Role Needs To Be User or Admin",
                        None,
                    )

            else:
                response.status_code = status.HTTP_400_BAD_REQUEST

                return Utility.formatResponse(
                    False,
                    response.status_code,
                    "User Password Needs To Be Atleast 8 Characters Long",
                    None,
                )

        else:
            response.status_code = status.HTTP_400_BAD_REQUEST

            return Utility.formatResponse(
                False,
                response.status_code,
                "User Email Format Is Incorrect",
                None,
            )

    except Exception as e:
        errorMessage = str(e)
        if "E11000 duplicate key error collection" in errorMessage:
            response.status_code = status.HTTP_400_BAD_REQUEST

            if "username" in errorMessage:
                return Utility.formatResponse(
                    False, response.status_code, "Username Already Used", None
                )

            elif "email" in errorMessage:
                return Utility.formatResponse(
                    False, response.status_code, "Email Already Used", None
                )

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.put("/api/user/change/{id}")
def userChange(response: Response, id: int, body: UserChangeModel):
    try:
        if Utility.checkEmail(body.email):
            if body.role in ["user", "admin"]:
                userCollection = database.getCollection("user")
                userObject = userCollection.find_one({"_id": id})

                if userObject != None:
                    updatedUserObject = userCollection.update_one(
                        {"_id": id},
                        {
                            "$set": {
                                "name": body.name,
                                "username": body.username,
                                "email": body.email,
                                "role": body.role,
                                "updated_at": datetime.datetime.now(),
                            }
                        },
                    )

                    if updatedUserObject != None:
                        response.status_code = status.HTTP_202_ACCEPTED

                        return Utility.formatResponse(
                            True,
                            response.status_code,
                            "User Changed",
                            userCollection.find_one({"_id": id}),
                        )

                    else:
                        response.status_code = status.HTTP_400_BAD_REQUEST

                        return Utility.formatResponse(
                            False,
                            response.status_code,
                            "User Failed To Be Changed",
                            None,
                        )

                else:
                    response.status_code = status.HTTP_404_NOT_FOUND

                    return Utility.formatResponse(
                        False, response.status_code, "User Not Found", None
                    )

            else:
                response.status_code = status.HTTP_400_BAD_REQUEST

                return Utility.formatResponse(
                    False,
                    response.status_code,
                    "User Role Needs To Be User or Admin",
                    None,
                )

        else:
            response.status_code = status.HTTP_400_BAD_REQUEST

            return Utility.formatResponse(
                False,
                response.status_code,
                "User Email Format Is Incorrect",
                None,
            )

    except Exception as e:
        errorMessage = str(e)
        if "E11000 duplicate key error collection" in errorMessage:
            response.status_code = status.HTTP_400_BAD_REQUEST

            if "username" in errorMessage:
                return Utility.formatResponse(
                    False, response.status_code, "Username Already Used", None
                )

            elif "email" in errorMessage:
                return Utility.formatResponse(
                    False, response.status_code, "Email Already Used", None
                )

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.put("/api/user/change-password/{id}")
def userChangePassword(response: Response, id: int, body: UserChangePasswordModel):
    try:
        if len(body.password) >= 8:
            userCollection = database.getCollection("user")
            userObject = userCollection.find_one({"_id": id})

            if userObject != None:
                updatedUserObject = userCollection.update_one(
                    {"_id": id},
                    {
                        "$set": {
                            "password": Utility.encrypt(body.password),
                            "updated_at": datetime.datetime.now(),
                        }
                    },
                )

                if updatedUserObject != None:
                    response.status_code = status.HTTP_202_ACCEPTED

                    return Utility.formatResponse(
                        True,
                        response.status_code,
                        "User Password Changed",
                        userCollection.find_one({"_id": id}),
                    )

                else:
                    response.status_code = status.HTTP_400_BAD_REQUEST

                    return Utility.formatResponse(
                        False,
                        response.status_code,
                        "User Password Failed To Be Changed",
                        None,
                    )

            else:
                response.status_code = status.HTTP_404_NOT_FOUND

                return Utility.formatResponse(
                    False, response.status_code, "User Not Found", None
                )

        else:
            response.status_code = status.HTTP_400_BAD_REQUEST

            return Utility.formatResponse(
                False,
                response.status_code,
                "User Password Needs To Be Atleast 8 Characters Long",
                None,
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.put("/api/user/change-active/{id}")
def userChangeActive(response: Response, id: int):
    try:
        userCollection = database.getCollection("user")
        userObject = userCollection.find_one({"_id": id}, {"is_active": True})

        if userObject != None:
            updatedUserObject = userCollection.update_one(
                {"_id": id},
                {
                    "$set": {
                        "is_active": not userObject["is_active"],
                        "updated_at": datetime.datetime.now(),
                    }
                },
            )

            if updatedUserObject:
                response.status_code = status.HTTP_202_ACCEPTED

                return Utility.formatResponse(
                    True,
                    response.status_code,
                    "User Status Change",
                    userCollection.find_one({"_id": id}),
                )

            else:
                response.status_code = status.HTTP_400_BAD_REQUEST

                return Utility.formatResponse(
                    False,
                    response.status_code,
                    "User Status Failed To Be Changed",
                    None,
                )
        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False, response.status_code, "User Not Found", None
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.delete("/api/user/remove/{id}")
def userRemove(response: Response, id: int):
    try:
        userCollection = database.getCollection("user")
        userObject = userCollection.find_one({"_id": id})

        if userObject != None:
            deletedUserObject = userCollection.find_one_and_delete({"_id": id})

            if deletedUserObject != None:
                response.status_code = status.HTTP_202_ACCEPTED

                return Utility.formatResponse(
                    True, response.status_code, "User Removed", deletedUserObject
                )

            else:
                response.status_code = status.HTTP_400_BAD_REQUEST

                return Utility.formatResponse(
                    False, response.status_code, "User Failed To Be Removed", None
                )
        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False, response.status_code, "User Not Found", None
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/document")
def document(response: Response, body: DocumentPageModel):
    try:
        documentQuery = [
            {
                "$lookup": {
                    "from": "user",
                    "localField": "id_author",
                    "foreignField": "_id",
                    "as": "author_extend",
                }
            },
            {"$unwind": "$author_extend"},
        ]

        if body.count != 0 and body.page != 0:
            documentQuery = documentQuery + [
                {"$skip": body.count * (body.page - 1)},
                {"$limit": body.count},
            ]

        documentQuery = documentQuery + [
            {
                "$project": {
                    "_id": 1,
                    "id_author": 1,
                    "code": 1,
                    "title": 1,
                    "category": 1,
                    "description": 1,
                    "created_at": 1,
                    "updated_at": 1,
                    "author_extend.username": 1,
                }
            },
        ]

        documentArray = list(
            database.getCollection("document").aggregate(documentQuery)
        )

        if len(documentArray) > 0:
            response.status_code = status.HTTP_200_OK

            return Utility.formatResponse(
                True, response.status_code, "Document Found", documentArray
            )

        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False, response.status_code, "Document Not Found", None
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/document/count")
def documentCount(response: Response):
    try:
        response.status_code = status.HTTP_200_OK

        documentCollection = database.getCollection("document")
        return Utility.formatResponse(
            True,
            response.status_code,
            "Document Count",
            {
                "total": documentCollection.count_documents({}),
            },
        )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/document/{id}")
def documentFind(response: Response, id: int):
    try:
        documentArray = list(
            database.getCollection("document").aggregate(
                [
                    {
                        "$lookup": {
                            "from": "user",
                            "localField": "id_author",
                            "foreignField": "_id",
                            "as": "author_extend",
                        }
                    },
                    {"$unwind": "$author_extend"},
                    {"$match": {"_id": id}},
                    {"$limit": 1},
                    {
                        "$project": {
                            "_id": 1,
                            "id_author": 1,
                            "code": 1,
                            "title": 1,
                            "category": 1,
                            "description": 1,
                            "created_at": 1,
                            "updated_at": 1,
                            "author_extend.username": 1,
                        }
                    },
                ]
            )
        )

        if len(documentArray) > 0:
            response.status_code = status.HTTP_200_OK

            return Utility.formatResponse(
                True, response.status_code, "Document Found", documentArray[0]
            )

        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False,
                response.status_code,
                "Document Not Found",
                None,
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/document/access/{id}")
def documentAccess(response: Response, body: DocumentPageModel, id: int):
    try:
        documentQuery = [
            {
                "$lookup": {
                    "from": "user",
                    "localField": "id_author",
                    "foreignField": "_id",
                    "as": "author_extend",
                }
            },
            {"$unwind": "$author_extend"},
            {
                "$match": {
                    "$or": [
                        {"id_author": id},
                        {
                            "_id": {
                                "$in": [
                                    accessObject["id_document"]
                                    for accessObject in list(
                                        database.getCollection("access").find(
                                            {"id_user": id}
                                        )
                                    )
                                ]
                            }
                        },
                    ]
                }
            },
        ]

        if body.count != 0 and body.page != 0:
            documentQuery = documentQuery + [
                {"$skip": body.count * (body.page - 1)},
                {"$limit": body.count},
            ]

        documentQuery = documentQuery + [
            {
                "$project": {
                    "_id": 1,
                    "id_author": 1,
                    "code": 1,
                    "title": 1,
                    "category": 1,
                    "description": 1,
                    "created_at": 1,
                    "updated_at": 1,
                    "author_extend.username": 1,
                }
            },
        ]

        documentArray = list(
            database.getCollection("document").aggregate(documentQuery)
        )

        if len(documentArray) > 0:
            response.status_code = status.HTTP_200_OK

            return Utility.formatResponse(
                True, response.status_code, "Document Access Found", documentArray
            )

        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False, response.status_code, "Document Access Not Found", None
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/document/access/{id}/count")
def documentAccessCount(response: Response, id: int):
    try:
        response.status_code = status.HTTP_200_OK

        documentCollection = database.getCollection("document")
        documentOwned = documentCollection.count_documents({"id_author": id})
        documentShared = documentCollection.count_documents(
            {
                "_id": {
                    "$in": [
                        accessObject["id_document"]
                        for accessObject in list(
                            database.getCollection("access").find({"id_user": id})
                        )
                    ]
                }
            }
        )

        return Utility.formatResponse(
            True,
            response.status_code,
            "Document Count",
            {
                "total": documentOwned + documentShared,
                "owned": documentOwned,
                "shared": documentShared,
            },
        )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.post("/api/document/upload")
def documentUpload(
    response: Response,
    id_author: int = Form(...),
    code: str = Form(...),
    title: str = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(),
):
    try:
        documentCollection = database.getCollection("document")
        newDocumentObject = {
            "_id": database.newId("document"),
            "id_author": id_author,
            "id_file": database.fileSystemInsert(file),
            "code": code,
            "title": title,
            "category": category,
            "description": description,
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
        }

        insertedDocumentObject = documentCollection.insert_one(newDocumentObject)

        if insertedDocumentObject != None:
            response.status_code = status.HTTP_201_CREATED

            return Utility.formatResponse(
                True, response.status_code, "Document Uploaded", newDocumentObject
            )

        else:
            response.status_code = status.HTTP_400_BAD_REQUEST

            return Utility.formatResponse(
                False,
                response.status_code,
                "Document Failed To Be Uploaded",
                None,
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/document/view/{id}")
def documentView(response: Response, id: int):
    try:
        documentObject = database.getCollection("document").find_one(
            {"_id": id}, {"id_file": True}
        )

        if documentObject != None:
            fileObject = database.fileSystemFind(documentObject["id_file"])

            if fileObject != None:
                response.status_code = status.HTTP_200_OK

                return StreamingResponse(
                    BytesIO(fileObject.read()), media_type="image/jpeg"
                )

            else:
                response.status_code = status.HTTP_404_NOT_FOUND

                return Utility.formatResponse(
                    False,
                    response.status_code,
                    "File Not Found",
                    None,
                )

        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False,
                response.status_code,
                "Document Not Found",
                None,
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.delete("/api/document/remove/{id}")
def documentRemove(response: Response, id: int):
    try:
        documentCollection = database.getCollection("document")
        documentObject = documentCollection.find_one({"_id": id})

        if documentObject != None:
            database.fileSystemDelete(documentObject["id_file"])
            database.getCollection("access").delete_many({"id_document": id})
            deletedDocumentObject = documentCollection.find_one_and_delete({"_id": id})

            if deletedDocumentObject != None:
                response.status_code = status.HTTP_202_ACCEPTED

                return Utility.formatResponse(
                    True,
                    response.status_code,
                    "Document Removed",
                    deletedDocumentObject,
                )

            else:
                response.status_code = status.HTTP_400_BAD_REQUEST

                return Utility.formatResponse(
                    False, response.status_code, "Document Failed To Be Removed", None
                )
        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False, response.status_code, "Document Not Found", None
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/access")
def access(response: Response, body: AccessPageModel):
    try:
        accessArray = list(
            database.getCollection("access")
            .find()
            .skip(body.count * (body.page - 1))
            .limit(body.count)
            if body.count != 0 and body.page != 0
            else database.getCollection("access").find()
        )

        if len(accessArray) > 0:
            response.status_code = status.HTTP_200_OK

            return Utility.formatResponse(
                True, response.status_code, "Access Found", accessArray
            )

        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False, response.status_code, "Access Not Found", None
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/access/count")
def accessCount(response: Response):
    try:
        response.status_code = status.HTTP_200_OK

        accessCollection = database.getCollection("access")
        return Utility.formatResponse(
            True,
            response.status_code,
            "Access Count",
            {
                "total": accessCollection.count_documents({}),
            },
        )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/access/{id}")
def accessFind(response: Response, id: int):
    try:
        accessArray = list(
            database.getCollection("access").aggregate(
                [
                    {
                        "$lookup": {
                            "from": "user",
                            "localField": "id_user",
                            "foreignField": "_id",
                            "as": "user_extend",
                        }
                    },
                    {"$unwind": "$user_extend"},
                    {"$match": {"_id": id}},
                    {"$limit": 1},
                    {
                        "$project": {
                            "_id": 1,
                            "id_user": 1,
                            "id_document": 1,
                            "user_extend.username": 1,
                        }
                    },
                ]
            )
        )

        if len(accessArray) > 0:
            response.status_code = status.HTTP_200_OK

            return Utility.formatResponse(
                True, response.status_code, "Access Found", accessArray[0]
            )

        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False,
                response.status_code,
                "Access Not Found",
                None,
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/access/document/{id}")
def accessDocument(response: Response, body: AccessPageModel, id: int):
    try:
        accessQuery = [
            {
                "$lookup": {
                    "from": "user",
                    "localField": "id_user",
                    "foreignField": "_id",
                    "as": "user_extend",
                }
            },
            {"$unwind": "$user_extend"},
            {"$match": {"id_document": id}},
        ]

        if body.count != 0 and body.page != 0:
            accessQuery = accessQuery + [
                {"$skip": body.count * (body.page - 1)},
                {"$limit": body.count},
            ]

        accessQuery = accessQuery + [
            {
                "$project": {
                    "_id": 1,
                    "id_user": 1,
                    "id_document": 1,
                    "user_extend.username": 1,
                }
            },
        ]

        accessArray = list(database.getCollection("access").aggregate(accessQuery))

        if len(accessArray) > 0:
            response.status_code = status.HTTP_200_OK

            return Utility.formatResponse(
                True, response.status_code, "Access Document Found", accessArray
            )

        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False, response.status_code, "Access Document Not Found", None
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/access/document/{id}/count")
def accessDocumentCount(response: Response, id: int):
    try:
        response.status_code = status.HTTP_200_OK

        accessCollection = database.getCollection("access")
        return Utility.formatResponse(
            True,
            response.status_code,
            "Access Document Count",
            {
                "total": accessCollection.count_documents({"id_document": id}),
            },
        )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.post("/api/access/add")
def accessAdd(response: Response, body: AccessAddModel):
    try:
        userObject = database.getCollection("user").find_one(
            {"username": body.username_user}, {"_id": True}
        )

        if userObject != None:
            accessCollection = database.getCollection("access")
            accessObject = accessCollection.find_one(
                {"id_user": userObject["_id"], "id_document": body.id_document},
                {"_id": True},
            )

            if accessObject == None:
                newAccessObject = {
                    "_id": database.newId("access"),
                    "id_user": userObject["_id"],
                    "id_document": body.id_document,
                    "created_at": datetime.datetime.now(),
                    "updated_at": datetime.datetime.now(),
                }
                insertedAccessObject = accessCollection.insert_one(newAccessObject)

                if insertedAccessObject != None:
                    response.status_code = status.HTTP_201_CREATED

                    return Utility.formatResponse(
                        True, response.status_code, "Access Added", newAccessObject
                    )

                else:
                    response.status_code = status.HTTP_400_BAD_REQUEST

                    return Utility.formatResponse(
                        False,
                        response.status_code,
                        "Access Failed To Be Added",
                        None,
                    )
            else:
                response.status_code = status.HTTP_404_NOT_FOUND

                return Utility.formatResponse(
                    False,
                    response.status_code,
                    "Access Already Existed",
                    None,
                )

        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False,
                response.status_code,
                "User Not Found",
                None,
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.delete("/api/access/remove/{id}")
def accessRemove(response: Response, id: int):
    try:
        accessCollection = database.getCollection("access")
        accessObject = accessCollection.find_one({"_id": id})

        if accessObject:
            deletedAccessObject = accessCollection.find_one_and_delete({"_id": id})

            if deletedAccessObject:
                response.status_code = status.HTTP_202_ACCEPTED

                return Utility.formatResponse(
                    True, response.status_code, "Access Deleted", deletedAccessObject
                )

            else:
                response.status_code = status.HTTP_400_BAD_REQUEST

                return Utility.formatResponse(
                    False, response.status_code, "Access Failed To Be Deleted", None
                )
        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False, response.status_code, "Access Not Found", None
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)

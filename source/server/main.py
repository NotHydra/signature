import datetime
from io import BytesIO

from click import File
from database import Database
from fastapi import FastAPI, Form, Response, UploadFile, status
from fastapi.responses import StreamingResponse
from model.document import DocumentPageModel
from model.login import LoginModel
from model.user import (
    UserModel,
    UserPageModel,
    UserUpdateModel,
    UserUpdatePasswordModel,
)
from utility import Utility

app = FastAPI()
database = Database()


@app.post("/api/auth/login")
def auth(response: Response, body: LoginModel):
    try:
        user = database.getCollection("user")
        documentObject = user.find_one(
            {"username": body.username}, {"_id": 1, "password": 1}
        )

        if documentObject:
            if Utility.decrypt(body.password, documentObject["password"]):
                response.status_code = status.HTTP_202_ACCEPTED

                return Utility.formatResponse(
                    True,
                    response.status_code,
                    "Login Successful",
                    {"_id": documentObject["_id"]},
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
        documentArray = list(
            database.getCollection("user")
            .find()
            .skip(body.count * (body.page - 1))
            .limit(body.count)
            if body.count != 0 and body.page != 0
            else database.getCollection("user").find()
        )

        if documentArray:
            response.status_code = status.HTTP_200_OK

            return Utility.formatResponse(
                True, response.status_code, "User Found", documentArray
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

        user = database.getCollection("user")
        return Utility.formatResponse(
            True,
            response.status_code,
            "User Count",
            {
                "total": user.count_documents({}),
                "user": user.count_documents({"role": "user"}),
                "admin": user.count_documents({"role": "admin"}),
            },
        )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/user/{id}")
def userFind(response: Response, id: int):
    try:
        documentObject = database.getCollection("user").find_one({"_id": id})

        if documentObject:
            response.status_code = status.HTTP_200_OK

            return Utility.formatResponse(
                True, response.status_code, "User Found", documentObject
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


@app.post("/api/user/create")
def userCreate(response: Response, body: UserModel):
    try:
        if Utility.checkEmail(body.email):
            if len(body.password) >= 8:
                if body.role in ["user", "admin"]:
                    user = database.getCollection("user")
                    newDocument = {
                        "_id": database.newId("user"),
                        "name": body.name,
                        "username": body.username,
                        "email": body.email,
                        "password": Utility.encrypt(body.password),
                        "role": body.role,
                        "isActive": body.isActive,
                        "createdAt": datetime.datetime.now(),
                        "updatedAt": datetime.datetime.now(),
                    }
                    documentObject = user.insert_one(newDocument)

                    if documentObject:
                        response.status_code = status.HTTP_201_CREATED

                        return Utility.formatResponse(
                            True, response.status_code, "User Created", newDocument
                        )

                    else:
                        response.status_code = status.HTTP_400_BAD_REQUEST

                        return Utility.formatResponse(
                            False,
                            response.status_code,
                            "User Failed To Be Created",
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


@app.put("/api/user/update/{id}")
def userUpdate(response: Response, id: int, body: UserUpdateModel):
    try:
        if Utility.checkEmail(body.email):
            if body.role in ["user", "admin"]:
                user = database.getCollection("user")
                documentObject = user.find_one({"_id": id})

                if documentObject:
                    documentObject = user.update_one(
                        {"_id": id},
                        {
                            "$set": {
                                "name": body.name,
                                "username": body.username,
                                "email": body.email,
                                "role": body.role,
                                "updatedAt": datetime.datetime.now(),
                            }
                        },
                    )

                    if documentObject:
                        response.status_code = status.HTTP_202_ACCEPTED

                        return Utility.formatResponse(
                            True,
                            response.status_code,
                            "User Updated",
                            user.find_one({"_id": id}),
                        )

                    else:
                        response.status_code = status.HTTP_400_BAD_REQUEST

                        return Utility.formatResponse(
                            False,
                            response.status_code,
                            "User Failed To Be Updated",
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


@app.put("/api/user/update-password/{id}")
def userUpdatePassword(response: Response, id: int, body: UserUpdatePasswordModel):
    try:
        if len(body.password) >= 8:
            user = database.getCollection("user")
            documentObject = user.find_one({"_id": id})

            if documentObject:
                documentObject = user.update_one(
                    {"_id": id},
                    {
                        "$set": {
                            "password": Utility.encrypt(body.password),
                            "updatedAt": datetime.datetime.now(),
                        }
                    },
                )

                if documentObject:
                    response.status_code = status.HTTP_202_ACCEPTED

                    return Utility.formatResponse(
                        True,
                        response.status_code,
                        "User Password Updated",
                        user.find_one({"_id": id}),
                    )

                else:
                    response.status_code = status.HTTP_400_BAD_REQUEST

                    return Utility.formatResponse(
                        False,
                        response.status_code,
                        "User Password Failed To Be Updated",
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


@app.put("/api/user/update-active/{id}")
def userUpdateActive(response: Response, id: int):
    try:
        user = database.getCollection("user")
        documentObject = user.find_one({"_id": id}, {"isActive": 1})

        if documentObject:
            documentObject = user.update_one(
                {"_id": id},
                {
                    "$set": {
                        "isActive": not documentObject["isActive"],
                        "updatedAt": datetime.datetime.now(),
                    }
                },
            )

            if documentObject:
                response.status_code = status.HTTP_202_ACCEPTED

                return Utility.formatResponse(
                    True,
                    response.status_code,
                    "User Status Updated",
                    user.find_one({"_id": id}),
                )

            else:
                response.status_code = status.HTTP_400_BAD_REQUEST

                return Utility.formatResponse(
                    False,
                    response.status_code,
                    "User Status Failed To Be Updated",
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


@app.delete("/api/user/delete/{id}")
def userDelete(response: Response, id: int):
    try:
        user = database.getCollection("user")
        documentObject = user.find_one({"_id": id})

        if documentObject:
            documentObject = user.find_one_and_delete({"_id": id})

            if documentObject:
                response.status_code = status.HTTP_202_ACCEPTED

                return Utility.formatResponse(
                    True, response.status_code, "User Deleted", documentObject
                )

            else:
                response.status_code = status.HTTP_400_BAD_REQUEST

                return Utility.formatResponse(
                    False, response.status_code, "User Failed To Be Deleted", None
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
        query = [
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
            query = query + [
                {"$skip": body.count * (body.page - 1)},
                {"$limit": body.count},
            ]

        query = query + [
            {
                "$project": {
                    "_id": 1,
                    "id_author": 1,
                    "code": 1,
                    "title": 1,
                    "category": 1,
                    "description": 1,
                    "createdAt": 1,
                    "updatedAt": 1,
                    "author_extend.username": 1,
                }
            },
        ]

        documentArray = list(database.getCollection("document").aggregate(query))

        if documentArray:
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


@app.get("/api/document/access/{id}")
def documentAccess(response: Response, body: DocumentPageModel, id: int):
    try:
        query = [
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
            query = query + [
                {"$skip": body.count * (body.page - 1)},
                {"$limit": body.count},
            ]

        query = query + [
            {
                "$project": {
                    "_id": 1,
                    "id_author": 1,
                    "code": 1,
                    "title": 1,
                    "category": 1,
                    "description": 1,
                    "createdAt": 1,
                    "updatedAt": 1,
                    "author_extend.username": 1,
                }
            },
        ]

        documentArray = list(database.getCollection("document").aggregate(query))

        if documentArray:
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

        document = database.getCollection("document")
        return Utility.formatResponse(
            True,
            response.status_code,
            "Document Count",
            {
                "total": document.count_documents({}),
            },
        )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        print(str(e))
        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.get("/api/document/access/{id}/count")
def documentAccessCount(response: Response, id: int):
    try:
        response.status_code = status.HTTP_200_OK

        document = database.getCollection("document")
        documentOwned = document.count_documents({"id_author": id})
        documentShared = document.count_documents(
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
                            "createdAt": 1,
                            "updatedAt": 1,
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
        document = database.getCollection("document")
        newDocument = {
            "_id": database.newId("document"),
            "id_author": id_author,
            "id_file": database.fileSystemInsert(file),
            "code": code,
            "title": title,
            "category": category,
            "description": description,
            "createdAt": datetime.datetime.now(),
            "updatedAt": datetime.datetime.now(),
        }

        documentObject = document.insert_one(newDocument)

        if documentObject:
            response.status_code = status.HTTP_201_CREATED

            return Utility.formatResponse(
                True, response.status_code, "Document Uploaded", newDocument
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


@app.get("/api/document/view/{id}", response_model=dict)
def documentView(response: Response, id: int):
    try:
        documentObject = database.getCollection("document").find_one(
            {"_id": id}, {"id_file": True}
        )

        if documentObject:
            file = database.fileSystemFind(documentObject["id_file"])

            if file:
                response.status_code = status.HTTP_200_OK

                return StreamingResponse(BytesIO(file.read()), media_type="image/jpeg")

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)

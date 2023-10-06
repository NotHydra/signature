import datetime

from fastapi import FastAPI, Response, status

from database import Database
from utility import Utility

from model.user import UserModel


app = FastAPI()
database = Database()


@app.get("/api/user")
def user(response: Response):
    try:
        documentArray = list(database.getCollection("user").find())

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
        return Utility.formatResponse(False, response.status_code, str(e), None)


@app.get("/api/user/{id}")
def user(response: Response, id: int):
    try:
        documentObject = database.getCollection("user").find_one({"_id": id})
        if documentObject:
            response.status_code = status.HTTP_200_OK
            return Utility.formatResponse(
                True, response.status_code, f"User {id} Found", documentObject
            )

        else:
            response.status_code = status.HTTP_404_NOT_FOUND
            return Utility.formatResponse(
                False,
                response.status_code,
                f"User {id} Not Found",
                None,
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Utility.formatResponse(False, response.status_code, str(e), None)


@app.post("/api/user/create")
def userCreate(response: Response, body: UserModel):
    try:
        user = database.getCollection("user")
        document = user.insert_one(
            {
                "_id": database.newId("user"),
                "name": body.name,
                "username": body.username,
                "email": body.email,
                "password": body.password,
                "level": body.level,
                "isActive": body.isActive,
                "createdAt": datetime.datetime.now(),
                "updatedAt": datetime.datetime.now(),
            }
        )

        if document:
            response.status_code = status.HTTP_201_CREATED
            return Utility.formatResponse(
                False, response.status_code, "User Created", None
            )

        else:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return Utility.formatResponse(
                False, response.status_code, "User Failed To Be Created", None
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Utility.formatResponse(False, response.status_code, str(e), None)

import datetime

from fastapi import FastAPI, Response, status

from database import Database
from utility import Utility

from model.user import UserModel
from model.login import LoginModel


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

        return Utility.formatResponse(False, response.status_code, "Server Error", None)


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

        return Utility.formatResponse(False, response.status_code, "Server Error", None)


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

        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.post("/api/user/create")
def userCreate(response: Response, body: UserModel):
    try:
        user = database.getCollection("user")
        newDocument = {
            "_id": database.newId("user"),
            "name": body.name,
            "username": body.username,
            "email": body.email,
            "password": Utility.encrypt(body.password),
            "level": body.level,
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
                False, response.status_code, "User Failed To Be Created", None
            )

    except Exception as e:
        errorMessage = str(e)
        if "E11000 duplicate key error collection" in errorMessage:
            response.status_code = status.HTTP_400_BAD_REQUEST

            if "username" in errorMessage:
                return Utility.formatResponse(
                    False, response.status_code, "Username already used", None
                )

            elif "email" in errorMessage:
                return Utility.formatResponse(
                    False, response.status_code, "Email already used", None
                )

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Utility.formatResponse(False, response.status_code, "Server Error", None)


@app.put("/api/user/update/{id}")
def userUpdate(response: Response, id: int, body: UserModel):
    try:
        user = database.getCollection("user")
        documentObject = user.find_one({"_id": id})

        if documentObject:
            newDocument = {
                "name": body.name,
                "username": body.username,
                "email": body.email,
                "level": body.level,
                "isActive": body.isActive,
                "updatedAt": datetime.datetime.now(),
            }

            if body.password:
                newDocument["password"] = Utility.encrypt(body.password)

            documentObject = user.find_one_and_update(
                {"_id": id},
                {"$set": newDocument},
            )

            if documentObject:
                response.status_code = status.HTTP_202_ACCEPTED

                return Utility.formatResponse(
                    True, response.status_code, f"User {id} Updated", documentObject
                )

            else:
                response.status_code = status.HTTP_400_BAD_REQUEST

                return Utility.formatResponse(
                    False, response.status_code, f"User {id} Failed To Be Updated", None
                )
        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False, response.status_code, f"User {id} Not Found", None
            )

    except Exception as e:
        errorMessage = str(e)
        if "E11000 duplicate key error collection" in errorMessage:
            response.status_code = status.HTTP_400_BAD_REQUEST

            if "username" in errorMessage:
                return Utility.formatResponse(
                    False, response.status_code, "Username already used", None
                )

            elif "email" in errorMessage:
                return Utility.formatResponse(
                    False, response.status_code, "Email already used", None
                )

        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

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
                    True, response.status_code, f"User {id} Deleted", documentObject
                )

            else:
                response.status_code = status.HTTP_400_BAD_REQUEST

                return Utility.formatResponse(
                    False, response.status_code, f"User {id} Failed To Be Deleted", None
                )
        else:
            response.status_code = status.HTTP_404_NOT_FOUND

            return Utility.formatResponse(
                False, response.status_code, f"User {id} Not Found", None
            )

    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        return Utility.formatResponse(False, response.status_code, str(e), None)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=8000, reload=True)

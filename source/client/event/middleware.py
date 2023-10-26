import requests


class Middleware:
    def refreshSessionDataMiddleware(self):
        try:
            response = requests.get(
                f"http://localhost:8000/api/user/{self.userObject['_id']}"
            ).json()

            if response["success"] == True:
                self.userObject["name"] = response["data"]["name"]
                self.userObject["username"] = response["data"]["username"]
                self.userObject["email"] = response["data"]["email"]
                self.userObject["role"] = response["data"]["role"]
                self.userObject["isActive"] = response["data"]["isActive"]

                return True

            else:
                self.errorMessage(response["message"])
                self.logoutCall()

        except:
            self.errorMessage("Server Error")
            self.logoutCall()

        return False

class Call:
    def forgetCall(self) -> None:
        for widget in self.winfo_children():
            if "frame" in str(widget):
                widget.grid_forget()

    def logoutCall(self) -> None:
        self.userObject = {
            "_id": 0,
            "name": None,
            "username": None,
            "email": None,
            "role": None,
            "isActive": None,
        }

        self.forgetCall()
        self.loginFrame()

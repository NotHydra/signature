import time
import random
import requests
import customtkinter as ctk

from PIL import Image

from component.message import Message
from component.widget import Widget
from event.call import Call
from event.middleware import Middleware

from module import Dependency, Utility


class App(ctk.CTk, Message, Widget, Call, Middleware):
    userObject = {
        "_id": 0,
        "name": None,
        "username": None,
        "email": None,
        "role": None,
        "isActive": None,
    }

    sidebarId = 1

    def __init__(self) -> None:
        super().__init__()

        self.iconbitmap(Dependency.appIconPath)
        self.title(f"{Dependency.title} - {Dependency.subtitle}")
        self.geometry(
            f"{Dependency.resolution['width']}x{Dependency.resolution['height']}"
        )
        self.resizable(False, False)

        self.loadingFrame()

    def loadingFrame(self) -> None:
        def logoGroup():
            logoLoadingImage = ctk.CTkLabel(
                loadingFrame,
                image=ctk.CTkImage(
                    Image.open(Utility.getAsset("logo.png")),
                    size=(
                        Dependency.logoResolution["width"] / 4,
                        Dependency.logoResolution["height"] / 4,
                    ),
                ),
                text="",
            )
            logoLoadingImage.grid(row=0, column=0, padx=20)

        def contentGroup():
            def increaseLoadingValue() -> None:
                if not Dependency.skip:
                    loadingValue = 0
                    while loadingValue < 1:
                        loadingValue += random.uniform(0.005, 0.01)
                        progressTextProgressBar.set(loadingValue)

                        self.update()
                        time.sleep(0.00001)

                self.forgetCall()
                self.loginFrame()

            textLoadingFrame = ctk.CTkFrame(
                loadingFrame, corner_radius=0, fg_color="transparent"
            )
            textLoadingFrame.rowconfigure([0, 1, 2], weight=1)
            textLoadingFrame.columnconfigure(0, weight=1)
            textLoadingFrame.grid(row=0, column=1, padx=20)

            titleTextLabel = ctk.CTkLabel(
                textLoadingFrame,
                text=Dependency.title.upper(),
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=80,
                    weight="bold",
                ),
                text_color=Dependency.colorPalette["text"],
            )
            titleTextLabel.grid(row=0, column=0, sticky="ew")

            subtitleTextLabel = ctk.CTkLabel(
                textLoadingFrame,
                text=Dependency.subtitle.upper(),
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=27,
                    weight="bold",
                ),
                text_color=Dependency.colorPalette["text"],
            )
            subtitleTextLabel.grid(row=1, column=0, sticky="ew")

            progressTextProgressBar = ctk.CTkProgressBar(
                textLoadingFrame,
                orientation="horizontal",
                mode="determinate",
                progress_color=Dependency.colorPalette["main"],
            )
            progressTextProgressBar.grid(row=2, column=0, pady=10, sticky="ew")
            progressTextProgressBar.set(0)

            self.after(500, increaseLoadingValue)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        loadingFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        loadingFrame.rowconfigure(0, weight=1)
        loadingFrame.columnconfigure([0, 1], weight=1)
        loadingFrame.grid(row=0, column=0)

        logoGroup()
        contentGroup()

    def loginFrame(self) -> None:
        def aboutGroup():
            aboutFrame = ctk.CTkFrame(
                self, corner_radius=0, fg_color=Dependency.colorPalette["main"]
            )
            aboutFrame.rowconfigure(0, weight=1)
            aboutFrame.columnconfigure(0, weight=1)
            aboutFrame.grid(row=0, column=0, sticky="nsew")

            descriptionAboutLabel = ctk.CTkLabel(
                aboutFrame,
                image=ctk.CTkImage(
                    Image.open(Utility.getAsset("logo-opacity.png")),
                    size=(
                        Dependency.logoResolution["width"] / 2,
                        Dependency.logoResolution["height"] / 2,
                    ),
                ),
                text="SIGNATURE\nDesktop-based application\nthat is capable of digitally\nmanaging multiple kinds of\ndocument online. Such as\nuploading, downloading and\nsigning digital documents.",
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=20,
                    weight="bold",
                ),
                text_color=Dependency.colorPalette["text"],
            )
            descriptionAboutLabel.grid(row=0, column=0, sticky="nsew")

        def loginGroup():
            def submitButtonEvent():
                username = usernameLoginEntry.get()
                password = passwordLoginEntry.get()

                if username != "" and password != "":
                    response = None
                    try:
                        response = requests.post(
                            "http://localhost:8000/api/auth/login",
                            json={"username": username, "password": password},
                        ).json()

                    except:
                        self.errorMessage("Server Error")

                    if (response != None):
                        if response["success"] == True:
                            self.successMessage(response["message"])

                            self.userObject["_id"] = response["data"]["_id"]

                            self.forgetCall()
                            self.homeFrame()

                        else:
                            self.errorMessage(response["message"])

                else:
                    self.errorMessage("Please Insert Username and Password")

            def exitButtonEvent():
                if self.confirmationMessage():
                    self.quit()

            loginFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
            loginFrame.columnconfigure(0, weight=1)
            loginFrame.grid(row=0, column=1, sticky="nsew")

            titleLoginLabel = ctk.CTkLabel(
                loginFrame,
                text="Login Details",
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"], size=40, weight="bold"
                ),
            )
            titleLoginLabel.grid(row=0, column=0, pady=(180, 20))

            usernameLoginEntry = ctk.CTkEntry(
                loginFrame,
                width=320,
                height=60,
                placeholder_text="username",
                justify="center",
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"], size=20, weight="bold"
                ),
            )
            usernameLoginEntry.grid(row=1, column=0, pady=(0, 10))

            passwordLoginEntry = ctk.CTkEntry(
                loginFrame,
                width=320,
                height=60,
                show="*",
                placeholder_text="password",
                justify="center",
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"], size=20, weight="bold"
                ),
            )
            passwordLoginEntry.grid(row=2, column=0, pady=(0, 10))

            submitLoginButton = ctk.CTkButton(
                loginFrame,
                text="Login",
                width=320,
                height=60,
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"], size=24, weight="bold"
                ),
                fg_color=Dependency.colorPalette["main"],
                hover_color=Dependency.colorPalette["main-dark"],
                command=submitButtonEvent,
            )
            submitLoginButton.grid(row=3, column=0, pady=(0, 10))

            exitLoginButton = ctk.CTkButton(
                loginFrame,
                text="Exit",
                width=320,
                height=60,
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"], size=24, weight="bold"
                ),
                fg_color=Dependency.colorPalette["danger"],
                hover_color=Dependency.colorPalette["danger-dark"],
                command=exitButtonEvent,
            )
            exitLoginButton.grid(row=4, column=0)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        aboutGroup()
        loginGroup()

        if Dependency.skip:
            self.userObject["_id"] = 1

            self.forgetCall()
            self.homeFrame()

    def homeFrame(self) -> None:
        if self.refreshSessionDataMiddleware():

            def contentGroup():
                def welcomeGroup():
                    welcomeContentLabel = ctk.CTkLabel(
                        contentFrame,
                        height=40,
                        corner_radius=8,
                        text=f"Welcome to Signature {self.userObject['username']}!",
                        font=ctk.CTkFont(
                            family=Dependency.fontFamily["main"],
                            size=20,
                            weight="bold",
                        ),
                        text_color=Dependency.colorPalette["text"],
                        fg_color=Dependency.colorPalette["main"],
                    )
                    welcomeContentLabel.grid(
                        row=1, column=0, pady=(0, 20), sticky="nsew"
                    )

                def changeButtonEvent():
                    pass

                def changePasswordButtonEvent():
                    pass

                contentFrame = ctk.CTkFrame(
                    self, corner_radius=0, fg_color="transparent"
                )
                contentFrame.rowconfigure(2, weight=1)
                contentFrame.columnconfigure(0, weight=1)
                contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

                self.titleContentWidget(contentFrame, "HOME")

                welcomeGroup()

                self.containerWidget(
                    contentFrame,
                    2,
                    "Profile",
                    [
                        {
                            "id": 1,
                            "entry": [
                                {
                                    "id": 1,
                                    "text": "Name",
                                    "placeholder": "name",
                                    "value": self.userObject["name"],
                                    "state": False,
                                },
                                {
                                    "id": 2,
                                    "text": "Username",
                                    "placeholder": "username",
                                    "value": self.userObject["username"],
                                    "state": False,
                                },
                            ],
                        },
                        {
                            "id": 2,
                            "entry": [
                                {
                                    "id": 1,
                                    "text": "Email",
                                    "placeholder": "email",
                                    "value": self.userObject["email"],
                                    "state": False,
                                },
                                {
                                    "id": 2,
                                    "text": "Role",
                                    "placeholder": "role",
                                    "value": self.userObject["role"],
                                    "state": False,
                                },
                            ],
                        },
                    ],
                    [
                        {
                            "id": 1,
                            "text": "Change",
                            "icon": "change",
                            "color": Dependency.colorPalette["warning"],
                            "hover": Dependency.colorPalette["warning-dark"],
                            "event": changeButtonEvent,
                        },
                        {
                            "id": 2,
                            "text": "Change Password",
                            "icon": "password",
                            "color": Dependency.colorPalette["danger"],
                            "hover": Dependency.colorPalette["danger-dark"],
                            "event": changePasswordButtonEvent,
                        },
                    ],
                )

            self.sidebarId = 1

            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=31)

            self.sidebarWidget()

            contentGroup()

    def userFrame(self) -> None:
        if self.refreshSessionDataMiddleware():
            self.sidebarId = 2

            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=31)

            self.sidebarWidget()

            contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
            contentFrame.columnconfigure(0, weight=1)
            contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

            titleContentLabel = ctk.CTkLabel(
                contentFrame,
                text="USER",
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=36,
                    weight="bold",
                ),
                text_color=Dependency.colorPalette["text"],
            )
            titleContentLabel.grid(row=0, column=0, pady=10, sticky="nsw")

            boxContentFrame = ctk.CTkFrame(
                contentFrame,
                height=80,
                corner_radius=8,
                fg_color="transparent",
            )
            boxContentFrame.rowconfigure(0, weight=1)
            boxContentFrame.columnconfigure([0, 1, 2], weight=1)
            boxContentFrame.grid(row=1, column=0, sticky="nsew")

            try:
                response = requests.get(
                    "http://localhost:8000/api/user/count",
                ).json()

            except:
                pass

            boxButtonArray = [
                {
                    "id": 1,
                    "icon": "user-total",
                    "display": "Total",
                    "value": response["data"]["total"] | 0,
                },
                {
                    "id": 2,
                    "icon": "user",
                    "display": "User",
                    "value": response["data"]["user"] | 0,
                },
                {
                    "id": 3,
                    "icon": "admin",
                    "display": "Admin",
                    "value": response["data"]["admin"] | 0,
                },
            ]

            for boxButtonIndex, boxButtonObject in enumerate(boxButtonArray):
                ctk.CTkButton(
                    boxContentFrame,
                    height=72,
                    image=ctk.CTkImage(
                        Image.open(Utility.getIcon(f"{boxButtonObject['icon']}.png")),
                        size=(40, 40),
                    ),
                    text=f"{boxButtonObject['display']}\n{boxButtonObject['value']}",
                    font=ctk.CTkFont(
                        family=Dependency.fontFamily["main"], size=20, weight="bold"
                    ),
                    corner_radius=8,
                    text_color=Dependency.colorPalette["text"],
                    fg_color=Dependency.colorPalette["main"],
                    hover_color=Dependency.colorPalette["main"],
                ).grid(
                    row=0,
                    column=boxButtonIndex,
                    padx=(0, 20) if boxButtonIndex != (len(boxButtonArray) - 1) else 0,
                    sticky="nsew",
                )


if __name__ == "__main__":
    app = App()
    app.mainloop()

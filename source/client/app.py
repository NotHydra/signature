import os
import time
import random
import requests
import customtkinter as ctk

from PIL import Image
from CTkMessagebox import CTkMessagebox


class Utility:
    def combinePath(base: str, path: str) -> str:
        return os.path.join(base, path)

    def getAsset(file):
        return Utility.combinePath(Dependency.assetPath, file)

    def getIcon(file):
        return Utility.combinePath(Dependency.iconPath, file)


class Dependency:
    title = "Signature"
    subtitle = "Online Document Application"

    resolution = {"width": 1200, "height": 700}
    logoResolution = {"width": 639, "height": 799}

    path = os.path.dirname(os.path.realpath(__file__))
    assetPath = Utility.combinePath(path, "..\\asset")
    iconPath = Utility.combinePath(assetPath, "icon")
    appIconPath = "./source/asset/icon.ico"

    fontFamily = {"main": "Montserrat"}
    colorPalette = {
        "main": "#54A4F5",
        "main-dark": "#3498DB",
        "text": "#FFFFFF",
        "success": "#2ECC71",
        "success-dark": "#28B463",
        "warning": "#F1C40F",
        "warning-dark": "#D4AC0D",
        "danger": "#E74C3C",
        "danger-dark": "#CB4335",
    }

    skip = False


class Message:
    def errorMessage(self, message: str) -> None:
        CTkMessagebox(
            corner_radius=8,
            icon="cancel",
            title="Error",
            message=message,
        )

    def successMessage(self, message: str) -> None:
        CTkMessagebox(
            corner_radius=8,
            icon="check",
            title="Success",
            message=message,
        )

    def confirmationMessage(self, message: str = "Are You Sure?") -> None:
        return (
            True
            if CTkMessagebox(
                corner_radius=8,
                icon="question",
                title="Confirmation",
                message=message,
                option_1="Yes",
                option_2="No",
            ).get()
            == "Yes"
            else False
        )


class Component:
    def lineComponent(self, master, row, column, weight=2):
        ctk.CTkFrame(
            master,
            height=weight,
            corner_radius=0,
            fg_color=Dependency.colorPalette["text"],
        ).grid(row=row, column=column, sticky="nsew")

    def sidebarComponent(self) -> None:
        def sidebarButton(master, item, start=0, index=0, highlight=False):
            ctk.CTkButton(
                master,
                height=40,
                image=ctk.CTkImage(
                    Image.open(Utility.getIcon(f"{item['icon']}.png")),
                    size=(20, 20),
                ),
                text=item["title"],
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"], size=16, weight="bold"
                ),
                cursor="hand2",
                corner_radius=0,
                text_color=Dependency.colorPalette["text"],
                fg_color=Dependency.colorPalette["main-dark"]
                if (highlight and self.sidebarId == item["id"])
                else Dependency.colorPalette["main"],
                hover_color=Dependency.colorPalette["main-dark"],
                command=item["event"],
            ).grid(row=(start + index), column=0, sticky="ew")

        def contentGroup():
            def brandButtonEvent():
                self.forgetCall()
                self.homeFrame()

            def brandGroup():
                brandSidebarButton = ctk.CTkButton(
                    contentSidebarFrame,
                    height=80,
                    image=ctk.CTkImage(
                        Image.open(Utility.getAsset("logo.png")),
                        size=(
                            Dependency.logoResolution["width"] / 16,
                            Dependency.logoResolution["height"] / 16,
                        ),
                    ),
                    text="Signature",
                    font=ctk.CTkFont(
                        family=Dependency.fontFamily["main"], size=28, weight="bold"
                    ),
                    cursor="hand2",
                    corner_radius=0,
                    text_color=Dependency.colorPalette["text"],
                    fg_color=Dependency.colorPalette["main"],
                    hover_color=Dependency.colorPalette["main-dark"],
                    command=brandButtonEvent,
                )
                brandSidebarButton.grid(row=0, column=0, sticky="ew")

            def profileGroup():
                profileSidebarFrame = ctk.CTkFrame(
                    contentSidebarFrame, corner_radius=0, fg_color="transparent"
                )
                profileSidebarFrame.rowconfigure(0, weight=1)
                profileSidebarFrame.columnconfigure([0, 1], weight=1)
                profileSidebarFrame.grid(row=2, column=0, sticky="ew")

                roleProfileImage = ctk.CTkLabel(
                    profileSidebarFrame,
                    image=ctk.CTkImage(
                        Image.open(Utility.getIcon(f"{self.userObject['role']}.png")),
                        size=(32, 32),
                    ),
                    text="",
                )
                roleProfileImage.grid(row=0, column=0, padx=10, rowspan=2, sticky="e")

                usernameProfileLabel = ctk.CTkLabel(
                    profileSidebarFrame,
                    text=self.userObject["username"],
                    font=ctk.CTkFont(
                        family=Dependency.fontFamily["main"], size=20, weight="bold"
                    ),
                    text_color=Dependency.colorPalette["text"],
                )
                usernameProfileLabel.grid(row=0, column=1, padx=10, sticky="w")

                roleProfileLabel = ctk.CTkLabel(
                    profileSidebarFrame,
                    text=str(self.userObject["role"]).upper(),
                    font=ctk.CTkFont(
                        family=Dependency.fontFamily["main"], size=12, weight="bold"
                    ),
                    text_color=Dependency.colorPalette["text"],
                )
                roleProfileLabel.grid(row=1, column=1, padx=10, sticky="w")

            def itemGroup():
                def homeButtonEvent():
                    self.forgetCall()
                    self.homeFrame()

                sidebarItemArray = [
                    {
                        "id": 1,
                        "title": "Home",
                        "icon": "house",
                        "event": homeButtonEvent,
                    }
                ]

                if self.userObject["role"] == "user":
                    sidebarItemArray = sidebarItemArray + [
                        {
                            "id": 2,
                            "title": "Upload",
                            "icon": "upload",
                            "event": lambda: None,
                        },
                        {
                            "id": 3,
                            "title": "Download",
                            "icon": "download",
                            "event": lambda: None,
                        },
                        {
                            "id": 4,
                            "title": "Sign",
                            "icon": "sign",
                            "event": lambda: None,
                        },
                    ]

                elif self.userObject["role"] == "admin":

                    def userButtonEvent():
                        self.forgetCall()
                        self.userFrame()

                    sidebarItemArray = sidebarItemArray + [
                        {
                            "id": 2,
                            "title": "User",
                            "icon": "user",
                            "event": userButtonEvent,
                        }
                    ]

                for sidebarItemIndex, sidebarItemObject in enumerate(sidebarItemArray):
                    sidebarButton(
                        contentSidebarFrame,
                        sidebarItemObject,
                        4,
                        sidebarItemIndex,
                        True,
                    )

            contentSidebarFrame = ctk.CTkFrame(
                sidebarFrame,
                corner_radius=0,
                fg_color=Dependency.colorPalette["main"],
            )
            contentSidebarFrame.columnconfigure(0, weight=1)
            contentSidebarFrame.grid(row=0, column=0, sticky="new")

            brandGroup()

            self.lineComponent(contentSidebarFrame, 1, 0)

            profileGroup()

            self.lineComponent(contentSidebarFrame, 3, 0)

            itemGroup()

        def footerGroup():
            def logoutGroup():
                def logoutButtonEvent():
                    if self.confirmationMessage():
                        self.logoutCall()

                sidebarButton(
                    footerSidebarFrame,
                    {
                        "id": 1,
                        "title": "Logout",
                        "icon": "logout",
                        "event": logoutButtonEvent,
                    },
                )

            def copyrightGroup():
                copyrightSidebarLabel = ctk.CTkLabel(
                    footerSidebarFrame,
                    height=40,
                    text="Copyright © 2023 Kelompok 8",
                    font=ctk.CTkFont(
                        family=Dependency.fontFamily["main"], size=12, weight="bold"
                    ),
                    corner_radius=0,
                    text_color=Dependency.colorPalette["text"],
                )
                copyrightSidebarLabel.grid(row=2, column=0, sticky="ew")

            footerSidebarFrame = ctk.CTkFrame(
                sidebarFrame,
                corner_radius=0,
                fg_color=Dependency.colorPalette["main"],
            )
            footerSidebarFrame.columnconfigure(0, weight=1)
            footerSidebarFrame.grid(row=1, column=0, sticky="sew")

            logoutGroup()

            self.lineComponent(footerSidebarFrame, 1, 0)

            copyrightGroup()

        sidebarFrame = ctk.CTkFrame(
            self, corner_radius=0, fg_color=Dependency.colorPalette["main"]
        )
        sidebarFrame.rowconfigure(0, weight=15)
        sidebarFrame.rowconfigure(1, weight=1)
        sidebarFrame.columnconfigure(0, weight=1)
        sidebarFrame.grid(row=0, column=0, sticky="nsew")

        contentGroup()
        footerGroup()

    def titleContentComponent(self, master, title: str, row: int) -> None:
        ctk.CTkLabel(
            master,
            text=title,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=36,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"],
        ).grid(row=row, column=0, pady=5, sticky="nsw")

    def titleContainerComponent(self, master, title, row):
        ctk.CTkLabel(
            master,
            text=title,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=20,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"],
        ).grid(row=row, column=0, padx=10, pady=10, sticky="nsw")

    def entryDataComponent(self, master, title, placeholder, value, state, row, column):
        entryFrame = ctk.CTkFrame(master, corner_radius=0, fg_color="transparent")
        entryFrame.rowconfigure([0, 1], weight=1)
        entryFrame.columnconfigure(0, weight=1)
        entryFrame.grid(row=row, column=column, sticky="nsew")

        ctk.CTkLabel(
            entryFrame,
            text=title,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=20,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"],
        ).grid(
            row=0,
            column=0,
            padx=(0, 5) if column == 0 else (5, 0),
            pady=(0, 5),
            sticky="nsw",
        )

        entryValue = ctk.StringVar()
        entryValue.set(value)

        entryObject = ctk.CTkEntry(
            entryFrame,
            height=40,
            placeholder_text=placeholder,
            textvariable=entryValue,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=20,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"],
            placeholder_text_color=Dependency.colorPalette["text"],
            fg_color="transparent",
            border_color=Dependency.colorPalette["text"],
            state="normal" if state else "disabled",
        )
        entryObject.grid(
            row=1,
            column=0,
            padx=(0, 5) if column == 0 else (5, 0),
            pady=(0, 10),
            sticky="nsew",
        )

        return entryObject

    def buttonDataComponent(
        self, master, text, icon, mainColor, hoverColor, event, row
    ):
        ctk.CTkButton(
            master,
            height=40,
            image=ctk.CTkImage(
                Image.open(Utility.getIcon(f"{icon}.png")),
                size=(24, 24),
            ),
            text=text,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=20,
                weight="bold",
            ),
            cursor="hand2",
            corner_radius=8,
            text_color=Dependency.colorPalette["text"],
            fg_color=mainColor,
            hover_color=hoverColor,
            command=event,
        ).grid(
            row=row,
            column=0,
            columnspan=2,
            pady=(0, 10),
            sticky="nsew",
        )


class Call:
    def forgetCall(self: ctk.CTk) -> None:
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


class Middleware:
    def refreshSessionDataMiddleware(self) -> bool:
        response = None
        try:
            response = requests.get(
                f"http://localhost:8000/api/user/{self.userObject['_id']}"
            ).json()

        except:
            self.errorMessage("Server Error")
            self.logoutCall()

        if response != None:
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

        return False


class App(ctk.CTk, Message, Component, Call, Middleware):
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
        def loadingEvent() -> None:
            if not Dependency.skip:
                loadingValue = 0
                while loadingValue < 1:
                    loadingValue += random.uniform(0.005, 0.01)
                    progressTextProgressBar.set(loadingValue)

                    self.update()
                    time.sleep(0.00001)

            self.forgetCall()
            self.loginFrame()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        loadingFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        loadingFrame.rowconfigure(0, weight=1)
        loadingFrame.columnconfigure([0, 1], weight=1)
        loadingFrame.grid(row=0, column=0)

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

        self.after(500, loadingEvent)

    def loginFrame(self) -> None:
        def submitButtonEvent() -> None:
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

                if response != None:
                    if response["success"] == True:
                        self.successMessage(response["message"])

                        self.userObject["_id"] = response["data"]["_id"]

                        self.forgetCall()
                        self.homeFrame()

                    else:
                        self.errorMessage(response["message"])

            else:
                self.errorMessage("Please Insert Username and Password")

        def exitButtonEvent() -> None:
            if self.confirmationMessage():
                self.quit()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

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

        if Dependency.skip:
            self.userObject["_id"] = 1

            self.forgetCall()
            self.homeFrame()

    def homeFrame(self) -> None:
        if self.refreshSessionDataMiddleware():

            def changeButtonEvent() -> None:
                self.forgetCall()
                self.homeChangeFrame()

            def changePasswordButtonEvent() -> None:
                pass

            self.sidebarId = 1

            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=31)

            self.sidebarComponent()

            contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
            contentFrame.rowconfigure(2, weight=1)
            contentFrame.columnconfigure(0, weight=1)
            contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

            self.titleContentComponent(contentFrame, title="HOME", row=0)

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
            welcomeContentLabel.grid(row=1, column=0, pady=(0, 20), sticky="nsew")

            containerContentFrame = ctk.CTkFrame(
                contentFrame,
                corner_radius=8,
                fg_color=Dependency.colorPalette["main"],
            )
            containerContentFrame.columnconfigure(0, weight=1)
            containerContentFrame.grid(row=2, column=0, pady=(0, 20), sticky="nsew")

            self.titleContainerComponent(containerContentFrame, title="Profile", row=0)
            self.lineComponent(containerContentFrame, row=1, column=0)

            dataContainerFrame = ctk.CTkFrame(
                containerContentFrame,
                corner_radius=0,
                fg_color="transparent",
            )
            dataContainerFrame.columnconfigure([0, 1], weight=1)
            dataContainerFrame.grid(
                row=2, column=0, padx=10, pady=(5, 0), sticky="nsew"
            )

            self.entryDataComponent(
                dataContainerFrame,
                title="Name",
                placeholder="name",
                value=self.userObject["name"],
                state=False,
                row=0,
                column=0,
            )
            self.entryDataComponent(
                dataContainerFrame,
                title="Username",
                placeholder="username",
                value=self.userObject["username"],
                state=False,
                row=0,
                column=1,
            )

            self.entryDataComponent(
                dataContainerFrame,
                title="Email",
                placeholder="email",
                value=self.userObject["email"],
                state=False,
                row=1,
                column=0,
            )
            self.entryDataComponent(
                dataContainerFrame,
                title="Role",
                placeholder="role",
                value=self.userObject["role"],
                state=False,
                row=1,
                column=1,
            )

            self.buttonDataComponent(
                dataContainerFrame,
                text="Change",
                icon="change",
                mainColor=Dependency.colorPalette["warning"],
                hoverColor=Dependency.colorPalette["warning-dark"],
                event=changeButtonEvent,
                row=2,
            )
            self.buttonDataComponent(
                dataContainerFrame,
                text="Change Password",
                icon="password",
                mainColor=Dependency.colorPalette["danger"],
                hoverColor=Dependency.colorPalette["danger-dark"],
                event=changePasswordButtonEvent,
                row=3,
            )

    # def homeChangeFrame(self) -> None:
    #     if self.refreshSessionDataMiddleware():
    #         self.sidebarId = 1

    #         self.rowconfigure(0, weight=1)
    #         self.columnconfigure(0, weight=1)
    #         self.columnconfigure(1, weight=31)

    #         self.sidebarComponent()

    #         def changeButtonEvent():
    #             if self.confirmationMessage():
    #                 name = entryArray[0].get()
    #                 username = entryArray[1].get()
    #                 email = entryArray[2].get()

    #                 if name != "" and username != "" and email != "":
    #                     response = None
    #                     try:
    #                         response = requests.post(
    #                             f"http://localhost:8000/api/user/update/{self.userObject['_id']}",
    #                             json={
    #                                 "name": name,
    #                                 "username": username,
    #                                 "email": email,
    #                                 "role": self.userObject["role"],
    #                             },
    #                         ).json()

    #                     except:
    #                         self.errorMessage("Server Error")

    #                     if response != None:
    #                         if response["success"] == True:
    #                             self.successMessage(response["message"])

    #                             self.userObject["_id"] = response["data"]["_id"]

    #                             self.forgetCall()
    #                             self.homeChangeFrame()

    #                         else:
    #                             self.errorMessage(response["message"])

    #                 else:
    #                     self.errorMessage("Please Insert Name, Username and Email")

    #         def backButtonEvent():
    #             self.forgetCall()
    #             self.homeFrame()

    #         contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
    #         contentFrame.rowconfigure(1, weight=1)
    #         contentFrame.columnconfigure(0, weight=1)
    #         contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

    #         self.titleContentComponent(contentFrame, "HOME CHANGE PROFILE")

    #         entryArray = self.containerComponent(
    #             contentFrame,
    #             1,
    #             "Change Profile",
    #             [
    #                 {
    #                     "id": 1,
    #                     "entry": [
    #                         {
    #                             "id": 1,
    #                             "text": "Name",
    #                             "placeholder": "name",
    #                             "value": self.userObject["name"],
    #                             "state": True,
    #                         },
    #                         {
    #                             "id": 2,
    #                             "text": "Username",
    #                             "placeholder": "username",
    #                             "value": self.userObject["username"],
    #                             "state": True,
    #                         },
    #                     ],
    #                 },
    #                 {
    #                     "id": 2,
    #                     "entry": [
    #                         {
    #                             "id": 1,
    #                             "text": "Email",
    #                             "placeholder": "email",
    #                             "value": self.userObject["email"],
    #                             "state": True,
    #                         }
    #                     ],
    #                 },
    #             ],
    #             [
    #                 {
    #                     "id": 1,
    #                     "text": "Change",
    #                     "icon": "change",
    #                     "color": Dependency.colorPalette["warning"],
    #                     "hover": Dependency.colorPalette["warning-dark"],
    #                     "event": changeButtonEvent,
    #                 },
    #                 {
    #                     "id": 2,
    #                     "text": "Back",
    #                     "icon": "back",
    #                     "color": Dependency.colorPalette["danger"],
    #                     "hover": Dependency.colorPalette["danger-dark"],
    #                     "event": backButtonEvent,
    #                 },
    #             ],
    #         )

    # def userFrame(self) -> None:
    #     if self.refreshSessionDataMiddleware():
    #         self.sidebarId = 2

    #         self.rowconfigure(0, weight=1)
    #         self.columnconfigure(0, weight=1)
    #         self.columnconfigure(1, weight=31)

    #         self.sidebarComponent()

    #         contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
    #         contentFrame.columnconfigure(0, weight=1)
    #         contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

    #         titleContentLabel = ctk.CTkLabel(
    #             contentFrame,
    #             text="USER",
    #             font=ctk.CTkFont(
    #                 family=Dependency.fontFamily["main"],
    #                 size=36,
    #                 weight="bold",
    #             ),
    #             text_color=Dependency.colorPalette["text"],
    #         )
    #         titleContentLabel.grid(row=0, column=0, pady=10, sticky="nsw")

    #         boxContentFrame = ctk.CTkFrame(
    #             contentFrame,
    #             height=80,
    #             corner_radius=8,
    #             fg_color="transparent",
    #         )
    #         boxContentFrame.rowconfigure(0, weight=1)
    #         boxContentFrame.columnconfigure([0, 1, 2], weight=1)
    #         boxContentFrame.grid(row=1, column=0, sticky="nsew")

    #         try:
    #             response = requests.get(
    #                 "http://localhost:8000/api/user/count",
    #             ).json()

    #         except:
    #             pass

    #         boxButtonArray = [
    #             {
    #                 "id": 1,
    #                 "icon": "user-total",
    #                 "display": "Total",
    #                 "value": response["data"]["total"] | 0,
    #             },
    #             {
    #                 "id": 2,
    #                 "icon": "user",
    #                 "display": "User",
    #                 "value": response["data"]["user"] | 0,
    #             },
    #             {
    #                 "id": 3,
    #                 "icon": "admin",
    #                 "display": "Admin",
    #                 "value": response["data"]["admin"] | 0,
    #             },
    #         ]

    #         for boxButtonIndex, boxButtonObject in enumerate(boxButtonArray):
    #             ctk.CTkButton(
    #                 boxContentFrame,
    #                 height=72,
    #                 image=ctk.CTkImage(
    #                     Image.open(Utility.getIcon(f"{boxButtonObject['icon']}.png")),
    #                     size=(40, 40),
    #                 ),
    #                 text=f"{boxButtonObject['display']}\n{boxButtonObject['value']}",
    #                 font=ctk.CTkFont(
    #                     family=Dependency.fontFamily["main"], size=20, weight="bold"
    #                 ),
    #                 corner_radius=8,
    #                 text_color=Dependency.colorPalette["text"],
    #                 fg_color=Dependency.colorPalette["main"],
    #                 hover_color=Dependency.colorPalette["main"],
    #             ).grid(
    #                 row=0,
    #                 column=boxButtonIndex,
    #                 padx=(0, 20) if boxButtonIndex != (len(boxButtonArray) - 1) else 0,
    #                 sticky="nsew",
    #             )


if __name__ == "__main__":
    app = App()
    app.mainloop()

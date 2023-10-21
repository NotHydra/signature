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


class App(ctk.CTk):
    userObject = {
        "_id": 0,
        "name": None,
        "username": None,
        "email": None,
        "role": None,
        "isActive": None,
    }

    def __init__(self) -> None:
        super().__init__()

        self.iconbitmap(Dependency.appIconPath)
        self.title(f"{Dependency.title} - {Dependency.subtitle}")
        self.geometry(
            f"{Dependency.resolution['width']}x{Dependency.resolution['height']}"
        )
        self.resizable(False, False)

        self.loading()

    def forgetFrame(self) -> None:
        for widget in self.winfo_children():
            if "frame" in str(widget):
                widget.grid_forget()

    def logoutEvent(self) -> None:
        self.userObject = {
            "_id": 0,
            "name": None,
            "username": None,
            "email": None,
            "role": None,
            "isActive": None,
        }

        self.forgetFrame()
        self.login()

    def refreshSessionData(self):
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
                self.showError(response["message"])
                self.logoutEvent()

        except:
            self.showError("Server Error")
            self.logoutEvent()

        return False

    def showError(self, message: str) -> None:
        CTkMessagebox(
            corner_radius=8,
            icon="cancel",
            title="Error",
            message=message,
        )

    def showSuccess(self, message: str) -> None:
        CTkMessagebox(
            corner_radius=8,
            icon="check",
            title="Success",
            message=message,
        )

    def showConfirmation(self, message: str = "Are You Sure?") -> None:
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

    def line(self, master, row, column, weight=2):
        ctk.CTkFrame(
            master,
            height=weight,
            corner_radius=0,
            fg_color=Dependency.colorPalette["text"],
        ).grid(row=row, column=column, sticky="nsew")

    def loading(self) -> None:
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

                self.forgetFrame()
                self.login()

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

    def login(self) -> None:
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
                    try:
                        response = requests.post(
                            "http://localhost:8000/api/auth/login",
                            json={"username": username, "password": password},
                        ).json()

                        if response["success"] == True:
                            self.showSuccess(response["message"])

                            self.userObject["_id"] = response["data"]["_id"]

                            self.forgetFrame()
                            self.home()

                        else:
                            self.showError(response["message"])

                    except:
                        self.showError("Server Error")

                else:
                    self.showError("Please Insert Username and Password")

            def exitButtonEvent():
                if self.showConfirmation():
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

            self.forgetFrame()
            self.home()

    def sidebar(self) -> None:
        def contentGroup():
            def brandButtonEvent():
                self.forgetFrame()
                self.home()

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
                    self.forgetFrame()
                    self.home()

                homeSidebarButton = ctk.CTkButton(
                    contentSidebarFrame,
                    height=40,
                    image=ctk.CTkImage(
                        Image.open(Utility.getIcon("house.png")),
                        size=(20, 20),
                    ),
                    text="Home",
                    font=ctk.CTkFont(
                        family=Dependency.fontFamily["main"], size=16, weight="bold"
                    ),
                    cursor="hand2",
                    corner_radius=0,
                    text_color=Dependency.colorPalette["text"],
                    fg_color=Dependency.colorPalette["main"],
                    hover_color=Dependency.colorPalette["main-dark"],
                    command=homeButtonEvent,
                )
                homeSidebarButton.grid(row=4, column=0, sticky="ew")

                if self.userObject["role"] == "user":
                    uploadSidebarButton = ctk.CTkButton(
                        contentSidebarFrame,
                        height=40,
                        image=ctk.CTkImage(
                            Image.open(Utility.getIcon("upload.png")),
                            size=(20, 20),
                        ),
                        text="Upload",
                        font=ctk.CTkFont(
                            family=Dependency.fontFamily["main"],
                            size=16,
                            weight="bold",
                        ),
                        cursor="hand2",
                        corner_radius=0,
                        text_color=Dependency.colorPalette["text"],
                        fg_color=Dependency.colorPalette["main"],
                        hover_color=Dependency.colorPalette["main-dark"],
                    )
                    uploadSidebarButton.grid(row=5, column=0, sticky="ew")

                    downloadSidebarButton = ctk.CTkButton(
                        contentSidebarFrame,
                        height=40,
                        image=ctk.CTkImage(
                            Image.open(Utility.getIcon("download.png")),
                            size=(20, 20),
                        ),
                        text="Download",
                        font=ctk.CTkFont(
                            family=Dependency.fontFamily["main"],
                            size=16,
                            weight="bold",
                        ),
                        cursor="hand2",
                        corner_radius=0,
                        text_color=Dependency.colorPalette["text"],
                        fg_color=Dependency.colorPalette["main"],
                        hover_color=Dependency.colorPalette["main-dark"],
                    )
                    downloadSidebarButton.grid(row=6, column=0, sticky="ew")

                    signSidebarButton = ctk.CTkButton(
                        contentSidebarFrame,
                        height=40,
                        image=ctk.CTkImage(
                            Image.open(Utility.getIcon("sign.png")),
                            size=(20, 20),
                        ),
                        text="Sign",
                        font=ctk.CTkFont(
                            family=Dependency.fontFamily["main"],
                            size=16,
                            weight="bold",
                        ),
                        cursor="hand2",
                        corner_radius=0,
                        text_color=Dependency.colorPalette["text"],
                        fg_color=Dependency.colorPalette["main"],
                        hover_color=Dependency.colorPalette["main-dark"],
                    )
                    signSidebarButton.grid(row=7, column=0, sticky="ew")

                elif self.userObject["role"] == "admin":

                    def userButtonEvent():
                        self.forgetFrame()
                        self.user()

                    userSidebarButton = ctk.CTkButton(
                        contentSidebarFrame,
                        height=40,
                        image=ctk.CTkImage(
                            Image.open(Utility.getIcon("user.png")),
                            size=(20, 20),
                        ),
                        text="User",
                        font=ctk.CTkFont(
                            family=Dependency.fontFamily["main"],
                            size=16,
                            weight="bold",
                        ),
                        cursor="hand2",
                        corner_radius=0,
                        text_color=Dependency.colorPalette["text"],
                        fg_color=Dependency.colorPalette["main"],
                        hover_color=Dependency.colorPalette["main-dark"],
                        command=userButtonEvent,
                    )
                    userSidebarButton.grid(row=5, column=0, sticky="ew")

            contentSidebarFrame = ctk.CTkFrame(
                sidebarFrame,
                corner_radius=0,
                fg_color=Dependency.colorPalette["main"],
            )
            contentSidebarFrame.columnconfigure(0, weight=1)
            contentSidebarFrame.grid(row=0, column=0, sticky="new")

            brandGroup()

            self.line(contentSidebarFrame, 1, 0)

            profileGroup()

            self.line(contentSidebarFrame, 3, 0)

            itemGroup()

        def footerGroup():
            def logoutGroup():
                def logoutButtonEvent():
                    if self.showConfirmation():
                        self.logoutEvent()

                logoutSidebarButton = ctk.CTkButton(
                    footerSidebarFrame,
                    height=40,
                    image=ctk.CTkImage(
                        Image.open(Utility.getIcon("logout.png")),
                        size=(20, 20),
                    ),
                    text="Logout",
                    font=ctk.CTkFont(
                        family=Dependency.fontFamily["main"], size=16, weight="bold"
                    ),
                    cursor="hand2",
                    corner_radius=0,
                    text_color=Dependency.colorPalette["text"],
                    fg_color=Dependency.colorPalette["main"],
                    hover_color=Dependency.colorPalette["main-dark"],
                    command=logoutButtonEvent,
                )
                logoutSidebarButton.grid(row=0, column=0, sticky="ew")

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

            self.line(footerSidebarFrame, 1, 0)

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

    def home(self) -> None:
        if self.refreshSessionData():

            def contentGroup():
                def titleGroup():
                    titleContentLabel = ctk.CTkLabel(
                        contentFrame,
                        text="HOME",
                        font=ctk.CTkFont(
                            family=Dependency.fontFamily["main"],
                            size=36,
                            weight="bold",
                        ),
                        text_color=Dependency.colorPalette["text"],
                    )
                    titleContentLabel.grid(row=0, column=0, pady=5, sticky="nsw")

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

                def containerGroup():
                    def titleGroup():
                        titleContainerLabel = ctk.CTkLabel(
                            containerContentFrame,
                            text="Profile",
                            font=ctk.CTkFont(
                                family=Dependency.fontFamily["main"],
                                size=20,
                                weight="bold",
                            ),
                            text_color=Dependency.colorPalette["text"],
                        )
                        titleContainerLabel.grid(
                            row=0, column=0, padx=10, pady=10, sticky="nsw"
                        )

                    def dataGroup():
                        dataContainerFrame = ctk.CTkFrame(
                            containerContentFrame,
                            corner_radius=0,
                            fg_color="transparent",
                        )
                        dataContainerFrame.columnconfigure([0, 1], weight=1)
                        dataContainerFrame.grid(
                            row=2, column=0, padx=10, pady=(5, 0), sticky="nsew"
                        )

                        # Name
                        nameDataLabel = ctk.CTkLabel(
                            dataContainerFrame,
                            text="Name",
                            font=ctk.CTkFont(
                                family=Dependency.fontFamily["main"],
                                size=20,
                                weight="bold",
                            ),
                            text_color=Dependency.colorPalette["text"],
                        )
                        nameDataLabel.grid(
                            row=0, column=0, padx=(0, 5), pady=(0, 5), sticky="nsw"
                        )

                        nameDataValue = ctk.StringVar()
                        nameDataValue.set(self.userObject["name"])
                        nameDataEntry = ctk.CTkEntry(
                            dataContainerFrame,
                            height=40,
                            placeholder_text="name",
                            textvariable=nameDataValue,
                            font=ctk.CTkFont(
                                family=Dependency.fontFamily["main"],
                                size=20,
                                weight="bold",
                            ),
                            text_color=Dependency.colorPalette["text"],
                            placeholder_text_color=Dependency.colorPalette["text"],
                            fg_color="transparent",
                            border_color=Dependency.colorPalette["text"],
                            state="disabled",
                        )
                        nameDataEntry.grid(
                            row=1, column=0, padx=(0, 5), pady=(0, 10), sticky="nsew"
                        )

                        # Username
                        usernameDataLabel = ctk.CTkLabel(
                            dataContainerFrame,
                            text="Username",
                            font=ctk.CTkFont(
                                family=Dependency.fontFamily["main"],
                                size=20,
                                weight="bold",
                            ),
                            text_color=Dependency.colorPalette["text"],
                        )
                        usernameDataLabel.grid(
                            row=0, column=1, padx=(0, 5), pady=(0, 5), sticky="nsw"
                        )

                        usernameDataValue = ctk.StringVar()
                        usernameDataValue.set(self.userObject["username"])
                        usernameDataEntry = ctk.CTkEntry(
                            dataContainerFrame,
                            height=40,
                            placeholder_text="username",
                            textvariable=usernameDataValue,
                            font=ctk.CTkFont(
                                family=Dependency.fontFamily["main"],
                                size=20,
                                weight="bold",
                            ),
                            text_color=Dependency.colorPalette["text"],
                            placeholder_text_color=Dependency.colorPalette["text"],
                            fg_color="transparent",
                            border_color=Dependency.colorPalette["text"],
                            state="disabled",
                        )
                        usernameDataEntry.grid(
                            row=1, column=1, padx=(5, 0), pady=(0, 10), sticky="nsew"
                        )

                        # Email
                        emailDataLabel = ctk.CTkLabel(
                            dataContainerFrame,
                            text="Email",
                            font=ctk.CTkFont(
                                family=Dependency.fontFamily["main"],
                                size=20,
                                weight="bold",
                            ),
                            text_color=Dependency.colorPalette["text"],
                        )
                        emailDataLabel.grid(
                            row=2, column=0, padx=(0, 5), pady=(0, 5), sticky="nsw"
                        )

                        emailDataValue = ctk.StringVar()
                        emailDataValue.set(self.userObject["email"])
                        emailDataEntry = ctk.CTkEntry(
                            dataContainerFrame,
                            height=40,
                            placeholder_text="email",
                            textvariable=emailDataValue,
                            font=ctk.CTkFont(
                                family=Dependency.fontFamily["main"],
                                size=20,
                                weight="bold",
                            ),
                            text_color=Dependency.colorPalette["text"],
                            placeholder_text_color=Dependency.colorPalette["text"],
                            fg_color="transparent",
                            border_color=Dependency.colorPalette["text"],
                            state="disabled",
                        )
                        emailDataEntry.grid(
                            row=3, column=0, padx=(0, 5), pady=(0, 10), sticky="nsew"
                        )

                        # Role
                        roleDataLabel = ctk.CTkLabel(
                            dataContainerFrame,
                            text="Role",
                            font=ctk.CTkFont(
                                family=Dependency.fontFamily["main"],
                                size=20,
                                weight="bold",
                            ),
                            text_color=Dependency.colorPalette["text"],
                        )
                        roleDataLabel.grid(
                            row=2, column=1, padx=(0, 5), pady=(0, 5), sticky="nsw"
                        )

                        roleDataValue = ctk.StringVar()
                        roleDataValue.set(self.userObject["role"].capitalize())
                        roleDataEntry = ctk.CTkEntry(
                            dataContainerFrame,
                            height=40,
                            placeholder_text="role",
                            textvariable=roleDataValue,
                            font=ctk.CTkFont(
                                family=Dependency.fontFamily["main"],
                                size=20,
                                weight="bold",
                            ),
                            text_color=Dependency.colorPalette["text"],
                            placeholder_text_color=Dependency.colorPalette["text"],
                            fg_color="transparent",
                            border_color=Dependency.colorPalette["text"],
                            state="disabled",
                        )
                        roleDataEntry.grid(
                            row=3, column=1, padx=(5, 0), pady=(0, 10), sticky="nsew"
                        )

                        # Button
                        changeDataButton = ctk.CTkButton(
                            dataContainerFrame,
                            height=40,
                            image=ctk.CTkImage(
                                Image.open(Utility.getIcon("change.png")),
                                size=(24, 24),
                            ),
                            text="Change",
                            font=ctk.CTkFont(
                                family=Dependency.fontFamily["main"],
                                size=20,
                                weight="bold",
                            ),
                            cursor="hand2",
                            corner_radius=8,
                            text_color=Dependency.colorPalette["text"],
                            fg_color=Dependency.colorPalette["warning"],
                            hover_color=Dependency.colorPalette["warning-dark"],
                        )
                        changeDataButton.grid(
                            row=4,
                            column=0,
                            padx=(0, 5),
                            sticky="nsew",
                        )

                        changePasswordDataButton = ctk.CTkButton(
                            dataContainerFrame,
                            height=40,
                            image=ctk.CTkImage(
                                Image.open(Utility.getIcon("password.png")),
                                size=(24, 24),
                            ),
                            text="Change Password",
                            font=ctk.CTkFont(
                                family=Dependency.fontFamily["main"],
                                size=20,
                                weight="bold",
                            ),
                            cursor="hand2",
                            corner_radius=8,
                            text_color=Dependency.colorPalette["text"],
                            fg_color=Dependency.colorPalette["danger"],
                            hover_color=Dependency.colorPalette["danger-dark"],
                        )
                        changePasswordDataButton.grid(
                            row=4,
                            column=1,
                            padx=(5, 0),
                            sticky="nsew",
                        )

                    containerContentFrame = ctk.CTkFrame(
                        contentFrame,
                        corner_radius=8,
                        fg_color=Dependency.colorPalette["main"],
                    )
                    containerContentFrame.columnconfigure(0, weight=1)
                    containerContentFrame.grid(
                        row=2, column=0, pady=(0, 20), sticky="nsew"
                    )

                    titleGroup()

                    self.line(containerContentFrame, row=1, column=0)

                    dataGroup()

                contentFrame = ctk.CTkFrame(
                    self, corner_radius=0, fg_color="transparent"
                )
                contentFrame.rowconfigure(2, weight=1)
                contentFrame.columnconfigure(0, weight=1)
                contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

                titleGroup()
                welcomeGroup()
                containerGroup()

            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=31)

            self.sidebar()
            contentGroup()

    def user(self) -> None:
        if self.refreshSessionData():
            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=31)

            self.sidebar()

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

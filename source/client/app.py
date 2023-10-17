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


class Dependency:
    title = "Signature"
    subTitle = "Online Document Application"

    resolution = {"width": 1200, "height": 700}
    logoResolution = {"width": 639, "height": 799}

    path = os.path.dirname(os.path.realpath(__file__))
    iconPath = "./source/asset/icon.ico"
    logoPath = Utility.combinePath(path, "..\\asset\\logo.png")

    fontFamily = {"main": "Montserrat"}
    colorPalette = {
        "main": "#54A4F5",
        "main-dark": "#2976C4",
        "text": "#FFFFFF",
        "danger": "#DC143C",
        "danger-dark": "#8B0000",
    }

    skip = True


class App(ctk.CTk):
    userId = 0

    def __init__(self) -> None:
        super().__init__()

        self.iconbitmap(Dependency.iconPath)
        self.title(f"{Dependency.title} - {Dependency.subTitle}")
        self.geometry(
            f"{Dependency.resolution['width']}x{Dependency.resolution['height']}"
        )
        self.resizable(False, False)

        self.loading()

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

    def line(self, master, row, column, weight=2):
        ctk.CTkFrame(
            master,
            height=weight,
            corner_radius=0,
            fg_color=Dependency.colorPalette["text"],
        ).grid(row=row, column=column, sticky="nsew")

    def loading(self) -> None:
        def increaseLoadingValue() -> None:
            if not Dependency.skip:
                loadingValue = 0
                while loadingValue < 1:
                    loadingValue += random.uniform(0.005, 0.01)
                    progressLoadingTextProgressBar.set(loadingValue)

                    self.update()
                    time.sleep(0.00001)

            loadingFrame.grid_forget()
            self.login()

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        loadingFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        loadingFrame.rowconfigure(0, weight=1)
        loadingFrame.columnconfigure([0, 1], weight=1)
        loadingFrame.grid(row=0, column=0)

        logoLoadingImage = ctk.CTkImage(
            Image.open(Dependency.logoPath),
            size=(
                Dependency.logoResolution["width"] / 4,
                Dependency.logoResolution["height"] / 4,
            ),
        )
        logoLoadingLabel = ctk.CTkLabel(
            loadingFrame,
            image=logoLoadingImage,
            text="",
        )
        logoLoadingLabel.grid(row=0, column=0, padx=20)

        loadingTextFrame = ctk.CTkFrame(
            loadingFrame, corner_radius=0, fg_color="transparent"
        )
        loadingTextFrame.rowconfigure([0, 1, 2], weight=1)
        loadingTextFrame.columnconfigure(0, weight=1)
        loadingTextFrame.grid(row=0, column=1, padx=20)

        titleLoadingTextLabel = ctk.CTkLabel(
            loadingTextFrame,
            text=Dependency.title.upper(),
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=80,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"],
        )
        titleLoadingTextLabel.grid(row=0, column=0, sticky="ew")

        subTitleLoadingTextLabel = ctk.CTkLabel(
            loadingTextFrame,
            text=Dependency.subTitle.upper(),
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=27,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"],
        )
        subTitleLoadingTextLabel.grid(row=1, column=0, sticky="ew")

        progressLoadingTextProgressBar = ctk.CTkProgressBar(
            loadingTextFrame,
            orientation="horizontal",
            mode="determinate",
            progress_color=Dependency.colorPalette["main"],
        )
        progressLoadingTextProgressBar.grid(row=2, column=0, pady=10, sticky="ew")
        progressLoadingTextProgressBar.set(0)

        self.after(500, increaseLoadingValue)

    def login(self) -> None:
        def authenticate():
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

                        self.userId = response["data"]["_id"]

                        aboutFrame.grid_forget()
                        loginFrame.grid_forget()
                        self.main()

                    else:
                        self.showError(response["message"])

                except:
                    self.showError("Server Error")

            else:
                self.showError("Please Insert Username and Password")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        aboutFrame = ctk.CTkFrame(
            self, corner_radius=0, fg_color=Dependency.colorPalette["main"]
        )
        aboutFrame.rowconfigure(0, weight=1)
        aboutFrame.columnconfigure(0, weight=1)
        aboutFrame.grid(row=0, column=0, sticky="nsew")

        backgroundAboutImage = ctk.CTkImage(
            Image.open(
                Utility.combinePath(Dependency.path, "../asset/logo-opacity.png")
            ),
            size=(
                Dependency.logoResolution["width"] / 2,
                Dependency.logoResolution["height"] / 2,
            ),
        )
        descriptionAboutLabel = ctk.CTkLabel(
            aboutFrame,
            image=backgroundAboutImage,
            text="SIGNATURE\ndesktop-based application\nthat is capable of digitally\nmanaging multiple kinds of\ndocument online. Such as\nuploading, downloading and\nsigning digital documents.",
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
            command=authenticate,
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
            command=lambda: self.quit(),
        )
        exitLoginButton.grid(row=4, column=0)

        if Dependency.skip:
            self.userId = 2

            aboutFrame.grid_forget()
            loginFrame.grid_forget()
            self.main()

    def main(self) -> None:
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=31)

        sidebarFrame = ctk.CTkFrame(
            self, corner_radius=0, fg_color=Dependency.colorPalette["main"]
        )
        sidebarFrame.columnconfigure(0, weight=1)
        sidebarFrame.grid(row=0, column=0, sticky="nsew")

        brandSidebarButton = ctk.CTkButton(
            sidebarFrame,
            height=80,
            text="Signature",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=28, weight="bold"
            ),
            cursor="hand2",
            corner_radius=0,
            text_color=Dependency.colorPalette["text"],
            fg_color=Dependency.colorPalette["main"],
            hover_color=Dependency.colorPalette["main-dark"],
        )
        brandSidebarButton.grid(row=0, column=0, sticky="nsew")

        self.line(sidebarFrame, 1, 0)


if __name__ == "__main__":
    app = App()
    app.mainloop()

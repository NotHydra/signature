import os
import random
import time
import customtkinter as ctk

from PIL import Image


class Utility:
    def combinePath(base, path):
        return os.path.join(base, path)


class Dependency:
    title = "Signature"
    subTitle = "Online Mail"

    resolution = {"width": 1000, "height": 600}
    logoResolution = {"width": 639, "height": 799}

    path = os.path.dirname(os.path.realpath(__file__))
    iconPath = "./source/asset/icon.ico"
    logoPath = Utility.combinePath(path, "..\\asset\\logo.png")

    fontFamily = {"main": "DM SANS"}
    colorPalette = {"main": "#54A4F5"}

    loading = False


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.iconbitmap(Dependency.iconPath)
        self.title(f"{Dependency.title} - {Dependency.subTitle}")
        self.geometry(
            f"{Dependency.resolution['width']}x{Dependency.resolution['height']}"
        )
        self.resizable(False, False)

        self.loading()

    def loading(self):
        def increaseLoadingValue():
            if Dependency.loading:
                loadingValue = 0
                while loadingValue < 1:
                    loadingValue += random.uniform(0.005, 0.01)
                    self.progressLoadingTextProgressBar.set(loadingValue)

                    self.update()
                    time.sleep(0.00001)

            self.loadingFrame.forget()
            self.login()

        self.loadingFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.loadingFrame.pack(expand=True)

        self.logoLoadingImage = ctk.CTkImage(
            Image.open(Dependency.logoPath),
            size=(
                Dependency.logoResolution["width"] / 4,
                Dependency.logoResolution["height"] / 4,
            ),
        )
        self.logoLoadingLabel = ctk.CTkLabel(
            self.loadingFrame, image=self.logoLoadingImage, text=""
        )
        self.logoLoadingLabel.grid(row=0, column=0, padx=20)

        self.loadingTextFrame = ctk.CTkFrame(
            self.loadingFrame, corner_radius=0, fg_color="transparent"
        )
        self.loadingTextFrame.grid(row=0, column=1, padx=20)

        self.titleLoadingTextLabel = ctk.CTkLabel(
            self.loadingTextFrame,
            text=Dependency.title.upper(),
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=80, weight="bold"
            ),
        )
        self.titleLoadingTextLabel.grid(row=0, column=0)

        self.progressLoadingTextProgressBar = ctk.CTkProgressBar(
            self.loadingTextFrame,
            orientation="horizontal",
            mode="determinate",
            progress_color=Dependency.colorPalette["main"],
        )
        self.progressLoadingTextProgressBar.grid(row=1, column=0, sticky="ew")
        self.progressLoadingTextProgressBar.set(0)

        self.after(500, increaseLoadingValue)

    def login(self):
        self.loginFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.loginFrame.pack(expand=True)

        self.titleLoginLabel = ctk.CTkLabel(
            self.loginFrame,
            text=Dependency.title.upper(),
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=40, weight="bold"
            ),
        )
        self.titleLoginLabel.grid(row=0, column=0, pady=(0, 5))

        self.usernameLoginEntry = ctk.CTkEntry(
            self.loginFrame,
            width=250,
            height=40,
            placeholder_text="username",
            justify="center",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
        )
        self.usernameLoginEntry.grid(row=1, column=0, pady=(0, 5))

        self.passwordLoginEntry = ctk.CTkEntry(
            self.loginFrame,
            width=250,
            height=40,
            show="*",
            placeholder_text="password",
            justify="center",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
        )
        self.passwordLoginEntry.grid(row=2, column=0, pady=(0, 10))

        self.loginLoginButton = ctk.CTkButton(
            self.loginFrame,
            text="Login",
            width=250,
            height=40,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=25, weight="bold"
            ),
        )
        self.loginLoginButton.grid(row=3, column=0)


if __name__ == "__main__":
    app = App()
    app.mainloop()

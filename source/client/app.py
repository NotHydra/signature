import os
import random
import time
import customtkinter as ctk

from PIL import Image


class Dependency:
    title = "Signature"
    subTitle = "Online Mail"
    resolution = {"width": 1000, "height": 600}

    path = os.path.dirname(os.path.realpath(__file__))

    logoResolution = {"width": 639, "height": 799}


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.iconbitmap("./source/asset/icon.ico")
        self.title(f"{Dependency.title} - {Dependency.subTitle}")
        self.geometry(
            f"{Dependency.resolution['width']}x{Dependency.resolution['height']}"
        )
        self.resizable(False, False)

        self.loading()

    def loading(self):
        def increaseLoadingValue():
            loadingValue = 0
            while loadingValue < 1:
                loadingValue += random.uniform(0.005, 0.01)
                self.progressLoadingTextProgressBar.set(loadingValue)

                self.update()
                time.sleep(0.00001)

            self.loadingFrame.forget()

        self.loadingFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.loadingFrame.pack(expand=True)

        self.logoLoadingImage = ctk.CTkImage(
            Image.open(Dependency.path + "\\..\\asset\\logo.png"),
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
            font=ctk.CTkFont(family="DM SANS", size=80, weight="bold"),
        )
        self.titleLoadingTextLabel.grid(row=0, column=0)

        self.progressLoadingTextProgressBar = ctk.CTkProgressBar(
            self.loadingTextFrame,
            orientation="horizontal",
            mode="determinate",
            progress_color="#54A4F5",
        )
        self.progressLoadingTextProgressBar.grid(row=1, column=0, sticky="ew")
        self.progressLoadingTextProgressBar.set(0)

        self.after(500, increaseLoadingValue)


if __name__ == "__main__":
    app = App()
    app.mainloop()

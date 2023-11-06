import os
import random
import time
from typing import Callable

import customtkinter as ctk
import requests
from CTkMessagebox import CTkMessagebox
from PIL import Image


class Utility:
    def combinePath(base: str, path: str) -> str:
        return os.path.join(base, path)

    def getAsset(file: str) -> str:
        return Utility.combinePath(Dependency.assetPath, file)

    def getIcon(file: str) -> str:
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
        "background": "#242424",
        "text": "#FFFFFF",
        "text-dark": "#F2F3F4",
        "success": "#2ECC71",
        "success-dark": "#28B463",
        "warning": "#F1C40F",
        "warning-dark": "#D4AC0D",
        "danger": "#E74C3C",
        "danger-dark": "#CB4335",
    }

    skip = True


class Message:
    def errorMessage(message: str) -> None:
        CTkMessagebox(
            corner_radius=8,
            icon="cancel",
            title="Error",
            message=message,
        )

    def successMessage(message: str) -> None:
        CTkMessagebox(
            corner_radius=8,
            icon="check",
            title="Success",
            message=message,
        )

    def confirmationMessage(message: str = "Are You Sure?") -> bool:
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


class Call:
    def resetFrameCall() -> None:
        app.rowconfigure([0, 1, 2, 3, 4], weight=0)
        app.columnconfigure([0, 1, 2, 3, 4], weight=0)

        for widget in app.winfo_children():
            if "frame" in str(widget):
                widget.grid_forget()

    def logoutCall() -> None:
        app.userObject = {
            "_id": 0,
            "name": None,
            "username": None,
            "email": None,
            "role": None,
            "isActive": None,
        }

        Call.resetFrameCall()
        app.loginFrame()


class Component:
    def lineHorizontalComponent(
        master: ctk.CTk | ctk.CTkFrame, row: int, weight: int = 2
    ) -> None:
        ctk.CTkFrame(
            master,
            width=0,
            height=weight,
            corner_radius=0,
            fg_color=Dependency.colorPalette["text"],
        ).grid(row=row, column=0, sticky="nsew")

    def lineVerticalComponent(
        master: ctk.CTk | ctk.CTkFrame,
        row: int = 0,
        column: int = 0,
        weight: int = 2,
    ) -> None:
        ctk.CTkFrame(
            master,
            width=weight,
            height=0,
            corner_radius=0,
            fg_color=Dependency.colorPalette["text"],
        ).grid(row=row, column=column, sticky="nsew")

    def sidebarComponent() -> None:
        def homeButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(app.homeFrame)

        def logoutButtonEvent() -> None:
            if Message.confirmationMessage():
                Call.logoutCall()

        def sidebarButtonComponent(
            master,
            title: str,
            icon: str,
            event: any,
            row: int,
            highlight: bool = False,
        ) -> None:
            ctk.CTkButton(
                master,
                height=40,
                image=ctk.CTkImage(
                    Image.open(Utility.getIcon(f"{icon}.png")),
                    size=(20, 20),
                ),
                text=title,
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"], size=16, weight="bold"
                ),
                cursor="hand2",
                corner_radius=0,
                text_color=Dependency.colorPalette["text"],
                fg_color=Dependency.colorPalette["main-dark"]
                if highlight
                else Dependency.colorPalette["main"],
                hover_color=Dependency.colorPalette["main-dark"],
                command=event,
            ).grid(row=row, column=0, sticky="ew")

        sidebarFrame = ctk.CTkFrame(
            app, corner_radius=0, fg_color=Dependency.colorPalette["main"]
        )
        sidebarFrame.rowconfigure(0, weight=15)
        sidebarFrame.rowconfigure(1, weight=1)
        sidebarFrame.columnconfigure(0, weight=1)
        sidebarFrame.grid(row=0, column=0, sticky="nsew")

        contentSidebarFrame = ctk.CTkFrame(
            sidebarFrame,
            corner_radius=0,
            fg_color=Dependency.colorPalette["main"],
        )
        contentSidebarFrame.columnconfigure(0, weight=1)
        contentSidebarFrame.grid(row=0, column=0, sticky="new")

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
            command=homeButtonEvent,
        )
        brandSidebarButton.grid(row=0, column=0, sticky="ew")

        Component.lineHorizontalComponent(contentSidebarFrame, 1)

        profileSidebarFrame = ctk.CTkFrame(
            contentSidebarFrame, corner_radius=0, fg_color="transparent"
        )
        profileSidebarFrame.rowconfigure(0, weight=1)
        profileSidebarFrame.columnconfigure([0, 1], weight=1)
        profileSidebarFrame.grid(row=2, column=0, sticky="ew")

        roleProfileImage = ctk.CTkLabel(
            profileSidebarFrame,
            image=ctk.CTkImage(
                Image.open(Utility.getIcon(f"{app.userObject['role']}.png")),
                size=(32, 32),
            ),
            text="",
        )
        roleProfileImage.grid(row=0, column=0, padx=10, rowspan=2, sticky="e")

        usernameProfileLabel = ctk.CTkLabel(
            profileSidebarFrame,
            text=app.userObject["username"],
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
            text_color=Dependency.colorPalette["text"],
        )
        usernameProfileLabel.grid(row=0, column=1, padx=10, sticky="w")

        roleProfileLabel = ctk.CTkLabel(
            profileSidebarFrame,
            text=str(app.userObject["role"]).upper(),
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=12, weight="bold"
            ),
            text_color=Dependency.colorPalette["text"],
        )
        roleProfileLabel.grid(row=1, column=1, padx=10, sticky="w")

        Component.lineHorizontalComponent(contentSidebarFrame, 3)

        sidebarButtonComponent(
            contentSidebarFrame,
            title="Home",
            icon="house",
            event=homeButtonEvent,
            row=4,
            highlight=True if app.sidebarId == 1 else False,
        )

        if app.userObject["role"] == "user":
            sidebarButtonComponent(
                contentSidebarFrame,
                title="Upload",
                icon="upload",
                event=lambda: None,
                row=5,
                highlight=True if app.sidebarId == 2 else False,
            )
            sidebarButtonComponent(
                contentSidebarFrame,
                title="Download",
                icon="download",
                event=lambda: None,
                row=6,
                highlight=True if app.sidebarId == 3 else False,
            )
            sidebarButtonComponent(
                contentSidebarFrame,
                title="Sign",
                icon="sign",
                event=lambda: None,
                row=7,
                highlight=True if app.sidebarId == 4 else False,
            )

        elif app.userObject["role"] == "admin":

            def userButtonEvent() -> None:
                Call.resetFrameCall()
                Middleware.refreshSessionDataMiddleware(app.userFrame)

            sidebarButtonComponent(
                contentSidebarFrame,
                title="User",
                icon="user",
                event=userButtonEvent,
                row=5,
                highlight=True if app.sidebarId == 2 else False,
            )

        footerSidebarFrame = ctk.CTkFrame(
            sidebarFrame,
            corner_radius=0,
            fg_color=Dependency.colorPalette["main"],
        )
        footerSidebarFrame.columnconfigure(0, weight=1)
        footerSidebarFrame.grid(row=1, column=0, sticky="sew")

        sidebarButtonComponent(
            footerSidebarFrame,
            title="Logout",
            icon="logout",
            event=logoutButtonEvent,
            row=0,
        )

        Component.lineHorizontalComponent(footerSidebarFrame, 1)

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

    def titleContentComponent(
        master: ctk.CTk | ctk.CTkFrame, title: str, row: int
    ) -> None:
        titleFrame = ctk.CTkFrame(
            master, corner_radius=8, fg_color=Dependency.colorPalette["main"]
        )
        titleFrame.grid(row=row, column=0, pady=20, sticky="ew")

        ctk.CTkLabel(
            titleFrame,
            text=title,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=30,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"],
        ).grid(row=row, column=0, padx=10, sticky="nsw")

    def boxContentComponent(
        master: ctk.CTk | ctk.CTkFrame, boxArray: list[dict[str, any]], row: int
    ) -> None:
        boxFrame = ctk.CTkFrame(
            master,
            height=80,
            corner_radius=0,
            fg_color="transparent",
        )
        boxFrame.rowconfigure(0, weight=1)
        boxFrame.columnconfigure([0, 1, 2], weight=1)
        boxFrame.grid(row=row, column=0, pady=(0, 20), sticky="nsew")

        for boxButtonIndex, boxButtonObject in enumerate(boxArray):
            ctk.CTkButton(
                boxFrame,
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
                padx=(0, 20) if boxButtonIndex != (len(boxArray) - 1) else 0,
                sticky="nsew",
            )

    def titleContainerComponent(
        master: ctk.CTk | ctk.CTkFrame, title: str, row: int
    ) -> None:
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

    def entryDataComponent(
        master: ctk.CTk | ctk.CTkFrame,
        title: str,
        placeholder: str,
        value: str,
        state: bool,
        row: int,
        column: int,
        show: str = "",
    ) -> ctk.CTkEntry:
        def focusIn(event):
            if entryObject.get() == placeholder:
                entryObject.delete(0, ctk.END)
                entryObject.configure(
                    show=show, text_color=Dependency.colorPalette["text"]
                )

        def focusOut(event):
            if entryObject.get() == "":
                entryObject.insert(0, placeholder)
                entryObject.configure(
                    show="", text_color=Dependency.colorPalette["text-dark"]
                )

        entryFrame = ctk.CTkFrame(master, corner_radius=0, fg_color="transparent")
        entryFrame.rowconfigure([0, 1], weight=1)
        entryFrame.columnconfigure(0, weight=1)
        entryFrame.grid(row=row, column=column, sticky="nsew")

        ctk.CTkLabel(
            entryFrame,
            text=title,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=18,
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
        entryValue.set(value if value != None else placeholder)

        entryObject = ctk.CTkEntry(
            entryFrame,
            height=36,
            textvariable=entryValue,
            show=show if value != None else "",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=18,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"]
            if value != None
            else Dependency.colorPalette["text-dark"],
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

        entryObject.bind("<FocusIn>", focusIn)
        entryObject.bind("<FocusOut>", focusOut)

        return entryObject

    def buttonDataComponent(
        master: ctk.CTk | ctk.CTkFrame,
        text: str,
        icon: str,
        mainColor: str,
        hoverColor: str,
        event: any,
        row: int,
    ) -> None:
        ctk.CTkButton(
            master,
            height=36,
            image=ctk.CTkImage(
                Image.open(Utility.getIcon(f"{icon}.png")),
                size=(22, 22),
            ),
            text=text,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=18,
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

    def tableDataComponent(
        master: ctk.CTk | ctk.CTkFrame,
        row: int,
        contentArray: list[dict[str, any]],
        idArray: list[int] = None,
        actionArray: list[dict[str, any]] = None,
        numbering: bool = True,
    ) -> None:
        tableFrame = ctk.CTkFrame(
            master, height=0, corner_radius=0, fg_color="transparent"
        )
        tableFrame.columnconfigure(0, weight=1)
        tableFrame.grid(row=row, column=0, padx=20, pady=20, sticky="nsew")

        Component.lineHorizontalComponent(tableFrame, row=0)

        headerTableFrame = ctk.CTkFrame(
            tableFrame, height=0, corner_radius=0, fg_color="transparent"
        )
        headerTableFrame.rowconfigure(0, weight=1)
        headerTableFrame.columnconfigure(
            [((i * 2) + 3) for i, _ in enumerate(contentArray[1:])]
            if numbering
            else [((i * 2) + 1) for i, _ in enumerate(contentArray)],
            weight=4,
        )
        headerTableFrame.grid(row=1, column=0, sticky="nsew")

        Component.lineVerticalComponent(headerTableFrame, column=0)

        for contentIndex, contentObject in enumerate(contentArray):
            dataHeaderFrame = ctk.CTkFrame(
                headerTableFrame,
                width=0,
                height=0,
                corner_radius=0,
                fg_color="transparent",
            )
            dataHeaderFrame.columnconfigure(0, weight=1)
            dataHeaderFrame.grid(row=0, column=(contentIndex * 2) + 1, sticky="nsew")

            ctk.CTkLabel(
                dataHeaderFrame,
                text=contentObject["header"],
                text_color=Dependency.colorPalette["text"],
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=12,
                    weight="bold",
                ),
                fg_color="transparent",
                bg_color="transparent",
            ).grid(row=0, column=0, padx=5, sticky="nsew")

            Component.lineHorizontalComponent(dataHeaderFrame, row=1)

            for dataIndex, dataObject in enumerate(contentObject["data"]):
                ctk.CTkLabel(
                    dataHeaderFrame,
                    text=dataObject,
                    text_color=Dependency.colorPalette["text"],
                    font=ctk.CTkFont(
                        family=Dependency.fontFamily["main"],
                        size=12,
                        weight="bold",
                    ),
                    fg_color="transparent",
                    bg_color="transparent",
                ).grid(
                    row=2 + (dataIndex * 2),
                    column=0,
                    padx=5,
                    sticky="nsew"
                    if contentObject["align"] == "center"
                    else "nsw"
                    if contentObject["align"] == "left"
                    else "nse",
                )

                Component.lineHorizontalComponent(
                    dataHeaderFrame, row=2 + (dataIndex * 2) + 1
                )

            Component.lineVerticalComponent(
                headerTableFrame, column=(contentIndex * 2) + 2
            )

        if actionArray != None:
            actionHeaderFrame = ctk.CTkFrame(
                headerTableFrame,
                width=0,
                height=0,
                corner_radius=0,
                fg_color="transparent",
            )
            actionHeaderFrame.columnconfigure(0, weight=1)
            actionHeaderFrame.grid(
                row=0, column=(len(contentArray) * 2) + 1, sticky="nsew"
            )

            ctk.CTkLabel(
                actionHeaderFrame,
                text="Action",
                text_color=Dependency.colorPalette["text"],
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=12,
                    weight="bold",
                ),
                fg_color="transparent",
                bg_color="transparent",
            ).grid(row=0, column=0, padx=5, sticky="nsew")

            Component.lineHorizontalComponent(actionHeaderFrame, row=1)

            for idIndex, idObject in enumerate(idArray):
                buttonActionFrame = ctk.CTkFrame(
                    actionHeaderFrame, width=0, corner_radius=0, fg_color="transparent"
                )
                buttonActionFrame.columnconfigure(0, weight=1)
                buttonActionFrame.grid(row=(idIndex * 2) + 2, column=0, sticky="nsew")

                for actionIndex, actionObject in enumerate(actionArray):
                    ctk.CTkButton(
                        buttonActionFrame,
                        width=0,
                        height=14,
                        image=ctk.CTkImage(
                            Image.open(Utility.getIcon(f"{actionObject['icon']}.png")),
                            size=(14, 14),
                        ),
                        text=f'{actionObject["text"]}',
                        font=ctk.CTkFont(
                            family=Dependency.fontFamily["main"],
                            size=14,
                            weight="bold",
                        ),
                        cursor="hand2",
                        corner_radius=8,
                        text_color=Dependency.colorPalette["text"],
                        fg_color=actionObject["mainColor"],
                        hover_color=actionObject["hoverColor"],
                        command=lambda event=actionObject["event"], id=idObject: event(
                            id
                        ),
                    ).grid(
                        row=0,
                        column=actionIndex,
                        padx=1,
                        pady=1,
                        sticky="nsew",
                    )

                Component.lineHorizontalComponent(
                    actionHeaderFrame, row=(idIndex * 2) + 3
                )

            Component.lineVerticalComponent(
                headerTableFrame, column=(len(contentArray) * 2) + 2
            )

    def labelDataComponent(
        master: ctk.CTk | ctk.CTkFrame,
        text: str,
        size: int = 16,
        row: int = 0,
        padx: int = 10,
        pady: int = 10,
    ) -> None:
        ctk.CTkLabel(
            master,
            text=text,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=size,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"],
        ).grid(row=row, column=0, padx=padx, pady=pady, sticky="nsew")


class Middleware:
    def refreshSessionDataMiddleware(
        frameFunction: Callable[[], None], tag=None
    ) -> None:
        def fetchSessionData() -> None:
            response = None
            try:
                response = requests.get(
                    f"http://localhost:8000/api/user/{app.userObject['_id']}"
                ).json()

            except requests.ConnectionError:
                Message.errorMessage("Make Sure You Are Connected To The Internet")
                Call.logoutCall()

            except:
                Message.errorMessage("Server Error")
                Call.logoutCall()

            if response != None:
                if response["success"] == True:
                    app.userObject["name"] = response["data"]["name"]
                    app.userObject["username"] = response["data"]["username"]
                    app.userObject["email"] = response["data"]["email"]
                    app.userObject["role"] = response["data"]["role"]
                    app.userObject["isActive"] = response["data"]["isActive"]

                    Call.resetFrameCall()

                    if tag == None:
                        frameFunction()

                    elif tag != None:
                        frameFunction(tag)

                else:
                    Message.errorMessage(response["message"])
                    Call.logoutCall()

        app.rowconfigure(0, weight=1)
        app.columnconfigure(0, weight=1)

        loadingFrame = ctk.CTkFrame(app, corner_radius=0, fg_color="transparent")
        loadingFrame.rowconfigure(0, weight=1)
        loadingFrame.columnconfigure(0, weight=1)
        loadingFrame.grid(row=0, column=0)

        logoLoadingImage = ctk.CTkLabel(
            loadingFrame,
            image=ctk.CTkImage(
                Image.open(Utility.getAsset("logo.png")),
                size=(
                    Dependency.logoResolution["width"] / 6,
                    Dependency.logoResolution["height"] / 6,
                ),
            ),
            text="",
        )
        logoLoadingImage.grid(row=0, column=0, padx=20)

        titleLoadingLabel = ctk.CTkLabel(
            loadingFrame,
            text="Loading",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=60,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"],
        )
        titleLoadingLabel.grid(row=0, column=1, padx=20)

        app.after(50, fetchSessionData)


class App(ctk.CTk):
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

        xOffset = (self.winfo_screenwidth() // 2) - (
            Dependency.resolution["width"] // 2
        )
        yOffset = (self.winfo_screenheight() // 2) - (
            Dependency.resolution["height"] // 2
        )
        self.geometry(
            f"{Dependency.resolution['width']}x{Dependency.resolution['height']}+{xOffset}+{yOffset}"
        )
        self.minsize(Dependency.resolution["width"], Dependency.resolution["height"])

        self.configure(fg_color=Dependency.colorPalette["background"])

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

            Call.resetFrameCall()
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

            if "" not in [username, password]:
                response = None
                try:
                    response = requests.post(
                        "http://localhost:8000/api/auth/login",
                        json={"username": username, "password": password},
                    ).json()

                except requests.ConnectionError:
                    Message.errorMessage("Make Sure You Are Connected To The Internet")

                except:
                    Message.errorMessage("Server Error")

                if response != None:
                    if response["success"] == True:
                        Message.successMessage(response["message"])

                        self.userObject["_id"] = response["data"]["_id"]

                        Call.resetFrameCall()
                        Middleware.refreshSessionDataMiddleware(self.homeFrame)

                    else:
                        Message.errorMessage(response["message"])

            else:
                Message.errorMessage("Please Fill Out The Form")

        def exitButtonEvent() -> None:
            if Message.confirmationMessage():
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

            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.homeFrame)

    def homeFrame(self) -> None:
        def changeButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.homeChangeFrame)

        def changePasswordButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.homeChangePasswordFrame)

        self.sidebarId = 1

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=31)

        Component.sidebarComponent()

        contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        contentFrame.rowconfigure(2, weight=1)
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

        Component.titleContentComponent(contentFrame, title="HOME", row=0)

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

        Component.titleContainerComponent(containerContentFrame, title="Profile", row=0)
        Component.lineHorizontalComponent(containerContentFrame, row=1)

        dataContainerFrame = ctk.CTkFrame(
            containerContentFrame,
            corner_radius=0,
            fg_color="transparent",
        )
        dataContainerFrame.columnconfigure([0, 1], weight=1)
        dataContainerFrame.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="nsew")

        Component.entryDataComponent(
            dataContainerFrame,
            title="Name",
            placeholder="name",
            value=self.userObject["name"],
            state=False,
            row=0,
            column=0,
        )
        Component.entryDataComponent(
            dataContainerFrame,
            title="Username",
            placeholder="username",
            value=self.userObject["username"],
            state=False,
            row=0,
            column=1,
        )

        Component.entryDataComponent(
            dataContainerFrame,
            title="Email",
            placeholder="email",
            value=self.userObject["email"],
            state=False,
            row=1,
            column=0,
        )
        Component.entryDataComponent(
            dataContainerFrame,
            title="Role",
            placeholder="role",
            value=self.userObject["role"].capitalize(),
            state=False,
            row=1,
            column=1,
        )

        Component.buttonDataComponent(
            dataContainerFrame,
            text="Change",
            icon="change",
            mainColor=Dependency.colorPalette["warning"],
            hoverColor=Dependency.colorPalette["warning-dark"],
            event=changeButtonEvent,
            row=2,
        )
        Component.buttonDataComponent(
            dataContainerFrame,
            text="Change Password",
            icon="password",
            mainColor=Dependency.colorPalette["danger"],
            hoverColor=Dependency.colorPalette["danger-dark"],
            event=changePasswordButtonEvent,
            row=3,
        )

    def homeChangeFrame(self) -> None:
        def changeButtonEvent() -> None:
            if Message.confirmationMessage():
                name = nameDataEntry.get()
                username = usernameDataEntry.get()
                email = emailDataEntry.get()

                if "" not in [name, username, email]:
                    response = None
                    try:
                        response = requests.put(
                            f"http://localhost:8000/api/user/update/{self.userObject['_id']}",
                            json={
                                "name": name,
                                "username": username,
                                "email": email,
                                "role": self.userObject["role"],
                            },
                        ).json()

                    except requests.ConnectionError:
                        Message.errorMessage(
                            "Make Sure You Are Connected To The Internet"
                        )

                    except:
                        Message.errorMessage("Server Error")

                    if response != None:
                        if response["success"] == True:
                            Message.successMessage(response["message"])

                            Call.resetFrameCall()
                            Middleware.refreshSessionDataMiddleware(
                                self.homeChangeFrame
                            )

                        else:
                            Message.errorMessage(response["message"])

                            if response["status"] == 404:
                                Call.logoutCall()

                else:
                    Message.errorMessage("Please Fill Out The Form")

        def backButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.homeFrame)

        self.sidebarId = 1

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=31)

        Component.sidebarComponent()

        contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

        Component.titleContentComponent(contentFrame, title="HOME", row=0)

        containerContentFrame = ctk.CTkFrame(
            contentFrame,
            corner_radius=8,
            fg_color=Dependency.colorPalette["main"],
        )
        containerContentFrame.columnconfigure(0, weight=1)
        containerContentFrame.grid(row=1, column=0, pady=(0, 20), sticky="nsew")

        Component.titleContainerComponent(
            containerContentFrame, title="Change Profile", row=0
        )
        Component.lineHorizontalComponent(containerContentFrame, row=1)

        dataContainerFrame = ctk.CTkFrame(
            containerContentFrame,
            corner_radius=0,
            fg_color="transparent",
        )
        dataContainerFrame.columnconfigure([0, 1], weight=1)
        dataContainerFrame.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="nsew")

        nameDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="Name",
            placeholder="name",
            value=self.userObject["name"],
            state=True,
            row=0,
            column=0,
        )
        usernameDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="Username",
            placeholder="username",
            value=self.userObject["username"],
            state=True,
            row=0,
            column=1,
        )

        emailDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="Email",
            placeholder="email",
            value=self.userObject["email"],
            state=True,
            row=1,
            column=0,
        )

        Component.buttonDataComponent(
            dataContainerFrame,
            text="Change",
            icon="change",
            mainColor=Dependency.colorPalette["warning"],
            hoverColor=Dependency.colorPalette["warning-dark"],
            event=changeButtonEvent,
            row=2,
        )
        Component.buttonDataComponent(
            dataContainerFrame,
            text="Back",
            icon="back",
            mainColor=Dependency.colorPalette["danger"],
            hoverColor=Dependency.colorPalette["danger-dark"],
            event=backButtonEvent,
            row=3,
        )

    # Rifky
    def homeChangePasswordFrame(self) -> None:
        def changePasswordButtonEvent() -> None:
            if Message.confirmationMessage():
                newPassword = newPasswordDataEntry.get()
                confirmPassword = confirmPasswordDataEntry.get()

                if "" not in [newPassword, confirmPassword]:
                    if newPassword == confirmPassword:
                        response = None
                        try:
                            response = requests.put(
                                f"http://localhost:8000/api/user/update-password/{self.userObject['_id']}",
                                json={
                                    "password": newPassword,
                                },
                            ).json()

                        except requests.ConnectionError:
                            Message.errorMessage(
                                "Make Sure You Are Connected To The Internet"
                            )

                        except:
                            Message.errorMessage("Server Error")

                        if response != None:
                            if response["success"] == True:
                                Message.successMessage(response["message"])

                                Call.resetFrameCall()
                                Middleware.refreshSessionDataMiddleware(
                                    self.homeChangePasswordFrame
                                )

                            else:
                                Message.errorMessage(response["message"])

                                if response["status"] == 404:
                                    Call.logoutCall()

                    else:
                        Message.errorMessage(
                            "Confirmation Password Doesn't Match New Password"
                        )

                else:
                    Message.errorMessage("Please Fill Out The Form")

        def backButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.homeFrame)

        self.sidebarId = 1

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=31)

        Component.sidebarComponent()

        contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

        Component.titleContentComponent(contentFrame, title="HOME", row=0)

        containerContentFrame = ctk.CTkFrame(
            contentFrame,
            corner_radius=8,
            fg_color=Dependency.colorPalette["main"],
        )
        containerContentFrame.columnconfigure(0, weight=1)
        containerContentFrame.grid(row=1, column=0, pady=(0, 20), sticky="nsew")

        Component.titleContainerComponent(
            containerContentFrame, title="Change Password Profile", row=0
        )
        Component.lineHorizontalComponent(containerContentFrame, row=1)

        dataContainerFrame = ctk.CTkFrame(
            containerContentFrame,
            corner_radius=0,
            fg_color="transparent",
        )
        dataContainerFrame.columnconfigure([0, 1], weight=1)
        dataContainerFrame.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="nsew")

        newPasswordDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="New Password",
            placeholder="new password",
            value=None,
            show="*",
            state=True,
            row=0,
            column=0,
        )
        confirmPasswordDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="Confirm Password",
            placeholder="confirm password",
            value=None,
            show="*",
            state=True,
            row=0,
            column=1,
        )

        Component.buttonDataComponent(
            dataContainerFrame,
            text="Change Password",
            icon="password",
            mainColor=Dependency.colorPalette["danger"],
            hoverColor=Dependency.colorPalette["danger-dark"],
            event=changePasswordButtonEvent,
            row=1,
        )
        Component.buttonDataComponent(
            dataContainerFrame,
            text="Back",
            icon="back",
            mainColor=Dependency.colorPalette["danger"],
            hoverColor=Dependency.colorPalette["danger-dark"],
            event=backButtonEvent,
            row=2,
        )

    def userFrame(self, page: int = 1) -> None:
        def AddButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.userAddFrame)

        def changeButtonEvent(id: int) -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.userChangeFrame, id)

        def changePasswordButtonEvent(id: int) -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.userChangePasswordFrame, id)

        def removeButtonEvent(id: int) -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.userRemoveFrame, id)

        self.sidebarId = 2

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=31)

        Component.sidebarComponent()

        contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        contentFrame.rowconfigure(2, weight=1)
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

        Component.titleContentComponent(contentFrame, title="USER", row=0)

        response = None
        try:
            response = requests.get(
                "http://localhost:8000/api/user/count",
            ).json()

        except:
            pass

        responseIsValid = response != None and response["success"]
        Component.boxContentComponent(
            contentFrame,
            boxArray=[
                {
                    "id": 1,
                    "display": "Total",
                    "icon": "user-total",
                    "value": response["data"]["total"] if responseIsValid else "?",
                },
                {
                    "id": 2,
                    "display": "User",
                    "icon": "user",
                    "value": response["data"]["user"] if responseIsValid else "?",
                },
                {
                    "id": 3,
                    "display": "Admin",
                    "icon": "admin",
                    "value": response["data"]["admin"] if responseIsValid else "?",
                },
            ],
            row=1,
        )

        containerContentFrame = ctk.CTkFrame(
            contentFrame,
            corner_radius=8,
            fg_color=Dependency.colorPalette["main"],
        )
        containerContentFrame.columnconfigure(0, weight=1)
        containerContentFrame.grid(row=2, column=0, pady=(0, 20), sticky="nsew")

        Component.titleContainerComponent(
            containerContentFrame, title="User Table", row=0
        )

        Component.lineHorizontalComponent(containerContentFrame, row=1)

        response = None
        try:
            response = requests.get(
                "http://localhost:8000/api/user", json={"count": 10, "page": page}
            ).json()

        except:
            pass

        if (
            response != None
            and response["success"] == True
            and len(response["data"]) > 0
        ):
            countArray = []
            idArray = []
            nameArray = []
            usernameArray = []
            emailArray = []
            roleArray = []
            for userIndex, userObject in enumerate(response["data"]):
                countArray.append(userIndex + 1)
                idArray.append(userObject["_id"])
                nameArray.append(userObject["name"])
                usernameArray.append(userObject["username"])
                emailArray.append(userObject["email"])
                roleArray.append(str(userObject["role"]).capitalize())

            Component.tableDataComponent(
                containerContentFrame,
                idArray=idArray,
                contentArray=[
                    {
                        "id": 1,
                        "header": "No.",
                        "data": countArray,
                        "align": "center",
                    },
                    {
                        "id": 2,
                        "header": "Name",
                        "data": nameArray,
                        "align": "left",
                    },
                    {
                        "id": 3,
                        "header": "Username",
                        "data": usernameArray,
                        "align": "left",
                    },
                    {
                        "id": 4,
                        "header": "Email",
                        "data": emailArray,
                        "align": "left",
                    },
                    {
                        "id": 5,
                        "header": "Role",
                        "data": roleArray,
                        "align": "center",
                    },
                ],
                actionArray=[
                    {
                        "id": 1,
                        "text": "Change",
                        "icon": "change",
                        "mainColor": Dependency.colorPalette["warning"],
                        "hoverColor": Dependency.colorPalette["warning-dark"],
                        "event": changeButtonEvent,
                    },
                    {
                        "id": 2,
                        "text": "Change Password",
                        "icon": "password",
                        "mainColor": Dependency.colorPalette["danger"],
                        "hoverColor": Dependency.colorPalette["danger-dark"],
                        "event": changePasswordButtonEvent,
                    },
                    {
                        "id": 3,
                        "text": "Remove",
                        "icon": "remove",
                        "mainColor": Dependency.colorPalette["danger"],
                        "hoverColor": Dependency.colorPalette["danger-dark"],
                        "event": removeButtonEvent,
                    },
                ],
                row=2,
            )

        else:
            Component.labelDataComponent(
                containerContentFrame,
                text="No Data Found",
                size=24,
                row=2,
                padx=80,
                pady=80,
            )

        dataContainerFrame = ctk.CTkFrame(
            containerContentFrame,
            corner_radius=0,
            fg_color="transparent",
        )
        dataContainerFrame.columnconfigure([0, 1], weight=1)
        dataContainerFrame.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="nsew")

        Component.buttonDataComponent(
            dataContainerFrame,
            text="Add",
            icon="add",
            mainColor=Dependency.colorPalette["success"],
            hoverColor=Dependency.colorPalette["success-dark"],
            event=AddButtonEvent,
            row=0,
        )

    # Rafly
    def userAddFrame(self) -> None:
        def addButtonEvent() -> None:
            if Message.confirmationMessage():
                name = nameDataEntry.get()
                username = usernameDataEntry.get()
                email = emailDataEntry.get()
                newPassword = newPasswordDataEntry.get()
                confirmPassword = confirmPasswordDataEntry.get()

                if "" not in [name, username, email, newPassword, confirmPassword]:
                    if newPassword == confirmPassword:
                        response = None
                        try:
                            response = requests.post(
                                f"http://localhost:8000/api/user/create",
                                json={
                                    "name": name,
                                    "username": username,
                                    "email": email,
                                    "password": newPassword,
                                    "role": "user",
                                    "isActive": True,
                                },
                            ).json()

                        except requests.ConnectionError:
                            Message.errorMessage(
                                "Make Sure You Are Connected To The Internet"
                            )

                        except:
                            Message.errorMessage("Server Error")

                        if response != None:
                            if response["success"] == True:
                                Message.successMessage(response["message"])

                                Call.resetFrameCall()
                                Middleware.refreshSessionDataMiddleware(
                                    self.userAddFrame
                                )

                            else:
                                Message.errorMessage(response["message"])

                    else:
                        Message.errorMessage(
                            "Confirmation Password Doesn't Match New Password"
                        )

                else:
                    Message.errorMessage("Please Fill Out The Form")

        def backButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.userFrame)

        self.sidebarId = 2

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=31)

        Component.sidebarComponent()

        contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

        Component.titleContentComponent(contentFrame, title="USER", row=0)

        containerContentFrame = ctk.CTkFrame(
            contentFrame,
            corner_radius=8,
            fg_color=Dependency.colorPalette["main"],
        )
        containerContentFrame.columnconfigure(0, weight=1)
        containerContentFrame.grid(row=1, column=0, pady=(0, 20), sticky="nsew")

        Component.titleContainerComponent(
            containerContentFrame, title="Add User", row=0
        )
        Component.lineHorizontalComponent(containerContentFrame, row=1)

        dataContainerFrame = ctk.CTkFrame(
            containerContentFrame,
            corner_radius=0,
            fg_color="transparent",
        )
        dataContainerFrame.columnconfigure([0, 1], weight=1)
        dataContainerFrame.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="nsew")

        nameDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="Name",
            placeholder="name",
            value=None,
            state=True,
            row=0,
            column=0,
        )
        usernameDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="Username",
            placeholder="username",
            value=None,
            state=True,
            row=0,
            column=1,
        )

        emailDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="Email",
            placeholder="email",
            value=None,
            state=True,
            row=1,
            column=0,
        )
        newPasswordDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="New Password",
            placeholder="new password",
            value=None,
            state=True,
            row=1,
            column=1,
            show="*",
        )

        confirmPasswordDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="Confirm Password",
            placeholder="confirm password",
            value=None,
            state=True,
            row=2,
            column=0,
            show="*",
        )

        Component.buttonDataComponent(
            dataContainerFrame,
            text="Add",
            icon="add",
            mainColor=Dependency.colorPalette["success"],
            hoverColor=Dependency.colorPalette["success-dark"],
            event=addButtonEvent,
            row=3,
        )
        Component.buttonDataComponent(
            dataContainerFrame,
            text="Back",
            icon="back",
            mainColor=Dependency.colorPalette["danger"],
            hoverColor=Dependency.colorPalette["danger-dark"],
            event=backButtonEvent,
            row=4,
        )

    # Kanaya
    def userChangeFrame(self, id: int) -> None:
        def changeButtonEvent() -> None:
            if Message.confirmationMessage():
                name = nameDataEntry.get()
                username = usernameDataEntry.get()
                email = emailDataEntry.get()

                if "" not in [name, username, email]:
                    response = None
                    try:
                        response = requests.put(
                            f"http://localhost:8000/api/user/update/{id}",
                            json={
                                "name": name,
                                "username": username,
                                "email": email,
                                "role": "user",
                            },
                        ).json()

                    except requests.ConnectionError:
                        Message.errorMessage(
                            "Make Sure You Are Connected To The Internet"
                        )

                    except:
                        Message.errorMessage("Server Error")

                    if response != None:
                        if response["success"] == True:
                            Message.successMessage(response["message"])

                            Call.resetFrameCall()
                            Middleware.refreshSessionDataMiddleware(
                                self.userChangeFrame, id
                            )

                        else:
                            Message.errorMessage(response["message"])

                            if response["status"] == 404:
                                backButtonEvent()

                else:
                    Message.errorMessage("Please Fill Out The Form")

        def backButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.userFrame)

        response = None
        try:
            response = requests.get(f"http://localhost:8000/api/user/{id}").json()

        except:
            Message.errorMessage("Server Error")

            backButtonEvent()

        if response != None and response["success"] == False:
            Message.errorMessage(response["message"])

            backButtonEvent()

        else:
            self.sidebarId = 2

            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=31)

            Component.sidebarComponent()

            contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
            contentFrame.columnconfigure(0, weight=1)
            contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

            Component.titleContentComponent(contentFrame, title="USER", row=0)

            containerContentFrame = ctk.CTkFrame(
                contentFrame,
                corner_radius=8,
                fg_color=Dependency.colorPalette["main"],
            )
            containerContentFrame.columnconfigure(0, weight=1)
            containerContentFrame.grid(row=1, column=0, pady=(0, 20), sticky="nsew")

            Component.titleContainerComponent(
                containerContentFrame, title="Change User", row=0
            )
            Component.lineHorizontalComponent(containerContentFrame, row=1)

            dataContainerFrame = ctk.CTkFrame(
                containerContentFrame,
                corner_radius=0,
                fg_color="transparent",
            )
            dataContainerFrame.columnconfigure([0, 1], weight=1)
            dataContainerFrame.grid(
                row=2, column=0, padx=10, pady=(5, 0), sticky="nsew"
            )

            nameDataEntry = Component.entryDataComponent(
                dataContainerFrame,
                title="Name",
                placeholder="name",
                value=response["data"]["name"],
                state=True,
                row=0,
                column=0,
            )
            usernameDataEntry = Component.entryDataComponent(
                dataContainerFrame,
                title="Username",
                placeholder="username",
                value=response["data"]["username"],
                state=True,
                row=0,
                column=1,
            )

            emailDataEntry = Component.entryDataComponent(
                dataContainerFrame,
                title="Email",
                placeholder="email",
                value=response["data"]["email"],
                state=True,
                row=1,
                column=0,
            )

            Component.buttonDataComponent(
                dataContainerFrame,
                text="Change",
                icon="change",
                mainColor=Dependency.colorPalette["warning"],
                hoverColor=Dependency.colorPalette["warning-dark"],
                event=changeButtonEvent,
                row=2,
            )
            Component.buttonDataComponent(
                dataContainerFrame,
                text="Back",
                icon="back",
                mainColor=Dependency.colorPalette["danger"],
                hoverColor=Dependency.colorPalette["danger-dark"],
                event=backButtonEvent,
                row=3,
            )

    # Salma
    def userChangePasswordFrame(self, id: int) -> None:
        def changePasswordButtonEvent() -> None:
            if Message.confirmationMessage():
                newPassword = newPasswordDataEntry.get()
                confirmPassword = confirmPasswordDataEntry.get()

                if "" not in [newPassword, confirmPassword]:
                    if newPassword == confirmPassword:
                        response = None
                        try:
                            response = requests.put(
                                f"http://localhost:8000/api/user/update-password/{id}",
                                json={
                                    "password": newPassword,
                                },
                            ).json()

                        except requests.ConnectionError:
                            Message.errorMessage(
                                "Make Sure You Are Connected To The Internet"
                            )

                        except:
                            Message.errorMessage("Server Error")

                        if response != None:
                            if response["success"] == True:
                                Message.successMessage(response["message"])

                                Call.resetFrameCall()
                                Middleware.refreshSessionDataMiddleware(
                                    self.userChangePasswordFrame, id
                                )

                            else:
                                Message.errorMessage(response["message"])

                                if response["status"] == 404:
                                    Call.logoutCall()

                    else:
                        Message.errorMessage(
                            "Confirmation Password Doesn't Match New Password"
                        )

                else:
                    Message.errorMessage("Please Fill Out The Form")

        def backButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.userFrame)

        response = None
        try:
            response = requests.get(f"http://localhost:8000/api/user/{id}").json()

        except:
            Message.errorMessage("Server Error")

            backButtonEvent()

        if response != None and response["success"] == False:
            Message.errorMessage(response["message"])

            backButtonEvent()

        else:
            self.sidebarId = 2

            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=31)

            Component.sidebarComponent()

            contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
            contentFrame.columnconfigure(0, weight=1)
            contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

            Component.titleContentComponent(contentFrame, title="USER", row=0)

            containerContentFrame = ctk.CTkFrame(
                contentFrame,
                corner_radius=8,
                fg_color=Dependency.colorPalette["main"],
            )
            containerContentFrame.columnconfigure(0, weight=1)
            containerContentFrame.grid(row=1, column=0, pady=(0, 20), sticky="nsew")

            Component.titleContainerComponent(
                containerContentFrame, title="Change Password User", row=0
            )
            Component.lineHorizontalComponent(containerContentFrame, row=1)

            dataContainerFrame = ctk.CTkFrame(
                containerContentFrame,
                corner_radius=0,
                fg_color="transparent",
            )
            dataContainerFrame.columnconfigure([0, 1], weight=1)
            dataContainerFrame.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="nsew")

            newPasswordDataEntry = Component.entryDataComponent(
                dataContainerFrame,
                title="New Password",
                placeholder="new password",
                value=None,
                show="*",
                state=True,
                row=0,
                column=0,
            )
            confirmPasswordDataEntry = Component.entryDataComponent(
                dataContainerFrame,
                title="Confirm Password",
                placeholder="confirm password",
                value=None,
                show="*",
                state=True,
                row=0,
                column=1,
            )

            Component.buttonDataComponent(
                dataContainerFrame,
                text="Change Password",
                icon="password",
                mainColor=Dependency.colorPalette["danger"],
                hoverColor=Dependency.colorPalette["danger-dark"],
                event=changePasswordButtonEvent,
                row=1,
            )
            Component.buttonDataComponent(
                dataContainerFrame,
                text="Back",
                icon="back",
                mainColor=Dependency.colorPalette["danger"],
                hoverColor=Dependency.colorPalette["danger-dark"],
                event=backButtonEvent,
                row=2,
            )

    # Chelsy
    def userRemoveFrame(self, id: int) -> None:
        def removeButtonEvent() -> None:
            if Message.confirmationMessage():
                response = None

                try:
                    response = requests.delete(
                        f"http://localhost:8000/api/user/delete/{id}",
                    ).json()

                except requests.ConnectionError:
                    Message.errorMessage("Make Sure You Are Connected To The Internet")

                except:
                    Message.errorMessage("Server Error")

                if response != None:
                    if response["success"] == True:
                        Message.successMessage(response["message"])

                        Call.resetFrameCall()
                        Middleware.refreshSessionDataMiddleware(self.userFrame)

                    else:
                        Message.errorMessage(response["message"])

        def backButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.userFrame)

        self.sidebarId = 2

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=31)

        Component.sidebarComponent()

        contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        contentFrame.rowconfigure(1, weight=1)
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

        Component.titleContentComponent(contentFrame, title="USER", row=0)

        containerContentFrame = ctk.CTkFrame(
            contentFrame,
            corner_radius=8,
            fg_color=Dependency.colorPalette["main"],
        )
        containerContentFrame.columnconfigure(0, weight=1)
        containerContentFrame.grid(row=1, column=0, pady=(0, 20), sticky="nsew")

        Component.titleContainerComponent(
            containerContentFrame, title="Remove User", row=0
        )
        Component.lineHorizontalComponent(containerContentFrame, row=1)

        dataContainerFrame = ctk.CTkFrame(
            containerContentFrame,
            corner_radius=0,
            fg_color="transparent",
        )
        dataContainerFrame.columnconfigure([0, 1], weight=1)
        dataContainerFrame.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="nsew")

        try:
            response = requests.get(f"http://localhost:8000/api/user/{id}").json()

        except:
            pass

        Component.entryDataComponent(
            dataContainerFrame,
            title="Name",
            placeholder="name",
            value=response["data"]["name"],
            state=False,
            row=0,
            column=0,
        )
        Component.entryDataComponent(
            dataContainerFrame,
            title="Username",
            placeholder="username",
            value=response["data"]["username"],
            state=False,
            row=0,
            column=1,
        )

        Component.entryDataComponent(
            dataContainerFrame,
            title="Email",
            placeholder="email",
            value=response["data"]["email"],
            state=False,
            row=1,
            column=0,
        )
        Component.entryDataComponent(
            dataContainerFrame,
            title="Role",
            placeholder="role",
            value=response["data"]["role"].capitalize(),
            state=False,
            row=1,
            column=1,
        )

        Component.buttonDataComponent(
            dataContainerFrame,
            text="Remove",
            icon="remove",
            mainColor=Dependency.colorPalette["danger"],
            hoverColor=Dependency.colorPalette["danger-dark"],
            event=removeButtonEvent,
            row=2,
        )
        Component.buttonDataComponent(
            dataContainerFrame,
            text="Back",
            icon="back",
            mainColor=Dependency.colorPalette["danger"],
            hoverColor=Dependency.colorPalette["danger-dark"],
            event=backButtonEvent,
            row=3,
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()

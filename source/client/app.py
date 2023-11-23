import os
import random
import time
import tkinter as tk
from io import BytesIO
from typing import Callable
from urllib.parse import unquote

import customtkinter as ctk
import requests
from CTkMessagebox import CTkMessagebox
from dotenv import load_dotenv
from PIL import Image, ImageTk

load_dotenv()

ctk.set_appearance_mode("Dark")


class Utility:
    def combinePath(base: str, path: str) -> str:
        return os.path.join(base, path)

    def getAsset(file: str) -> str:
        return Utility.combinePath(Dependency.assetPath, file)

    def getIcon(file: str) -> str:
        return Utility.combinePath(Dependency.iconPath, file)


class Dependency:
    host = f"http://{os.getenv("HOST")}:{os.getenv("PORT")}" if os.getenv("ENVIRONMENT") == "development" else "https://signature.irswanda.com"

    title = "Signature"
    subtitle = "Online Document Application"

    resolution = {"width": 1200, "height": 700}
    logoResolution = {"width": 639, "height": 799}

    assetPath = Utility.combinePath(os.path.dirname(os.path.realpath(__file__)), "asset")
    iconPath = Utility.combinePath(assetPath, "icon")
    appIconPath = "./source/client/asset/icon.ico"

    fontFamily = {"main": "Montserrat"}
    colorPalette = {
        "main": "#54A4F5",
        "main-dark": "#3498DB",
        "background-light": "#99A3A4",
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
            "is_active": None,
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

            def documentButtonEvent() -> None:
                Call.resetFrameCall()
                Middleware.refreshSessionDataMiddleware(app.documentFrame)

            sidebarButtonComponent(
                contentSidebarFrame,
                title="Document",
                icon="document",
                event=documentButtonEvent,
                row=5,
                highlight=True if app.sidebarId == 2 else False,
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
        span: int = 1,
    ) -> ctk.CTkEntry:
        # def focusIn(event):
        #     if entryObject.get() == placeholder:
        #         entryObject.delete(0, ctk.END)
        #         entryObject.configure(
        #             show=show, text_color=Dependency.colorPalette["text"]
        #         )

        # def focusOut(event):
        #     if entryObject.get() == "":
        #         entryObject.insert(0, placeholder)
        #         entryObject.configure(
        #             show="", text_color=Dependency.colorPalette["text-dark"]
        #         )

        entryFrame = ctk.CTkFrame(master, corner_radius=0, fg_color="transparent")
        entryFrame.rowconfigure([0, 1], weight=1)
        entryFrame.columnconfigure(0, weight=1)
        entryFrame.grid(row=row, column=column, columnspan=span, sticky="nsew")

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
        # entryValue.set(value if value != None else placeholder)
        entryValue.set(value if value != None else "")

        entryObject = ctk.CTkEntry(
            entryFrame,
            height=36,
            textvariable=entryValue,
            # show=show if value != None else "",
            show=show,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=18,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"],
            # if value != None
            # else Dependency.colorPalette["text-dark"],
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

        # entryObject.bind("<FocusIn>", focusIn)
        # entryObject.bind("<FocusOut>", focusOut)

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
        currentPage: int,
        totalPage: int,
        framePage: Callable[[], None],
        row: int,
        contentArray: list[dict[str, any]],
        idArray: list[int] = None,
        actionArray: list[dict[str, any]] = None,
        disabledIdArray: list[int] = None,
        numbering: bool = True,
        tag: int = None,
    ) -> None:
        def changePageEvent(page):
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(
                framePage, firstTag=page, secondTag=tag
            )

        tableFrame = ctk.CTkFrame(
            master, height=0, corner_radius=0, fg_color="transparent"
        )
        tableFrame.columnconfigure(0, weight=1)
        tableFrame.grid(row=row, column=0, padx=20, pady=(20, 10), sticky="nsew")

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
        headerTableFrame.grid(row=1, column=0, pady=(0, 10), sticky="nsew")

        Component.lineVerticalComponent(headerTableFrame, column=0)

        for contentIndex, contentObject in enumerate(contentArray):
            dataHeaderFrame = ctk.CTkFrame(
                headerTableFrame,
                width=0,
                height=28,
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
                height=28,
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
                    actionHeaderFrame,
                    width=0,
                    height=28,
                    corner_radius=0,
                    fg_color="transparent",
                )
                buttonActionFrame.grid(row=(idIndex * 2) + 2, column=0, sticky="nsew")

                for actionIndex, actionObject in enumerate(actionArray):
                    if actionObject["optional"]:
                        buttonActive = idObject not in disabledIdArray
                    else:
                        buttonActive = True

                    ctk.CTkButton(
                        buttonActionFrame,
                        width=0,
                        height=28,
                        image=ctk.CTkImage(
                            Image.open(Utility.getIcon(f"{actionObject['icon']}.png")),
                            size=(12, 12),
                        ),
                        text=f'{actionObject["text"]}',
                        font=ctk.CTkFont(
                            family=Dependency.fontFamily["main"],
                            size=12,
                            weight="bold",
                        ),
                        cursor="hand2",
                        corner_radius=0,
                        text_color=Dependency.colorPalette["text"],
                        fg_color=actionObject["mainColor"]
                        if buttonActive
                        else Dependency.colorPalette["background-light"],
                        hover_color=actionObject["hoverColor"]
                        if buttonActive
                        else Dependency.colorPalette["background-light"],
                        command=(
                            lambda event=actionObject["event"], id=idObject: event(id)
                        )
                        if buttonActive
                        else lambda: None,
                    ).grid(
                        row=0,
                        column=actionIndex,
                        ipadx=2,
                        sticky="nsew",
                    )

                Component.lineHorizontalComponent(
                    actionHeaderFrame, row=(idIndex * 2) + 3
                )

            Component.lineVerticalComponent(
                headerTableFrame, column=(len(contentArray) * 2) + 2
            )

        paginationFrame = ctk.CTkFrame(
            tableFrame, height=0, corner_radius=0, fg_color="transparent"
        )
        paginationFrame.columnconfigure([0, 1], weight=1)
        paginationFrame.grid(row=2, column=0, sticky="nsew")

        ctk.CTkLabel(
            paginationFrame,
            text=f"Page {currentPage} of {totalPage}",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=16,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"],
        ).grid(row=0, column=0, sticky="nsw")

        buttonPaginationFrame = ctk.CTkFrame(
            paginationFrame, height=0, corner_radius=0, fg_color="transparent"
        )
        buttonPaginationFrame.grid(row=0, column=1, sticky="nse")

        if currentPage > 1:
            ctk.CTkButton(
                buttonPaginationFrame,
                width=0,
                image=ctk.CTkImage(
                    Image.open(Utility.getIcon("previous.png")),
                    size=(16, 16),
                ),
                text="",
                cursor="hand2",
                corner_radius=8,
                text_color=Dependency.colorPalette["text"],
                fg_color=Dependency.colorPalette["main"],
                hover_color=Dependency.colorPalette["main-dark"],
                command=lambda: changePageEvent(currentPage - 1),
            ).grid(
                row=0,
                column=0,
                sticky="nsew",
            )

        if currentPage < totalPage:
            ctk.CTkButton(
                buttonPaginationFrame,
                width=0,
                image=ctk.CTkImage(
                    Image.open(Utility.getIcon("next.png")),
                    size=(16, 16),
                ),
                text="",
                cursor="hand2",
                corner_radius=16,
                text_color=Dependency.colorPalette["text"],
                fg_color=Dependency.colorPalette["main"],
                hover_color=Dependency.colorPalette["main-dark"],
                command=lambda: changePageEvent(currentPage + 1),
            ).grid(
                row=0,
                column=1,
                sticky="nsew",
            )

    def labelDataComponent(
        master: ctk.CTk | ctk.CTkFrame,
        text: str,
        size: int = 16,
        row: int = 0,
        padx: int = 10,
        pady: int = 10,
        columnspan: int = 1
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
        ).grid(row=row, column=0, columnspan=columnspan, padx=padx, pady=pady, sticky="nsew")

    def comboBoxDataComponent(
        master: ctk.CTk | ctk.CTkFrame,
        title: str,
        placeholder: str,
        value: str,
        option: list[str],
        state: bool,
        row: int,
        column: int,
        span: int = 1,
    ) -> ctk.CTkComboBox:
        def search(event):
            searchValue = event.widget.get()

            if searchValue == "":
                comboBoxObject.configure(values=option)

            else:
                searchedOption = []
                for optionObject in option:
                    if searchValue in optionObject:

                        searchedOption.append(optionObject)
                        
                        
                if len(searchedOption) == 0:
                    searchedOption.append("search not found")

                try:
                    comboBoxObject.configure(values=searchedOption)

                except:
                    pass

        comboBoxFrame = ctk.CTkFrame(master, corner_radius=0, fg_color="transparent")
        comboBoxFrame.rowconfigure([0, 1], weight=1)
        comboBoxFrame.columnconfigure(0, weight=1)
        comboBoxFrame.grid(row=row, column=column, columnspan=span, sticky="nsew")

        ctk.CTkLabel(
            comboBoxFrame,
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

        comboBoxValue = ctk.StringVar()
        comboBoxValue.set(value if value != None else "")

        comboBoxObject = ctk.CTkComboBox(
            comboBoxFrame,
            height=36,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=18,
                weight="bold",
            ),
            dropdown_font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=18,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"],
            fg_color=Dependency.colorPalette["main"],
            border_color=Dependency.colorPalette["text"],
            button_color=Dependency.colorPalette["main"],
            border_button_color=Dependency.colorPalette["text"],
            button_hover_color=Dependency.colorPalette["main-dark"],
            border_button_hover_color=Dependency.colorPalette["text"],
            dropdown_fg_color=Dependency.colorPalette["main"],
            dropdown_hover_color=Dependency.colorPalette["main-dark"],
            dropdown_text_color=Dependency.colorPalette["text"],
            state="normal" if state else "disabled",
            values=option,
            variable=comboBoxValue
        )
        comboBoxObject.grid(
            row=1,
            column=0,
            padx=(0, 5) if column == 0 else (5, 0),
            pady=(0, 10),
            sticky="nsew",
        )

        comboBoxObject.bind('<KeyRelease>', search)

        return comboBoxObject


class Middleware:
    def refreshSessionDataMiddleware(
        frameFunction: Callable[[], None], firstTag=None, secondTag=None
    ) -> None:
        def fetchSessionData() -> None:
            response = None
            try:
                response = requests.get(
                    f"{Dependency.host}/api/user/{app.userObject['_id']}"
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
                    app.userObject["is_active"] = response["data"]["is_active"]

                    Call.resetFrameCall()

                    if firstTag == None:
                        frameFunction()

                    elif firstTag != None:
                        if secondTag == None:
                            frameFunction(firstTag)

                        else:
                            frameFunction(firstTag, secondTag)

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

        app.after(100, fetchSessionData)


class App(ctk.CTk):
    userObject = {
        "_id": 0,
        "name": None,
        "username": None,
        "email": None,
        "role": None,
        "is_active": None,
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
            if not skipObject["status"]:
                loadingValue = 0
                while loadingValue < 1:
                    loadingValue += random.uniform(0.005, 0.01)
                    progressTextProgressBar.set(loadingValue)

                    self.update()
                    time.sleep(0.00001)

            Call.resetFrameCall()

            if skipObject["status"]:
                self.userObject["_id"] = skipObject["id"]

                Call.resetFrameCall()

                if skipObject["tag"] == None:
                    Middleware.refreshSessionDataMiddleware(skipObject["frame"])

                else:
                    Middleware.refreshSessionDataMiddleware(
                        skipObject["frame"], skipObject["tag"]
                    )

            else:
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
        def loginButtonEvent() -> None:
            username = usernameLoginEntry.get()
            password = passwordLoginEntry.get()

            if "" not in [username, password]:
                response = None
                try:
                    response = requests.post(
                        f"{Dependency.host}/api/auth/login",
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

        def registerButtonEvent() -> None:
            Call.resetFrameCall()
            self.registerFrame()

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
        loginFrame.rowconfigure(6, weight=1)
        loginFrame.columnconfigure(0, weight=1)
        loginFrame.grid(row=0, column=1, padx=120, pady=(80, 20), sticky="nsew")

        titleLoginLabel = ctk.CTkLabel(
            loginFrame,
            text="Login Details",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=36, weight="bold"
            ),
        )
        titleLoginLabel.grid(row=0, column=0, pady=(0, 20), sticky="nsw")

        usernameLoginEntry = ctk.CTkEntry(
            loginFrame,
            height=48,
            placeholder_text="username",
            justify="left",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
        )
        usernameLoginEntry.grid(row=1, column=0, pady=(0, 10), sticky="nsew")

        passwordLoginEntry = ctk.CTkEntry(
            loginFrame,
            height=48,
            show="*",
            placeholder_text="password",
            justify="left",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
        )
        passwordLoginEntry.grid(row=2, column=0, pady=(0, 20), sticky="nsew")

        submitLoginButton = ctk.CTkButton(
            loginFrame,
            text="Login",
            height=48,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
            fg_color=Dependency.colorPalette["main"],
            hover_color=Dependency.colorPalette["main-dark"],
            command=loginButtonEvent,
        )
        submitLoginButton.grid(row=3, column=0, pady=(0, 10), sticky="nsew")

        orLoginLabel = ctk.CTkLabel(
            loginFrame,
            text="or",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
        )
        orLoginLabel.grid(row=4, column=0, pady=(0, 10), sticky="nsew")

        registerLoginButton = ctk.CTkButton(
            loginFrame,
            text="Register",
            height=48,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
            fg_color=Dependency.colorPalette["main"],
            hover_color=Dependency.colorPalette["main-dark"],
            command=registerButtonEvent,
        )
        registerLoginButton.grid(row=5, column=0, sticky="nsew")

        exitLoginButton = ctk.CTkButton(
            loginFrame,
            text="Exit",
            height=40,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
            fg_color=Dependency.colorPalette["danger"],
            hover_color=Dependency.colorPalette["danger-dark"],
            command=exitButtonEvent,
        )
        exitLoginButton.grid(row=6, column=0, sticky="se")

    def registerFrame(self) -> None:
        def registerButtonEvent() -> None:
            name = nameRegisterEntry.get()
            username = usernameRegisterEntry.get()
            email = emailRegisterEntry.get()
            password = passwordRegisterEntry.get()
            confirmationPassword = confirmationPasswordRegisterEntry.get()

            if Message.confirmationMessage():
                if "" not in [name, username, email, password, confirmationPassword]:
                    if password == confirmationPassword:
                        response = None
                        try:
                            response = requests.post(
                                f"{Dependency.host}/api/auth/register",
                                json={"name": name, "username": username, "email": email, "password": password},
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
                        Message.errorMessage(
                            "Confirmation Password Doesn't Match Password"
                        )

                else:
                    Message.errorMessage("Please Fill Out The Form")

        def loginButtonEvent() -> None:
            Call.resetFrameCall()
            self.loginFrame()

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

        registerFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        registerFrame.rowconfigure(9, weight=1)
        registerFrame.columnconfigure(0, weight=1)
        registerFrame.grid(row=0, column=1, padx=120, pady=(80, 20), sticky="nsew")

        titleRegisterLabel = ctk.CTkLabel(
            registerFrame,
            text="Register Details",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=36, weight="bold"
            ),
        )
        titleRegisterLabel.grid(row=0, column=0, pady=(0, 20), sticky="nsw")

        nameRegisterEntry = ctk.CTkEntry(
            registerFrame,
            height=48,
            placeholder_text="name",
            justify="left",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
        )
        nameRegisterEntry.grid(row=1, column=0, pady=(0, 10), sticky="nsew")

        usernameRegisterEntry = ctk.CTkEntry(
            registerFrame,
            height=48,
            placeholder_text="username",
            justify="left",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
        )
        usernameRegisterEntry.grid(row=2, column=0, pady=(0, 10), sticky="nsew")

        emailRegisterEntry = ctk.CTkEntry(
            registerFrame,
            height=48,
            placeholder_text="email",
            justify="left",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
        )
        emailRegisterEntry.grid(row=3, column=0, pady=(0, 10), sticky="nsew")     
        
        passwordRegisterEntry = ctk.CTkEntry(
            registerFrame,
            height=48,
            show="*",
            placeholder_text="password",
            justify="left",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
        )
        passwordRegisterEntry.grid(row=4, column=0, pady=(0, 10), sticky="nsew")

        confirmationPasswordRegisterEntry = ctk.CTkEntry(
            registerFrame,
            height=48,
            show="*",
            placeholder_text="confirmation password",
            justify="left",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
        )
        confirmationPasswordRegisterEntry.grid(row=5, column=0, pady=(0, 20), sticky="nsew")

        submitRegisterButton = ctk.CTkButton(
            registerFrame,
            text="Register",
            height=48,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
            fg_color=Dependency.colorPalette["main"],
            hover_color=Dependency.colorPalette["main-dark"],
            command=registerButtonEvent,
        )
        submitRegisterButton.grid(row=6, column=0, pady=(0, 10), sticky="nsew")

        orRegisterLabel = ctk.CTkLabel(
            registerFrame,
            text="or",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
        )
        orRegisterLabel.grid(row=7, column=0, pady=(0, 10), sticky="nsew")

        loginRegisterButton = ctk.CTkButton(
            registerFrame,
            text="Login",
            height=48,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
            fg_color=Dependency.colorPalette["main"],
            hover_color=Dependency.colorPalette["main-dark"],
            command=loginButtonEvent,
        )
        loginRegisterButton.grid(row=8, column=0, sticky="nsew")

        exitRegisterButton = ctk.CTkButton(
            registerFrame,
            text="Exit",
            height=40,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"], size=20, weight="bold"
            ),
            fg_color=Dependency.colorPalette["danger"],
            hover_color=Dependency.colorPalette["danger-dark"],
            command=exitButtonEvent,
        )
        exitRegisterButton.grid(row=9, column=0, sticky="se")

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
            text=f"Welcome To Signature {self.userObject['username']}!",
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
                            f"{Dependency.host}/api/user/change/{self.userObject['_id']}",
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
        contentFrame.rowconfigure(1, weight=1)
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
            span=2,
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

    def homeChangePasswordFrame(self) -> None:  # Rifky
        def changePasswordButtonEvent() -> None:
            if Message.confirmationMessage():
                newPassword = newPasswordDataEntry.get()
                confirmPassword = confirmPasswordDataEntry.get()

                if "" not in [newPassword, confirmPassword]:
                    if newPassword == confirmPassword:
                        response = None
                        try:
                            response = requests.put(
                                f"{Dependency.host}/api/user/change-password/{self.userObject['_id']}",
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
        contentFrame.rowconfigure(1, weight=1)
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
                f"{Dependency.host}/api/user/count",
            ).json()

        except:
            pass

        responseIsValid = response != None and response["success"]
        userTotal = response["data"]["total"]
        Component.boxContentComponent(
            contentFrame,
            boxArray=[
                {
                    "id": 1,
                    "display": "Total",
                    "icon": "user-total",
                    "value": userTotal if responseIsValid else "?",
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
                f"{Dependency.host}/api/user", json={"count": 10, "page": page}
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
            disabledIdArray = []
            for userIndex, userObject in enumerate(response["data"]):
                countArray.append((10 * (page - 1)) + userIndex + 1)
                idArray.append(userObject["_id"])
                nameArray.append(userObject["name"])
                usernameArray.append(userObject["username"])
                emailArray.append(userObject["email"])
                roleArray.append(str(userObject["role"]).capitalize())

                if userObject["role"] == "admin":
                    disabledIdArray.append(userObject["_id"])

            Component.tableDataComponent(
                containerContentFrame,
                currentPage=page,
                totalPage=((userTotal - 1) // 10) + 1,
                framePage=app.userFrame,
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
                        "optional": True,
                    },
                    {
                        "id": 2,
                        "text": "Change Password",
                        "icon": "password",
                        "mainColor": Dependency.colorPalette["danger"],
                        "hoverColor": Dependency.colorPalette["danger-dark"],
                        "event": changePasswordButtonEvent,
                        "optional": True,
                    },
                    {
                        "id": 3,
                        "text": "Remove",
                        "icon": "remove",
                        "mainColor": Dependency.colorPalette["danger"],
                        "hoverColor": Dependency.colorPalette["danger-dark"],
                        "event": removeButtonEvent,
                        "optional": True,
                    },
                ],
                disabledIdArray=disabledIdArray,
                row=2,
            )

        else:
            Component.labelDataComponent(
                containerContentFrame,
                text="Data Not Found",
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

    def userAddFrame(self) -> None:  # Rafly
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
                                f"{Dependency.host}/api/user/add",
                                json={
                                    "name": name,
                                    "username": username,
                                    "email": email,
                                    "password": newPassword,
                                    "role": "user",
                                    "is_active": True,
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
            span=2,
        )

        newPasswordDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="New Password",
            placeholder="new password",
            value=None,
            state=True,
            row=2,
            column=0,
            show="*",
        )
        confirmPasswordDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="Confirm Password",
            placeholder="confirm password",
            value=None,
            state=True,
            row=2,
            column=1,
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

    def userChangeFrame(self, id: int) -> None:  # Kanaya
        def changeButtonEvent() -> None:
            if Message.confirmationMessage():
                name = nameDataEntry.get()
                username = usernameDataEntry.get()
                email = emailDataEntry.get()

                if "" not in [name, username, email]:
                    response = None
                    try:
                        response = requests.put(
                            f"{Dependency.host}/api/user/change/{id}",
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
            response = requests.get(f"{Dependency.host}/api/user/{id}").json()

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
                span=2,
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

    def userChangePasswordFrame(self, id: int) -> None:  # Salma
        def changePasswordButtonEvent() -> None:
            if Message.confirmationMessage():
                newPassword = newPasswordDataEntry.get()
                confirmPassword = confirmPasswordDataEntry.get()

                if "" not in [newPassword, confirmPassword]:
                    if newPassword == confirmPassword:
                        response = None
                        try:
                            response = requests.put(
                                f"{Dependency.host}/api/user/change-password/{id}",
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
            response = requests.get(f"{Dependency.host}/api/user/{id}").json()

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
                containerContentFrame, title="Change Password User", row=0
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

    def userRemoveFrame(self, id: int) -> None:  # Chelsy
        def removeButtonEvent() -> None:
            if Message.confirmationMessage():
                response = None

                try:
                    response = requests.delete(
                        f"{Dependency.host}/api/user/remove/{id}",
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

                        if response["status"] == 404:
                            Call.logoutCall()

        def backButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.userFrame)

        response = None
        try:
            response = requests.get(f"{Dependency.host}/api/user/{id}").json()

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
            dataContainerFrame.grid(
                row=2, column=0, padx=10, pady=(5, 0), sticky="nsew"
            )

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

    def documentFrame(self, page: int = 1) -> None:
        def uploadButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.documentUploadFrame)

        def viewButtonEvent(id: int) -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.documentViewFrame, id)

        def downloadButtonEvent(id: int) -> None:
            if Message.confirmationMessage():
                response = None

                try:
                    response = requests.get(
                        f"{Dependency.host}/api/document/download/{id}", stream=True
                    )

                except requests.ConnectionError:
                    Message.errorMessage("Make Sure You Are Connected To The Internet")

                except:
                    Message.errorMessage("Server Error")

                if response != None and response.status_code == 200:
                    contentDisposition = response.headers.get("content-disposition")
                    defaultFileName = (
                        unquote(contentDisposition.split("filename=")[1])
                        if contentDisposition
                        else "Downloaded Document.jpg"
                    )

                    filePath = ctk.filedialog.asksaveasfilename(
                        filetypes=[("Image files", "*.jpg *.jpeg *.png")],
                        initialfile=defaultFileName,
                    )

                    if filePath:
                        with open(filePath, "wb") as file:
                            for chunk in response.iter_content(chunk_size=128):
                                file.write(chunk)

                        Message.successMessage("Document Downloaded")

                    else:
                        Message.errorMessage("Document Failed To Be Downloaded")

                else:
                    Message.errorMessage("Document Failed To Be Downloaded")

        def signButtonEvent(id: int) -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.documentSignFrame, id)

        def accessButtonEvent(id: int) -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.documentAccessFrame, 1, id)

        def removeButtonEvent(id: int) -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.documentRemoveFrame, id)

        self.sidebarId = 2

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=31)

        Component.sidebarComponent()

        contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        contentFrame.rowconfigure(2, weight=1)
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

        Component.titleContentComponent(contentFrame, title="DOCUMENT", row=0)

        response = None
        try:
            response = requests.get(
                f"{Dependency.host}/api/document/access/{self.userObject['_id']}/count",
            ).json()

        except:
            pass

        responseIsValid = response != None and response["success"]
        documentTotal = response["data"]["total"]
        Component.boxContentComponent(
            contentFrame,
            boxArray=[
                {
                    "id": 1,
                    "display": "Total",
                    "icon": "document-total",
                    "value": documentTotal if responseIsValid else "?",
                },
                {
                    "id": 2,
                    "display": "Owned",
                    "icon": "owned",
                    "value": response["data"]["owned"] if responseIsValid else "?",
                },
                {
                    "id": 3,
                    "display": "Shared",
                    "icon": "shared",
                    "value": response["data"]["shared"] if responseIsValid else "?",
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
            containerContentFrame, title="Document Table", row=0
        )

        Component.lineHorizontalComponent(containerContentFrame, row=1)

        response = None
        try:
            response = requests.get(
                f"{Dependency.host}/api/document/access/{self.userObject['_id']}",
                json={"count": 10, "page": page},
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
            authorArray = []
            codeArray = []
            titleArray = []
            categoryArray = []
            descriptionArray = []
            disabledIdArray = []
            for documentIndex, documentObject in enumerate(response["data"]):
                countArray.append((10 * (page - 1)) + documentIndex + 1)
                idArray.append(documentObject["_id"])
                authorArray.append(documentObject["author_extend"]["username"])
                codeArray.append(documentObject["code"])
                titleArray.append(documentObject["title"])
                categoryArray.append(documentObject["category"])
                descriptionArray.append(documentObject["description"])

                if documentObject["id_author"] != self.userObject["_id"]:
                    disabledIdArray.append(documentObject["_id"])

            Component.tableDataComponent(
                containerContentFrame,
                currentPage=page,
                totalPage=((documentTotal - 1) // 10) + 1,
                framePage=app.documentFrame,
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
                        "header": "Author",
                        "data": authorArray,
                        "align": "left",
                    },
                    {
                        "id": 3,
                        "header": "Code",
                        "data": codeArray,
                        "align": "center",
                    },
                    {
                        "id": 4,
                        "header": "Title",
                        "data": titleArray,
                        "align": "left",
                    },
                    {
                        "id": 5,
                        "header": "Category",
                        "data": categoryArray,
                        "align": "center",
                    },
                    {
                        "id": 6,
                        "header": "Description",
                        "data": descriptionArray,
                        "align": "left",
                    },
                ],
                actionArray=[
                    {
                        "id": 1,
                        "text": "View",
                        "icon": "view",
                        "mainColor": Dependency.colorPalette["success"],
                        "hoverColor": Dependency.colorPalette["success-dark"],
                        "event": viewButtonEvent,
                        "optional": False,
                    },
                    {
                        "id": 2,
                        "text": "Download",
                        "icon": "download",
                        "mainColor": Dependency.colorPalette["success"],
                        "hoverColor": Dependency.colorPalette["success-dark"],
                        "event": downloadButtonEvent,
                        "optional": False,
                    },
                    {
                        "id": 3,
                        "text": "Sign",
                        "icon": "sign",
                        "mainColor": Dependency.colorPalette["warning"],
                        "hoverColor": Dependency.colorPalette["warning-dark"],
                        "event": signButtonEvent,
                        "optional": False,
                    },
                    {
                        "id": 4,
                        "text": "Access",
                        "icon": "access",
                        "mainColor": Dependency.colorPalette["warning"],
                        "hoverColor": Dependency.colorPalette["warning-dark"],
                        "event": accessButtonEvent,
                        "optional": True,
                    },
                    {
                        "id": 5,
                        "text": "Remove",
                        "icon": "remove",
                        "mainColor": Dependency.colorPalette["danger"],
                        "hoverColor": Dependency.colorPalette["danger-dark"],
                        "event": removeButtonEvent,
                        "optional": True,
                    },
                ],
                disabledIdArray=disabledIdArray,
                row=2,
            )

        else:
            Component.labelDataComponent(
                containerContentFrame,
                text="Data Not Found",
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
            text="Upload",
            icon="upload",
            mainColor=Dependency.colorPalette["success"],
            hoverColor=Dependency.colorPalette["success-dark"],
            event=uploadButtonEvent,
            row=0,
        )

    def documentUploadFrame(self) -> None:
        def browseButtonEvent() -> None:
            filePath = ctk.filedialog.askopenfilename(
                title="Select a document",
                filetypes=[
                    # ("PDF files", "*.pdf"),
                    # ("Word files", "*.docx"),
                    ("Image files", "*.jpg *.jpeg *.png"),
                ],
            )

            if filePath:
                nameFileValue.set(filePath)

            else:
                nameFileValue.set("choose a document to upload")

        def uploadButtonEvent() -> None:
            if Message.confirmationMessage():
                code = codeDataEntry.get()
                title = titleDataEntry.get()
                category = categoryDataEntry.get()
                description = descriptionDataEntry.get()
                filePath = nameFileValue.get()

                if (
                    "" not in [code, title, category, description]
                    and filePath != "choose a document to upload"
                ):
                    response = None
                    try:
                        response = requests.post(
                            f"{Dependency.host}/api/document/upload",
                            data={
                                "id_author": self.userObject["_id"],
                                "code": code,
                                "title": title,
                                "category": category,
                                "description": description,
                            },
                            files={"file": open(filePath, "rb")},
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
                                self.documentUploadFrame
                            )

                        else:
                            Message.errorMessage(response["message"])

                else:
                    Message.errorMessage("Please Fill Out The Form")

        def backButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.documentFrame)

        self.sidebarId = 2

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=31)

        Component.sidebarComponent()

        contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        contentFrame.rowconfigure(1, weight=1)
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

        Component.titleContentComponent(contentFrame, title="DOCUMENT", row=0)

        containerContentFrame = ctk.CTkFrame(
            contentFrame,
            corner_radius=8,
            fg_color=Dependency.colorPalette["main"],
        )
        containerContentFrame.columnconfigure(0, weight=1)
        containerContentFrame.grid(row=1, column=0, pady=(0, 20), sticky="nsew")

        Component.titleContainerComponent(
            containerContentFrame, title="Upload Document", row=0
        )
        Component.lineHorizontalComponent(containerContentFrame, row=1)

        dataContainerFrame = ctk.CTkFrame(
            containerContentFrame,
            corner_radius=0,
            fg_color="transparent",
        )
        dataContainerFrame.columnconfigure([0, 1], weight=1)
        dataContainerFrame.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="nsew")

        codeDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="Code",
            placeholder="code",
            value=None,
            state=True,
            row=0,
            column=0,
        )
        titleDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="Title",
            placeholder="title",
            value=None,
            state=True,
            row=0,
            column=1,
        )

        categoryDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="Category",
            placeholder="category",
            value=None,
            state=True,
            row=1,
            column=0,
        )
        descriptionDataEntry = Component.entryDataComponent(
            dataContainerFrame,
            title="Description",
            placeholder="description",
            value=None,
            state=True,
            row=1,
            column=1,
        )

        fileDataFrame = ctk.CTkFrame(
            dataContainerFrame,
            corner_radius=0,
            fg_color="transparent",
        )
        fileDataFrame.columnconfigure(0, weight=3)
        fileDataFrame.columnconfigure(1, weight=1)
        fileDataFrame.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky="nsew")

        ctk.CTkLabel(
            fileDataFrame,
            text="Document",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=18,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"],
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 5),
            sticky="nsw",
        )

        nameFileValue = ctk.StringVar()
        nameFileValue.set("choose a document to upload")

        nameFileEntry = ctk.CTkEntry(
            fileDataFrame,
            height=36,
            textvariable=nameFileValue,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=18,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"],
            fg_color="transparent",
            border_color=Dependency.colorPalette["text"],
            state="disabled",
        )
        nameFileEntry.grid(
            row=1,
            column=0,
            padx=(0, 5),
            sticky="nsew",
        )

        ctk.CTkButton(
            fileDataFrame,
            height=36,
            text="Browse",
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=18,
                weight="bold",
            ),
            image=ctk.CTkImage(
                Image.open(Utility.getIcon(f"browse.png")),
                size=(22, 22),
            ),
            cursor="hand2",
            corner_radius=8,
            text_color=Dependency.colorPalette["text"],
            fg_color=Dependency.colorPalette["warning"],
            hover_color=Dependency.colorPalette["warning-dark"],
            command=browseButtonEvent,
        ).grid(
            row=1,
            column=1,
            padx=(5, 0),
            sticky="nsew",
        )

        Component.buttonDataComponent(
            dataContainerFrame,
            text="Upload",
            icon="upload",
            mainColor=Dependency.colorPalette["success"],
            hoverColor=Dependency.colorPalette["success-dark"],
            event=uploadButtonEvent,
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

    def documentViewFrame(self, id: int) -> None:
        def backButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.documentFrame)

        self.sidebarId = 2

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=31)

        Component.sidebarComponent()

        contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        contentFrame.rowconfigure(1, weight=1)
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

        Component.titleContentComponent(contentFrame, title="DOCUMENT", row=0)

        containerContentFrame = ctk.CTkFrame(
            contentFrame,
            corner_radius=8,
            fg_color=Dependency.colorPalette["main"],
        )
        containerContentFrame.rowconfigure(2, weight=1)
        containerContentFrame.columnconfigure(0, weight=1)
        containerContentFrame.grid(row=1, column=0, pady=(0, 20), sticky="nsew")

        Component.titleContainerComponent(
            containerContentFrame, title="View Document", row=0
        )
        Component.lineHorizontalComponent(containerContentFrame, row=1)

        dataContainerFrame = ctk.CTkFrame(
            containerContentFrame,
            corner_radius=0,
            fg_color="transparent",
        )
        dataContainerFrame.rowconfigure(0, weight=1)
        dataContainerFrame.columnconfigure([0, 1], weight=1)
        dataContainerFrame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew")

        response = None
        try:
            response = requests.get(f"{Dependency.host}/api/document/view/{id}")

        except:
            pass

        if response != None and response.status_code == 200:

            def show_full_image(event):
                global imageResize

                if (event.width / event.height) > imageRatio:
                    height = int(event.height)
                    width = int(height * imageRatio)
                else:
                    width = int(event.width)
                    height = int(width / imageRatio)

                imageResize = ImageTk.PhotoImage(image.resize((width, height)))
                imageDataCanvas.create_image(
                    int(event.width / 2),
                    int(event.height / 2),
                    anchor=ctk.CENTER,
                    image=imageResize,
                )

            image = Image.open(BytesIO(response.content))
            imageRatio = image.size[0] / image.size[1]

            imageDataCanvas = tk.Canvas(
                dataContainerFrame, bg=Dependency.colorPalette["main"], bd=2
            )
            imageDataCanvas.grid(
                row=0, column=0, columnspan=2, pady=(0, 10), sticky="nsew"
            )

            imageDataCanvas.bind("<Configure>", show_full_image)

        Component.buttonDataComponent(
            dataContainerFrame,
            text="Back",
            icon="back",
            mainColor=Dependency.colorPalette["danger"],
            hoverColor=Dependency.colorPalette["danger-dark"],
            event=backButtonEvent,
            row=1,
        )

    def documentSignFrame(self, id: int) -> None:
        def backButtonEvent() -> None:
            if Message.confirmationMessage():
                Call.resetFrameCall()
                Middleware.refreshSessionDataMiddleware(self.documentFrame)

        self.sidebarId = 2

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=31)

        Component.sidebarComponent()

        contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        contentFrame.rowconfigure(1, weight=1)
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

        Component.titleContentComponent(contentFrame, title="DOCUMENT", row=0)

        containerContentFrame = ctk.CTkFrame(
            contentFrame,
            corner_radius=8,
            fg_color=Dependency.colorPalette["main"],
        )
        containerContentFrame.rowconfigure(2, weight=1)
        containerContentFrame.columnconfigure(0, weight=1)
        containerContentFrame.grid(row=1, column=0, pady=(0, 20), sticky="nsew")

        Component.titleContainerComponent(
            containerContentFrame, title="Sign Document", row=0
        )
        Component.lineHorizontalComponent(containerContentFrame, row=1)

        dataContainerFrame = ctk.CTkFrame(
            containerContentFrame,
            corner_radius=0,
            fg_color="transparent",
        )
        dataContainerFrame.rowconfigure(0, weight=1)
        dataContainerFrame.columnconfigure([0, 1], weight=1)
        dataContainerFrame.grid(row=2, column=0, padx=10, pady=(10, 0), sticky="nsew")

        response = None
        try:
            response = requests.get(f"{Dependency.host}/api/document/view/{id}")

        except:
            pass

        if response != None and response.status_code == 200:
            global scalePercentage

            scalePercentage = 50

            def resizeImage(event):
                global imageResize, width, height, imageWidth, imageHeight

                if (event.width / event.height) > imageRatio:
                    height = int(event.height)
                    width = int(height * imageRatio)
                else:
                    width = int(event.width)
                    height = int(width / imageRatio)

                imageWidth = int(event.width / 2)
                imageHeight = int(event.height / 2)

                imageResize = ImageTk.PhotoImage(image.resize((width, height)))
                imageDataCanvas.create_image(
                    imageWidth,
                    imageHeight,
                    anchor=ctk.CENTER,
                    image=imageResize,
                )

            def insertButtonEvent() -> None:
                filePath = ctk.filedialog.askopenfilename(
                    title="Select a signature",
                    filetypes=[
                        ("PNG files", "*.png"),
                    ],
                )

                if filePath:
                    global signature, originalSignature, signatureXPosition, signatureYPosition

                    signature = Image.open(filePath)
                    originalSignature = signature.copy()

                    if signature:
                        signatureXPosition = tk.IntVar(value=0)
                        signatureYPosition = tk.IntVar(value=0)

                        width, height = originalSignature.size
                        signature = originalSignature.resize((int(width * (scalePercentage / 100)), int(height * (scalePercentage / 100))))
                
                        addSignature()

                        moveActionEntry.configure(state="normal")
                        
                        upActionButton.configure(state="normal", fg_color=Dependency.colorPalette["warning"], hover_color=Dependency.colorPalette["warning-dark"], command=lambda: moveButtonEvent("up"))
                        downActionButton.configure(state="normal", fg_color=Dependency.colorPalette["warning"], hover_color=Dependency.colorPalette["warning-dark"], command=lambda: moveButtonEvent("down"))
                        leftActionButton.configure(state="normal", fg_color=Dependency.colorPalette["warning"], hover_color=Dependency.colorPalette["warning-dark"], command=lambda: moveButtonEvent("left"))
                        rightActionButton.configure(state="normal", fg_color=Dependency.colorPalette["warning"], hover_color=Dependency.colorPalette["warning-dark"], command=lambda: moveButtonEvent("right"))
                        
                        scaleDownActionButton.configure(state="normal", fg_color=Dependency.colorPalette["warning"], hover_color=Dependency.colorPalette["warning-dark"], command=lambda: scaleButtonEvent("decrease"))
                        scaleUpActionButton.configure(state="normal", fg_color=Dependency.colorPalette["warning"], hover_color=Dependency.colorPalette["warning-dark"], command=lambda: scaleButtonEvent("increase"))
                        
                        saveActionButton.configure(state="normal", fg_color=Dependency.colorPalette["success"], hover_color=Dependency.colorPalette["success-dark"])

                else:
                    Message.errorMessage(
                        "Signature Failed To Be Inserted"
                    )

            def moveButtonEvent(direction):
                if direction == "up":
                    signatureYPosition.set(signatureYPosition.get() - moveValue.get())
                elif direction == "down":
                    signatureYPosition.set(signatureYPosition.get() + moveValue.get())
                elif direction == "left":
                    signatureXPosition.set(signatureXPosition.get() - moveValue.get())
                elif direction == "right":
                    signatureXPosition.set(signatureXPosition.get() + moveValue.get())

                addSignature()

            def scaleButtonEvent(type):
                global signature, scalePercentage
                
                scalePercentage = scalePercentage * 1.1 if type == "increase" else scalePercentage * 0.9
                width, height = originalSignature.size
                
                signature = originalSignature.resize((int(width * (scalePercentage / 100)), int(height * (scalePercentage / 100))))
                
                addSignature()

            def addSignature() -> None :
                image.paste(originalImage, (0, 0))
                image.paste(signature, (signatureXPosition.get(), signatureYPosition.get()), signature)
                
                displaySignature()

            def displaySignature() -> None:
                global imageResize

                imageResize = ImageTk.PhotoImage(image.resize((width, height)))
                imageDataCanvas.create_image(
                    imageWidth,
                    imageHeight,
                    anchor=ctk.CENTER,
                    image=imageResize,
                )

            def saveButtonEvent() -> None:
                global imageResize

                if Message.confirmationMessage():
                    imageByte = BytesIO()
                    image.save(imageByte, format='PNG')
                    imageByte = imageByte.getvalue()
                    
                    response = None
                    try:
                        response = requests.post(
                            f"{Dependency.host}/api/document/sign/{id}",
                            files={
                                "file": (
                                    f"{(requests.get(f"{Dependency.host}/api/document/{id}").json())["data"]["title"]}.png",
                                    imageByte,
                                    'image/png'
                                )
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
                                self.documentSignFrame, id
                            )

                        else:
                            Message.errorMessage(response["message"])

            image = Image.open(BytesIO(response.content))
            originalImage = image.copy() 
            imageRatio = image.size[0] / image.size[1]

            imageDataCanvas = tk.Canvas(
                dataContainerFrame, bg=Dependency.colorPalette["main"], bd=2
            )
            imageDataCanvas.grid(
                row=0, column=0, columnspan=2, pady=(0, 10), sticky="nsew"
            )

            imageDataCanvas.bind("<Configure>", resizeImage)

            actionDataFrame = ctk.CTkFrame(
                dataContainerFrame,
                corner_radius=0,
                fg_color="transparent",
            )
            actionDataFrame.rowconfigure([0, 1], weight=1)
            actionDataFrame.columnconfigure([0, 1, 2, 3, 4], weight=1)
            actionDataFrame.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="nsew")

            moveValue = ctk.IntVar()
            moveValue.set(10)
            moveActionEntry = ctk.CTkEntry(
                actionDataFrame,
                height=36,
                textvariable=moveValue,
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=18,
                    weight="bold",
                ),
                justify="center",
                text_color=Dependency.colorPalette["text"],
                fg_color="transparent",
                border_color=Dependency.colorPalette["text"],
                state="disabled",
            )
            moveActionEntry.grid(
                row=0,
                column=0,
                padx=(0, 5),
                pady=(0, 5),
                sticky="nsew",
            )

            ctk.CTkButton(
                actionDataFrame,
                height=36,
                image=ctk.CTkImage(
                    Image.open(Utility.getIcon(f"back.png")),
                    size=(22, 22),
                ),
                text="Back",
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=18,
                    weight="bold",
                ),
                cursor="hand2",
                corner_radius=8,
                text_color=Dependency.colorPalette["text"],
                fg_color=Dependency.colorPalette["danger"],
                hover_color=Dependency.colorPalette["danger-dark"],
                command=backButtonEvent,
            ).grid(
                row=1,
                column=0,
                padx=(0, 5),
                sticky="nsew",
            )



            scaleDownActionButton = ctk.CTkButton(
                actionDataFrame,
                height=36,
                image=ctk.CTkImage(
                    Image.open(Utility.getIcon("sign/scale-down.png")),
                    size=(22, 22),
                ),
                text="",
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=18,
                    weight="bold",
                ),
                cursor="hand2",
                corner_radius=8,
                text_color=Dependency.colorPalette["text"],
                fg_color=Dependency.colorPalette["background-light"],
                hover_color=Dependency.colorPalette["background-light"],
                command=lambda :None,
            )
            scaleDownActionButton.grid(
                row=0,
                column=1,
                padx=(0, 5),
                pady=(0, 5),
                sticky="nsew",
            )

            leftActionButton = ctk.CTkButton(
                actionDataFrame,
                height=36,
                image=ctk.CTkImage(
                    Image.open(Utility.getIcon("sign/left.png")),
                    size=(22, 22),
                ),
                text="",
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=18,
                    weight="bold",
                ),
                cursor="hand2",
                corner_radius=8,
                text_color=Dependency.colorPalette["text"],
                fg_color=Dependency.colorPalette["background-light"],
                hover_color=Dependency.colorPalette["background-light"],
                command=lambda: None,
            )
            leftActionButton.grid(
                row=1,
                column=1,
                padx=(0, 5),
                sticky="nsew",
            )



            upActionButton = ctk.CTkButton(
                actionDataFrame,
                height=36,
                image=ctk.CTkImage(
                    Image.open(Utility.getIcon(f"sign/up.png")),
                    size=(22, 22),
                ),
                text="",
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=18,
                    weight="bold",
                ),
                cursor="hand2",
                corner_radius=8,
                text_color=Dependency.colorPalette["text"],
                fg_color=Dependency.colorPalette["background-light"],
                hover_color=Dependency.colorPalette["background-light"],
                command=lambda: None,
            )
            upActionButton.grid(
                row=0,
                column=2,
                padx=(0, 5),
                pady=(0, 5),
                sticky="nsew",
            )

            downActionButton = ctk.CTkButton(
                actionDataFrame,
                height=36,
                image=ctk.CTkImage(
                    Image.open(Utility.getIcon("sign/down.png")),
                    size=(22, 22),
                ),
                text="",
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=18,
                    weight="bold",
                ),
                cursor="hand2",
                corner_radius=8,
                text_color=Dependency.colorPalette["text"],
                fg_color=Dependency.colorPalette["background-light"],
                hover_color=Dependency.colorPalette["background-light"],
                command=lambda: None,
            )
            downActionButton.grid(
                row=1,
                column=2,
                padx=(0, 5),
                sticky="nsew",
            )



            scaleUpActionButton = ctk.CTkButton(
                actionDataFrame,
                height=36,
                image=ctk.CTkImage(
                    Image.open(Utility.getIcon("sign/scale-up.png")),
                    size=(22, 22),
                ),
                text="",
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=18,
                    weight="bold",
                ),
                cursor="hand2",
                corner_radius=8,
                text_color=Dependency.colorPalette["text"],
                fg_color=Dependency.colorPalette["background-light"],
                hover_color=Dependency.colorPalette["background-light"],
                command=lambda: None,
            )
            scaleUpActionButton.grid(
                row=0,
                column=3,
                padx=(0, 5),
                pady=(0, 5),
                sticky="nsew",
            )

            rightActionButton = ctk.CTkButton(
                actionDataFrame,
                height=36,
                image=ctk.CTkImage(
                    Image.open(Utility.getIcon("sign/right.png")),
                    size=(22, 22),
                ),
                text="",
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=18,
                    weight="bold",
                ),
                cursor="hand2",
                corner_radius=8,
                text_color=Dependency.colorPalette["text"],
                fg_color=Dependency.colorPalette["background-light"],
                hover_color=Dependency.colorPalette["background-light"],
                command=lambda: None,
            )
            rightActionButton.grid(
                row=1,
                column=3,
                padx=(0, 5),
                sticky="nsew",
            )



            ctk.CTkButton(
                actionDataFrame,
                height=36,
                image=ctk.CTkImage(
                    Image.open(Utility.getIcon(f"sign.png")),
                    size=(22, 22),
                ),
                text="Insert",
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=18,
                    weight="bold",
                ),
                cursor="hand2",
                corner_radius=8,
                text_color=Dependency.colorPalette["text"],
                fg_color=Dependency.colorPalette["warning"],
                hover_color=Dependency.colorPalette["warning-dark"],
                command=insertButtonEvent,
            ).grid(
                row=0,
                column=4,
                pady=(0, 5),
                sticky="nsew",
            )

            saveActionButton = ctk.CTkButton(
                actionDataFrame,
                height=36,
                image=ctk.CTkImage(
                    Image.open(Utility.getIcon("sign/save.png")),
                    size=(22, 22),
                ),
                text="Save",
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=18,
                    weight="bold",
                ),
                cursor="hand2",
                corner_radius=8,
                text_color=Dependency.colorPalette["text"],
                fg_color=Dependency.colorPalette["background-light"],
                hover_color=Dependency.colorPalette["background-light"],
                command=saveButtonEvent,
            )
            saveActionButton.grid(
                row=1,
                column=4,
                sticky="nsew",
            )


        else:
            Component.labelDataComponent(
                dataContainerFrame,
                text="Data Not Found",
                size=24,
                row=0,
                columnspan=2,
                padx=80,
                pady=80,
            )

            Component.buttonDataComponent(
                dataContainerFrame,
                text="Back",
                icon="back",
                mainColor=Dependency.colorPalette["danger"],
                hoverColor=Dependency.colorPalette["danger-dark"],
                event=backButtonEvent,
                row=1,
            )

    def documentAccessFrame(self, page: int = 1, id: int = None) -> None:
        def addButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.documentAccessAddFrame, id)

        def removeButtonEvent(idAccess: int) -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(
                self.documentAccessRemoveFrame, id, idAccess
            )

        def backButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.documentFrame)

        self.sidebarId = 2

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=31)

        Component.sidebarComponent()

        contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        contentFrame.rowconfigure(1, weight=1)
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

        Component.titleContentComponent(contentFrame, title="DOCUMENT", row=0)

        containerContentFrame = ctk.CTkFrame(
            contentFrame,
            corner_radius=8,
            fg_color=Dependency.colorPalette["main"],
        )
        containerContentFrame.columnconfigure(0, weight=1)
        containerContentFrame.grid(row=1, column=0, pady=(0, 20), sticky="nsew")

        Component.titleContainerComponent(
            containerContentFrame, title="Access Document Table", row=0
        )

        Component.lineHorizontalComponent(containerContentFrame, row=1)

        accessTotal = None
        response = None
        try:
            accessTotal = requests.get(
                f"{Dependency.host}/api/access/document/{id}/count",
            ).json()["data"]["total"]

            response = requests.get(
                f"{Dependency.host}/api/access/document/{id}",
                json={"count": 10, "page": page},
            ).json()

        except:
            pass

        if (
            response != None
            and response["success"] == True
            and len(response["data"]) > 0
            and accessTotal != None
        ):
            countArray = []
            idArray = []
            usernameArray = []
            for documentIndex, documentObject in enumerate(response["data"]):
                countArray.append((10 * (page - 1)) + documentIndex + 1)
                idArray.append(documentObject["_id"])
                usernameArray.append(documentObject["user_extend"]["username"])

            Component.tableDataComponent(
                containerContentFrame,
                currentPage=page,
                totalPage=((accessTotal - 1) // 10) + 1,
                framePage=app.documentAccessFrame,
                tag=id,
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
                        "header": "Username",
                        "data": usernameArray,
                        "align": "left",
                    },
                ],
                actionArray=[
                    {
                        "id": 1,
                        "text": "Remove",
                        "icon": "remove",
                        "mainColor": Dependency.colorPalette["danger"],
                        "hoverColor": Dependency.colorPalette["danger-dark"],
                        "event": removeButtonEvent,
                        "optional": False,
                    },
                ],
                row=2,
            )

        else:
            Component.labelDataComponent(
                containerContentFrame,
                text="Data Not Found",
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
            event=addButtonEvent,
            row=0,
        )

        Component.buttonDataComponent(
            dataContainerFrame,
            text="Back",
            icon="back",
            mainColor=Dependency.colorPalette["danger"],
            hoverColor=Dependency.colorPalette["danger-dark"],
            event=backButtonEvent,
            row=1,
        )

    def documentAccessAddFrame(self, id: int) -> None:
        def addButtonEvent() -> None:
            if Message.confirmationMessage():
                username = usernameDataComboBox.get()

                if "" not in [username]:
                    response = None
                    try:
                        response = requests.post(
                            f"{Dependency.host}/api/access/add",
                            json={
                                "username_user": username,
                                "id_document": id,
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
                                self.documentAccessAddFrame, id
                            )

                        else:
                            Message.errorMessage(response["message"])

                else:
                    Message.errorMessage("Please Fill Out The Form")

        def backButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.documentAccessFrame, 1, id)

        self.sidebarId = 2

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=31)

        Component.sidebarComponent()

        contentFrame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        contentFrame.rowconfigure(1, weight=1)
        contentFrame.columnconfigure(0, weight=1)
        contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

        Component.titleContentComponent(contentFrame, title="DOCUMENT", row=0)

        containerContentFrame = ctk.CTkFrame(
            contentFrame,
            corner_radius=8,
            fg_color=Dependency.colorPalette["main"],
        )
        containerContentFrame.columnconfigure(0, weight=1)
        containerContentFrame.grid(row=1, column=0, pady=(0, 20), sticky="nsew")

        Component.titleContainerComponent(
            containerContentFrame, title="Add Access Document", row=0
        )
        Component.lineHorizontalComponent(containerContentFrame, row=1)

        dataContainerFrame = ctk.CTkFrame(
            containerContentFrame,
            corner_radius=0,
            fg_color="transparent",
        )
        dataContainerFrame.columnconfigure([0, 1], weight=1)
        dataContainerFrame.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="nsew")

        response = None
        try:
            response = requests.get(
                f"{Dependency.host}/api/document/access/available"
            ).json()

        except:
            pass
        
        option = []
        if response != None and response["success"] == True:
            for userObject in response["data"]:
                option.append(userObject["username"])

        else:
            option.append("Data not found")
        
        usernameDataComboBox = Component.comboBoxDataComponent(
            dataContainerFrame,
            title="Username",
            placeholder="select username",
            value=None,
            option=option,
            state=True,
            row=0,
            column=0,
            span=2,
        )

        Component.buttonDataComponent(
            dataContainerFrame,
            text="Add",
            icon="add",
            mainColor=Dependency.colorPalette["success"],
            hoverColor=Dependency.colorPalette["success-dark"],
            event=addButtonEvent,
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

    def documentAccessRemoveFrame(self, id: int, idAccess: int) -> None:
        def removeButtonEvent() -> None:
            if Message.confirmationMessage():
                response = None

                try:
                    response = requests.delete(
                        f"{Dependency.host}/api/access/remove/{idAccess}",
                    ).json()

                except requests.ConnectionError:
                    Message.errorMessage("Make Sure You Are Connected To The Internet")

                except:
                    Message.errorMessage("Server Error")

                if response != None:
                    if response["success"] == True:
                        Message.successMessage(response["message"])

                        Call.resetFrameCall()
                        Middleware.refreshSessionDataMiddleware(
                            self.documentAccessFrame, 1, id
                        )

                    else:
                        Message.errorMessage(response["message"])

                        if response["status"] == 404:
                            Call.logoutCall()

        def backButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.documentAccessFrame, 1, id)

        response = None
        try:
            response = requests.get(
                f"{Dependency.host}/api/access/{idAccess}"
            ).json()

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
            contentFrame.rowconfigure(1, weight=1)
            contentFrame.columnconfigure(0, weight=1)
            contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

            Component.titleContentComponent(contentFrame, title="DOCUMENT", row=0)

            containerContentFrame = ctk.CTkFrame(
                contentFrame,
                corner_radius=8,
                fg_color=Dependency.colorPalette["main"],
            )
            containerContentFrame.columnconfigure(0, weight=1)
            containerContentFrame.grid(row=1, column=0, pady=(0, 20), sticky="nsew")

            Component.titleContainerComponent(
                containerContentFrame, title="Remove Access Document", row=0
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

            Component.entryDataComponent(
                dataContainerFrame,
                title="Username",
                placeholder="username",
                value=response["data"]["user_extend"]["username"],
                state=False,
                row=0,
                column=0,
                span=2,
            )

            Component.buttonDataComponent(
                dataContainerFrame,
                text="Remove",
                icon="remove",
                mainColor=Dependency.colorPalette["danger"],
                hoverColor=Dependency.colorPalette["danger-dark"],
                event=removeButtonEvent,
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

    def documentRemoveFrame(self, id: int) -> None:
        def removeButtonEvent() -> None:
            if Message.confirmationMessage():
                response = None

                try:
                    response = requests.delete(
                        f"{Dependency.host}/api/document/remove/{id}",
                    ).json()

                except requests.ConnectionError:
                    Message.errorMessage("Make Sure You Are Connected To The Internet")

                except:
                    Message.errorMessage("Server Error")

                if response != None:
                    if response["success"] == True:
                        Message.successMessage(response["message"])

                        Call.resetFrameCall()
                        Middleware.refreshSessionDataMiddleware(self.documentFrame)

                    else:
                        Message.errorMessage(response["message"])

                        if response["status"] == 404:
                            Call.logoutCall()

        def backButtonEvent() -> None:
            Call.resetFrameCall()
            Middleware.refreshSessionDataMiddleware(self.documentFrame)

        response = None
        try:
            response = requests.get(f"{Dependency.host}/api/document/{id}").json()

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
            contentFrame.rowconfigure(1, weight=1)
            contentFrame.columnconfigure(0, weight=1)
            contentFrame.grid(row=0, column=1, padx=20, sticky="nsew")

            Component.titleContentComponent(contentFrame, title="DOCUMENT", row=0)

            containerContentFrame = ctk.CTkFrame(
                contentFrame,
                corner_radius=8,
                fg_color=Dependency.colorPalette["main"],
            )
            containerContentFrame.columnconfigure(0, weight=1)
            containerContentFrame.grid(row=1, column=0, pady=(0, 20), sticky="nsew")

            Component.titleContainerComponent(
                containerContentFrame, title="Remove Document", row=0
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

            Component.entryDataComponent(
                dataContainerFrame,
                title="Code",
                placeholder="code",
                value=response["data"]["code"],
                state=False,
                row=0,
                column=0,
            )
            Component.entryDataComponent(
                dataContainerFrame,
                title="Title",
                placeholder="title",
                value=response["data"]["title"],
                state=False,
                row=0,
                column=1,
            )

            Component.entryDataComponent(
                dataContainerFrame,
                title="Category",
                placeholder="category",
                value=response["data"]["category"],
                state=False,
                row=1,
                column=0,
            )
            Component.entryDataComponent(
                dataContainerFrame,
                title="Description",
                placeholder="description",
                value=response["data"]["description"],
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

    skipObject = {
        "status": False,
        "id": 4,
        "frame": app.documentFrame,
        "tag": None,
    }

    app.mainloop()

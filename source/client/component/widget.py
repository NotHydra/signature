import customtkinter as ctk

from PIL import Image

from environment import Utility, Dependency


class Widget:
    def lineWidget(self, master, row, column, weight=2):
        ctk.CTkFrame(
            master,
            height=weight,
            corner_radius=0,
            fg_color=Dependency.colorPalette["text"],
        ).grid(row=row, column=column, sticky="nsew")

    def sidebarWidget(self) -> None:
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
                self.forgetFrameEvent()
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
                    self.forgetFrameEvent()
                    self.home()

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
                        self.forgetFrameEvent()
                        self.user()

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

            self.lineWidget(contentSidebarFrame, 1, 0)

            profileGroup()

            self.lineWidget(contentSidebarFrame, 3, 0)

            itemGroup()

        def footerGroup():
            def logoutGroup():
                def logoutButtonEvent():
                    if self.showConfirmation():
                        self.logoutEvent()

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

            self.lineWidget(footerSidebarFrame, 1, 0)

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

    def titleContentWidget(self, master, text) -> None:
        titleContentLabel = ctk.CTkLabel(
            master,
            text=text,
            font=ctk.CTkFont(
                family=Dependency.fontFamily["main"],
                size=36,
                weight="bold",
            ),
            text_color=Dependency.colorPalette["text"],
        )
        titleContentLabel.grid(row=0, column=0, pady=5, sticky="nsw")

    def dataContainerWidget(self, master, row, entryArray, buttonArray) -> None:
        def entry(text, placeholder, value, state, row, column):
            ctk.CTkLabel(
                dataContainerFrame,
                text=text,
                font=ctk.CTkFont(
                    family=Dependency.fontFamily["main"],
                    size=20,
                    weight="bold",
                ),
                text_color=Dependency.colorPalette["text"],
            ).grid(
                row=0 + row,
                column=column,
                padx=(0, 5) if column == 0 else (5, 0),
                pady=(0, 5),
                sticky="nsw",
            )

            entryValue = ctk.StringVar()
            entryValue.set(value)
            ctk.CTkEntry(
                dataContainerFrame,
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
            ).grid(
                row=1 + row,
                column=column,
                padx=(0, 5) if column == 0 else (5, 0),
                pady=(0, 10),
                sticky="nsew",
            )

        def button(text, icon, color, hover, event, row):
            ctk.CTkButton(
                dataContainerFrame,
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
                fg_color=color,
                hover_color=hover,
                event=event,
            ).grid(
                row=row,
                column=0,
                columnspan=2,
                pady=(0, 10),
                sticky="nsew",
            )

        dataContainerFrame = ctk.CTkFrame(
            master,
            corner_radius=0,
            fg_color="transparent",
        )
        dataContainerFrame.columnconfigure([0, 1], weight=1)
        dataContainerFrame.grid(row=row, column=0, padx=10, pady=(5, 0), sticky="nsew")

        for entryRowIndex, entryRowObject in enumerate(entryArray):
            for entryIndex, entryObject in enumerate(entryRowObject["entry"]):
                entry(
                    entryObject["text"],
                    entryObject["placeholder"],
                    entryObject["value"],
                    entryObject["state"],
                    entryRowIndex * 2,
                    entryIndex % 2,
                )

        for buttonIndex, buttonObject in enumerate(buttonArray):
            button(
                buttonObject["text"],
                buttonObject["icon"],
                buttonObject["color"],
                buttonObject["hover"],
                buttonObject["event"],
                buttonIndex + (len(entryArray) * 2),
            )

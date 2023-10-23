from CTkMessagebox import CTkMessagebox


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

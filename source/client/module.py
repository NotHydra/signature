import os


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

    skip = True

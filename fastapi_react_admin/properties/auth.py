from ..entities import BaseProperty


class AuthProperty(BaseProperty):
    name: str = "Auth"
    package: str = "./Auth"
    property: str = "authProvider"
    use_braces: bool = True
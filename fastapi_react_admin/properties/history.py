from .. entities import BaseProperty


class HistoryProperty(BaseProperty):
    name: str = "createBrowserHistory"
    package: str = "history"
    property: str = "history"
    use_braces: bool = True
    initialize: bool = True
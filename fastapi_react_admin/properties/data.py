from .. utils import SafeOption
from .. entities import BaseProperty


class DataProperty(BaseProperty):
    name: str = "simpleRestProvider"
    package: str = "ra-data-simple-rest"
    property: str = "dataProvider"

    def __init__(self) -> None:
        from .. config import data_provider
        if not self.inits:
            self.inits = [data_provider, SafeOption("httpClient", "./Client", True)]
        super().__init__()

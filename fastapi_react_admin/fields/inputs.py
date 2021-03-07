from .. entities import BaseField
from .. constants import REGULAR, FOREIGN_KEY


class ReactInput(BaseField):
    """
    React Input
    """
    def build(self) -> str:
        build: str = str()
        if self.type == REGULAR:
            build: str = self._build_regular()
        elif self.type == FOREIGN_KEY:
            build: str = self._build_fk()
        return build

    def _build_fk(self) -> str:
        regular_input: str = (
            f"<ReactAdmin.SelectInput "
            f"optionText='{self.description.get('source_field')}' "
            f"/> \n"
        )
        fk_input: str = (
            f"<ReactAdmin.ReferenceInput "
            f"source='{self.field}_id' "
            f"reference='{self.field}'> "
            f"{regular_input} "
            f"</ReactAdmin.ReferenceInput> \n"
        )
        return fk_input

    def _build_regular(self) -> str:
        regular_input_type: str = self.mapping.get(self.description["type"])
        regular_input: str = f"<{regular_input_type} source='{self.field}' /> \n"
        return regular_input
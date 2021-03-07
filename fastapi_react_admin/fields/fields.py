from .. entities import BaseField
from .. constants import REGULAR, FOREIGN_KEY


class ReactField(BaseField):
    """
    React field
    """
    def build(self) -> str:
        build: str = str()
        if self.type == REGULAR:
            build: str = self._build_regular()
        elif self.type == FOREIGN_KEY:
            build: str = self._build_fk()
        return build

    def _build_fk(self) -> str:
        regular_field: str = (
            f"<ReactAdmin.TextField "
            f"source='{self.description.get('source_field')}' "
            f"/> \n"
        )
        fk_field: str = (
            f"<ReactAdmin.ReferenceField "
            f"source='{self.field}_id' "
            f"reference='{self.field}'> "
            f"{regular_field} "
            f"</ ReactAdmin.ReferenceField>"
        )
        return fk_field

    def _build_regular(self) -> str:
        regular_field_type: str = self.mapping.get(self.description["type"])
        regular_field: str = f"<{regular_field_type} source='{self.field}' /> \n"
        return regular_field
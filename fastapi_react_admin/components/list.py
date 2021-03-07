from tortoise import Model
from .. fields import ReactField, ReactInput
from .. entities import BaseComponent


class ReactListComponent(BaseComponent):
    """
    List react admin component
    """
    template: str = """
                    export const {name} = props => (
                    <ReactAdmin.List {props}>
                        <ReactAdmin.Datagrid rowClick="edit">
                            {fields}
                        </ReactAdmin.Datagrid>
                    </ReactAdmin.List>
                    );
                    """
    destination: str = "list"
    base_fields_type: str = "fields"

    def __init__(
            self,
            model: Model,
            fields: list[ReactField],
            inputs: list[ReactInput],
    ) -> None:
        self.name = f"{model.__name__}List"
        self.fields = " ".join([field.build() for field in fields])
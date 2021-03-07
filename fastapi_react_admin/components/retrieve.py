from tortoise import Model
from .. fields import ReactInput, ReactField
from .. entities import BaseComponent


class ReactRetrieveComponent(BaseComponent):
    """
    Retrieve react admin component
    """
    template: str = """
                    export const {name} = props => (
                    <ReactAdmin.Show {props}>
                        <ReactAdmin.SimpleShowLayout>
                            {fields}
                        </ReactAdmin.SimpleShowLayout>
                    </ReactAdmin.Show>
                    );
                    """
    destination: str = "show"
    base_fields_type: str = "fields"

    def __init__(
            self,
            model: Model,
            fields: list[ReactField],
            inputs: list[ReactInput],
    ) -> None:
        self.name = f"{model.__name__}Show"
        self.fields = " ".join([field.build() for field in fields])
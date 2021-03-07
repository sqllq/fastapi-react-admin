from tortoise import Model
from .. fields import ReactInput, ReactField
from .. entities import BaseComponent


class ReactCreateComponent(BaseComponent):
    """
    Create react admin component
    """
    template: str = """
                    export const {name} = props => (
                    <ReactAdmin.Create {props}>
                        <ReactAdmin.SimpleForm>
                            {inputs}
                        </ReactAdmin.SimpleForm>
                    </ReactAdmin.Create>
                    );
                    """
    destination: str = "create"
    base_fields_type: str = "inputs"

    def __init__(
            self,
            model: Model,
            fields: list[ReactField],
            inputs: list[ReactInput],
    ) -> None:
        self.name = f"{model.__name__}Create"
        self.inputs = " ".join([input.build() for input in inputs])
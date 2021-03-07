from tortoise import Model
from .. fields import ReactInput, ReactField
from .. entities import BaseComponent


class ReactUpdateComponent(BaseComponent):
    """
    Update react admin component
    """
    template: str = """
                    export const {name} = props => (
                    <ReactAdmin.Edit {props}>
                        <ReactAdmin.SimpleForm>
                            {inputs}
                        </ReactAdmin.SimpleForm>
                    </ReactAdmin.Edit>
                    );
                    """
    destination: str = "edit"
    base_fields_type: str = "inputs"

    def __init__(
            self,
            model: Model,
            fields: list[ReactField],
            inputs: list[ReactInput],
    ) -> None:
        self.name = f"{model.__name__}Edit"
        self.inputs = " ".join([input.build() for input in inputs])
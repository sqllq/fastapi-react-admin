from typing import Coroutine, Union
from fastapi import APIRouter
from pydantic import BaseModel
from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from . utils import SafeOption


class BaseComponent(object):
    """
    Base Component
    """
    props: str = "{...props}"
    template: str
    destination: str
    base_fields_type: str

    def build(self) -> str:
        formats: dict[str, str] = {
            "name": self.name,
            "props": self.props,
            self.base_fields_type: getattr(self, self.base_fields_type)
        }
        build: str = self.template.format(**formats)
        return build

    def build_resource(self) -> str:
        resource: str = f"{self.destination}=" + "{" + self.name + "}"
        return resource

    def build_import(self) -> str:
        imprt: str = self.name + ", "
        return imprt


class BaseRouter(object):
    """
    Base Router
    """
    def __init__(
            self,
            router: APIRouter,
            model: Model,
            list_size: int,
    ) -> None:
        self.model: Model = model
        self.router: APIRouter = router
        self.list_size: int = list_size
        self.pydantic_single: BaseModel = pydantic_model_creator(self.model)
        self.pydantic_queryset: BaseModel = pydantic_queryset_creator(self.model)

    def build(self) -> Coroutine:
        build: Coroutine = self.get_route()(self.get_view())
        return build


class BaseField(object):
    """
    Base Field
    """
    def __init__(
            self,
            type: str,
            field: str,
            mapping: dict[str, str],
            description: dict[str, str]

    ) -> None:
        self.type: str = type
        self.field: str = field
        self.mapping: dict[str, str] = mapping
        self.description: dict[str, str] = description


class BaseProperty(object):
    """
    Base Property
    """
    name: str
    package: str
    property: str
    use_braces: bool = False
    initialize: bool = False

    inits: list[Union[str, SafeOption]] = []
    options: dict[str, Union[str, SafeOption]] = {}

    def build_import(self) -> str:
        imprt: str = f"import {self.name} from '{self.package}'; \n"
        if self.use_braces:
            imprt: str = "import" + "{" + self.name + "}" + f"from '{self.package}'; \n"
        for init in self.inits:
            if isinstance(init, SafeOption):
                if init.use_braces:
                    imprt += "import" + "{" + init.option + "}" + f"from '{init.path}'; \n"
                else:
                    imprt += f"import {init.option} from '{init.path}'; \n"
        for _, option in self.options.items():
            if isinstance(option, SafeOption):
                if option.use_braces:
                    imprt += "import" + "{" + option.option + "}" + f"from '{option.path}'; \n"
                else:
                    imprt += f"import {option.option} from '{option.path}'; \n"
        return imprt

    def build_property(self) -> str:
        args: str = str()
        kwargs: str = str()
        for init in self.inits:
            if isinstance(init, SafeOption):
                args += f"{str(init)}, "
            else:
                args += f"'{init}', "
        for option, value in self.options:
            if isinstance(value, SafeOption):
                kwargs += f"{option}:{str(value)}, "
            else:
                kwargs += f"{option}:'{value}', "
        if kwargs:
            kwargs: str = "{" + kwargs + "}"
        values: str = args or kwargs
        if values or self.initialize:
            property: str = f"{self.property}=" + "{" + f"{self.name}({values})" + "} "
        else:
            property: str = f"{self.property}=" + "{" + f"{self.name}" + "} "
        return property


class BaseModelAdmin(object):
    """
    Base Model Admin
    """
    size: int
    model: Model

    options: dict[str, Union[str, SafeOption]]
    references: dict[str, str]

    routers: list[BaseRouter]
    components: list[BaseComponent]

    fields_mapping: dict[str, str]
    inputs_mapping: dict[str, str]

    _template: str = """
                    {react_import}
                    {admin_import}
                    {components}
                    """

    _react_import: str = "import * as React from 'react';"
    _admin_import: str = "import * as ReactAdmin from 'react-admin';"
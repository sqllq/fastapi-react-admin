from os import mkdir
from typing import Any
from os.path import join
from tortoise import Model
from fastapi import APIRouter
from collections import OrderedDict

from .. fields import ReactInput, ReactField
from .. constants import FOREIGN_KEY, REGULAR
from .. mappings import (
    tortoise_fields_mapping,
    tortoise_inputs_mapping,
)
from .. components import (
    ReactListComponent,
    ReactUpdateComponent,
    ReactCreateComponent,
    ReactRetrieveComponent
)
from .. routers import (
    ReactListRouter,
    ReactCreateRouter,
    ReactDeleteRouter,
    ReactUpdateRouter,
    ReactRetrieveRouter
)


class ReactTortoiseModelAdmin(object):
    size: int = 10
    model: Model

    options: dict[Any, Any] = {}
    references: dict[Any, Any] = {}

    components: list = [
        ReactListComponent,
        ReactUpdateComponent,
        ReactCreateComponent,
        ReactRetrieveComponent
    ]

    routers: list = [
        ReactListRouter,
        ReactCreateRouter,
        ReactDeleteRouter,
        ReactUpdateRouter,
        ReactRetrieveRouter
    ]

    fields_mapping: dict[str, str] = tortoise_fields_mapping
    inputs_mapping: dict[str, str] = tortoise_inputs_mapping

    _react_import: str = "import * as React from 'react';"
    _admin_import: str = "import * as ReactAdmin from 'react-admin';"
    _template: str = """
                     {react_import}
                     {admin_import}
                     {components}
                     """

    def __init__(self) -> None:
        from .. config import (
            router,
            base_dir,
            src_output_dir,
            models_output_dir
        )
        from ..utils import SafeOption

        self._safe: SafeOption = SafeOption
        self._router: APIRouter = router

        self._base_dir: str = base_dir
        self._src_output_dir: str = src_output_dir
        self._models_output_dir: str = models_output_dir

        self._fk_fields: OrderedDict = None
        self._regular_fields: OrderedDict = None
        self._m2m_fields: OrderedDict = None

    def compile(self) -> None:
        self._validate()
        js_dir: str = join(
            self._base_dir,
            self._src_output_dir,
            self._models_output_dir,
            f"{self.model.__name__.lower()}.js"
        )
        components: str = self._build_components()
        compiled: str = self._template.format(
            react_import=self._react_import,
            admin_import=self._admin_import,
            components=components
        )
        try:
            with open(js_dir, "w") as file:
                file.write(compiled)
        except FileNotFoundError:
            mkdir(self._src_output_dir)
            try:
                with open(js_dir, "w") as file:
                    file.write(compiled)
            except FileNotFoundError:
                models_dir: str = join(
                    self._base_dir,
                    self._src_output_dir,
                    self._models_output_dir
                )
                mkdir(models_dir)
                with open(js_dir, "w") as file:
                    file.write(compiled)

    def route(self) -> None:
        self._validate()
        routers = self._build_routers()
        for router in routers:
            router.build()

    def build_resource(self) -> str:
        resources: str = str()
        for component in self.components:
            resources += component(
                    model=self.model,
                    fields=list(),
                    inputs=list(),
                ).build_resource() + "\n"
        resource: str = (
            f"<ReactAdmin.Resource "
            f"name='{self.model.__name__.lower()}' "
            f"{resources}"
            f"/>"
        )
        if self.options:
            options: str = str()
            for option, value in self.options.items():
                if isinstance(value, self._safe):
                    options += f"{option}:{str(value)},"
                else:
                    options += f"{option}:'{value}',"
            options: str = "{{" + options + "}}"
            resource: str = (
                f"<ReactAdmin.Resource "
                f"name='{self.model.__name__.lower()}' "
                f"{resources} "
                f"options={options}/>"
            )
        return resource

    def build_import(self) -> str:
        imports: str = str()
        for component in self.components:
            imports += component(
                model=self.model,
                fields=list(),
                inputs=list(),
            ).build_import()
        imports: str = (
                "import " + "{" + imports + "}" +
                f" from './{self._models_output_dir}/{self.model.__name__.lower()}'; \n"
        )
        return imports

    def _build_components(self) -> str:
        js: str = str()
        fk_fields: OrderedDict = self._get_fk_fields()
        regular_fields: OrderedDict = self._get_regular_fields()
        inputs: list = list()
        fields: list = list()
        for field, description in fk_fields.items():
            inputs.append(
                ReactInput(
                    type=FOREIGN_KEY,
                    field=field,
                    description=description,
                    mapping=self.inputs_mapping
                )
            )
            fields.append(
                ReactField(
                    type=FOREIGN_KEY,
                    field=field,
                    description=description,
                    mapping=self.fields_mapping
                )
            )
        for field, description in regular_fields.items():
            inputs.append(
                ReactInput(
                    type=REGULAR,
                    field=field,
                    description=description,
                    mapping=self.inputs_mapping
                )
            )
            fields.append(
                ReactField(
                    type=REGULAR,
                    field=field,
                    description=description,
                    mapping=self.fields_mapping
                )
            )
        for component in self.components:
            js += component(
                model=self.model,
                fields=fields,
                inputs=inputs,
            ).build() + "\n"
        return js

    def _build_routers(self) -> list[object]:
        built: list = list()
        for router in self.routers:
            built.append(
                router(
                    router=self._router,
                    model=self.model,
                    list_size=self.size
                )
            )
        return built

    def _get_regular_fields(self) -> OrderedDict:
        if self._regular_fields:
            return self._regular_fields
        fields_description = self.model.describe()["data_fields"]
        regular_fields = OrderedDict()
        for description in fields_description:
            regular_fields[description["name"]] = dict(
                description=description["description"],
                type=description["field_type"]
            )
        self._regular_fields: OrderedDict = regular_fields
        return self._regular_fields

    def _get_fk_fields(self) -> OrderedDict:
        if self._fk_fields:
            return self._fk_fields
        fields_description = self.model.describe()["fk_fields"]
        fk_fields = OrderedDict()
        for description in fields_description:
            fk_fields[description["name"]] = dict(
                source_field=self.references.get(description["name"], "id")
            )
        self._fk_fields: OrderedDict = fk_fields
        return self._fk_fields

    def _get_m2m_fields(self) -> OrderedDict:
        if self._m2m_fields:
            return self._m2m_fields
        fields_description = self.model.describe()["m2m_fields"]
        m2m_fields = OrderedDict()
        for description in fields_description:
            pass
        self._m2m_fields: OrderedDict = m2m_fields
        return self._m2m_fields

    def _validate(self) -> None:
        assert self.model is not None, f"You must specify the model for {self.__class__.__name__}."
        assert issubclass(self.model, Model), f"{self.model.__name__} must be as subclass of tortoise.Model."
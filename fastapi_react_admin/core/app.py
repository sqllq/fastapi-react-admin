from os import mkdir
from os.path import join
from ..properties import (
    AuthProperty,
    DataProperty,
    HistoryProperty
)


class ReactAppAdmin(object):
    # TODO: add hot reload generation
    properties: list = [
        AuthProperty,
        DataProperty,
        HistoryProperty
    ]

    _name: str = "App.js"
    _react_import: str = "import * as React from 'react';"
    _admin_import: str = "import * as ReactAdmin from 'react-admin';"

    _template: str = """
                     {react_import}
                     {admin_import}
                     {imports}
                     const App = () => ( 
                     <ReactAdmin.Admin {properties}>
                        {resources}
                     </ReactAdmin.Admin>
                     );
                     export default App;
                     """

    def __init__(self, admins: list[object]) -> None:
        from .. config import (
            base_dir,
            src_output_dir,
            models_output_dir,
        )

        self._admins: list[object] = admins

        self._base_dir: str = base_dir
        self._src_output_dir: str = src_output_dir
        self._models_output_dir: str = models_output_dir

    def compile(self) -> None:
        js_dir: str = join(
            self._base_dir,
            self._src_output_dir,
            self._name
        )
        resources: str = self._build_resources()
        imports: str = self._build_imports()
        properties: str = self._build_properties()
        compiled: str = self._template.format(
            react_import=self._react_import,
            admin_import=self._admin_import,
            imports=imports,
            resources=resources,
            properties=properties,
        )
        try:
            with open(js_dir, "w") as file:
                file.write(compiled)
        except FileNotFoundError:
            mkdir(self._src_output_dir)
            with open(js_dir, "w") as file:
                file.write(compiled)

    def _build_resources(self) -> str:
        resources: str = str()
        for admin in self._admins:
            resources += admin.build_resource()
        return resources

    def _build_imports(self) -> str:
        imports: str = str()
        for admin in self._admins:
            imports += admin.build_import()
        for property in self.properties:
            initialized = property()
            imports += initialized.build_import()
        return imports

    def _build_properties(self) -> str:
        properties: str = str()
        for property in self.properties:
            initialized = property()
            properties += initialized.build_property()
        return properties

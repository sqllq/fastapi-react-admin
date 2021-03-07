from os.path import join


class SafeOption(object):
    """
    Simple wrapper to avoid objects of being quoted
    """

    def __init__(
            self,
            option: str,
            path: str,
            use_braces: bool = False
    ) -> None:
        from .config import base_dir, src_output_dir

        self.option: str = option
        self.path: str = path
        self.use_braces: bool = use_braces

        self._name: str = f"{path[2:]}.js"
        self._base_dir: str = base_dir
        self._src_output_dir: str = src_output_dir

    def __str__(self) -> str:
        self._validate()
        return self.option

    def _validate(self) -> None:
        js_dir: str = join(
            self._base_dir,
            self._src_output_dir,
            self._name
        )
        try:
            with open(js_dir, "r"):
                pass
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Cannot find {js_dir} to complete SafeOption {self.option} initialization."
            )
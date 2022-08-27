class RetObject:
    option_dict: dict[str] = {}
    aliases: dict[str] = {}
    macros: dict[str] = {}
    exit_code: int = 0
    module: str = 0
    activated_module_list: list[str] = []
    histfile: str = None
    command_found: bool = False

    def __init__(self) -> None:
        pass
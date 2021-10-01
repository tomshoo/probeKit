from config import colors as _colors

class unalias:
    def __init__(self, aliases: dict ,alias_list: list):
        self.alias_list = alias_list
        self.ret_list = [aliases, 0]

    def run(self) -> list:
        if not self.alias_list:
            self.ret_list[1] = 1
            print(f'{_colors.FALERT}[-] Error: no imput provided')
            return self.ret_list

        for alias in self.alias_list:
            self.unassign(alias)

        return self.ret_list

    def unassign(self, alias: str) -> None:
        exit_code: int = self.ret_list[1]
        aliases: dict = self.ret_list[0]

        if alias in aliases:
            del(aliases[alias])
            exit_code = 0

        else:
            print(f'{_colors.FALERT}[-] Error: no such alias \'{_colors.FURGENT}{alias}{_colors.FALERT}\' exists')
            exit_code = 1

        self.ret_list[0] = aliases
        self.ret_list[1] = exit_code
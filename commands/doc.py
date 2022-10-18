import re
import platform
from modules.util.extra import get_args
import config
from os import path
from rich import console, markdown, traceback
from fuzzywuzzy import process

from . import Runnable

traceback.install()
Console = console.Console(soft_wrap=True)

colors = config.colors


class Docs(Runnable):
    def run(self):
        root_dir = path.dirname(config.__file__)
        docs_dir = path.join(root_dir, "DOCS")
        if not self.args:
            Console.print(f"[{colors.FALERT}]Error: no sub commands found[/]")
            self.retobj.exit_code = 2
        elif self.args[0].lower() == "list":
            with open(path.join(docs_dir, "Index.md"), "r") as index:
                Console.print(markdown.Markdown(index.read()))
        elif self.args[0].lower() == "show":
            if not get_args(self.args, 1):
                Console.print(
                    f"[{colors.FALERT}]Error: no doc name requested to show")
                self.retobj.exit_code = 3
            else:
                index_list: list[str] = []
                with open(path.join(docs_dir, "Index.md"), "r") as index:
                    lines = index.readlines()
                    for idx, line in enumerate(lines):
                        if "(Directory)" in line:
                            lines.pop(idx)
                    contents = "\n".join(lines)
                    index_list = re.findall("\\[.*?\\]", contents)
                for idx, doc_name in enumerate(index_list):
                    index_list[idx] = doc_name.replace(
                        "[", "").replace("]", "")
                doc_name_arg = get_args(self.args, 1)
                if doc_name_arg not in index_list:
                    Console.print(
                        f"[{colors.FALERT}]Error: Invalid doc_name found")
                    fuzz_list = process.extractBests(doc_name_arg, index_list)
                    if fuzz_list[0][1] > 80:
                        Console.print(
                            f"[{colors.FPROMPT}]Perhaps you meant:[/]")
                        maxlen = max([len(x[0]) for x in fuzz_list])
                        for text, percentage in fuzz_list[:5]:
                            Console.print(
                                f"* [{colors.BSUCCESS}]{text:{maxlen}}[/] {percentage}%"
                            )
                    self.retobj.exit_code = 1
                else:
                    path_splitter = "\\" if "Windows" in platform.platform() else "/"
                    doc_file = path.join(
                        docs_dir, doc_name_arg.replace(
                            ".", path_splitter) + ".md"
                    )
                    if path.exists(doc_file):
                        with open(doc_file) as file:
                            Console.print(markdown.Markdown(file.read()))
                        self.retobj.exit_code = 0
                    else:
                        Console.print(
                            f"[{colors.FALERT}]Error: Documentation file does not exist"
                        )
                        self.retobj.exit_code = 1
        else:
            Console.print(f"[{colors.FALERT}]Error: Invalid sub command")
            self.retobj.exit_code = 1
        return self.retobj

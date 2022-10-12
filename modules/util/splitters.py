from multipledispatch.dispatcher import str_signature
from rich import traceback

traceback.install()


class SplitterError(Exception):
    def __init__(self, **kwargs):
        self.kind = kd if (kd := kwargs.get("kind")) is not None else "General"
        self.msg = msg if (msg := kwargs.get("msg")) is not None else "Unknown"
        super().__init__(f"{self.kind}: {self.msg}")


class UnclosedBraceError(SplitterError):
    def __init__(self, brace: str):
        super().__init__(kind="UnclosedBrace",
                         msg=f"unclosed brace found {brace}")


class UnopenedBrace(SplitterError):
    def __init__(self, brace: str):
        super().__init__(kind="UnopenedBrace",
                         msg=f"{brace} was never opened")


class InvalidDelimiter(SplitterError):
    def __init__(self, char: str):
        super().__init__(kind="InvalidDelimiter",
                         msg=f"Delimiter is invalid: {char}")


def __single_delm_splitter(string: str, delm: str = ' ') -> list[str]:
    brace_map = {
        '(': ')',
        '{': '}',
        '[': ']',
    }
    if delm.isalnum() or brace_map.get(delm) or not delm:
        raise InvalidDelimiter(delm)

    split_stack: list[str] = []
    brace: list[str] = []
    squote, dquote = False, False

    def checked_push(cond1, cond2, item1: str, item2) -> None:
        if cond1:
            split_stack.append(item1)
        elif cond2:
            split_stack[-1] += item2

    for _, ch in enumerate(string):
        squote = (not squote and (not (dquote or brace) and ch == "'")) or (
            squote and ch != "'")
        dquote = (not dquote and (not (squote or brace) and ch == '"')) or (
            dquote and ch != '"')

        if squote or dquote:
            checked_push(ch in ('"', "'"), True, "", ch)

        elif ch in (')', ']', '}'):
            if not brace:
                raise SplitterError()

            cbrace = brace.pop()
            if brace:
                split_stack[-1] += ch
            pass

        elif (cbrace := brace_map.get(ch)) is not None:
            checked_push(not brace, True, "", ch)
            brace.append(cbrace)

        elif brace:
            split_stack[-1] += ch

        elif ch.isalnum() or (ch == '_' and delm != '_'):
            checked_push(not split_stack, True, ch, ch)
        else:
            checked_push((ch == delm) or (ch in ('"', "'")), True, "", ch)

        # print(ch, squote, brace, dquote)

    if brace:
        cbrace = brace[-1]
        raise UnclosedBraceError(
            "(" if cbrace == ")" else "[" if cbrace == "]" else "{")

    return split_stack


def __double_delm_splitter(string: str, inner_delm: str, outer_delm: str) -> list[list[str]]:
    brace_map = {
        '(': ')',
        '{': '}',
        '[': ']',
    }

    if inner_delm.isalnum() or brace_map.get(inner_delm) or not inner_delm:
        raise InvalidDelimiter(inner_delm)

    if outer_delm.isalnum() or brace_map.get(outer_delm) or not outer_delm:
        raise InvalidDelimiter(outer_delm)

    super_stack: list[list[str]] = [[]]
    split_stack: list[str] = super_stack[-1]
    brace: list[str] = []
    squote, dquote = False, False

    def checked_push(cond1, cond2, item1: str, item2) -> None:
        if cond1:
            split_stack.append(item1)
        elif cond2:
            split_stack[-1] += item2

    for _, ch in enumerate(string):
        squote = (not squote and (not (dquote or brace) and ch == "'")) or (
            squote and ch != "'")
        dquote = (not dquote and (not (squote or brace) and ch == '"')) or (
            dquote and ch != '"')

        if squote or dquote:
            checked_push(ch in ('"', "'"), True, "", ch)

        elif ch in (')', ']', '}'):
            if not brace:
                raise SplitterError()

            cbrace = brace.pop()
            if brace:
                split_stack[-1] += ch
            pass

        elif (cbrace := brace_map.get(ch)) is not None:
            checked_push(not brace, True, "", ch)
            brace.append(cbrace)

        elif brace:
            split_stack[-1] += ch

        elif ch.isalnum() or (ch == '_' and inner_delm != '_'):
            checked_push(not split_stack, True, ch, ch)

        elif ch == outer_delm:
            super_stack.append([])
            split_stack = super_stack[-1]

        else:
            checked_push((ch == inner_delm) or (
                ch in ('"', "'")), True, "", ch)

        # print(ch, squote, brace, dquote)

    if brace:
        cbrace = brace[-1]
        raise UnclosedBraceError(
            "(" if cbrace == ")" else "[" if cbrace == "]" else "{")

    return super_stack


def splitter(string: str, inner_delm: str = ' ', outer_delm: str = ' ') -> list[list[str]]:
    if outer_delm == inner_delm:
        return [__single_delm_splitter(string, inner_delm)]
    else:
        return __double_delm_splitter(string, inner_delm, outer_delm)

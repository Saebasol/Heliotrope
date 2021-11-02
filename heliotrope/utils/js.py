from asyncio import to_thread
from hashlib import md5
from typing import Any, Coroutine, Union, cast

from js2py.evaljs import EvalJs  # type: ignore
from js2py.translators import parse  # type: ignore
from js2py.translators.translating_nodes import trans  # type: ignore
from js2py.translators.translator import DEFAULT_HEADER  # type: ignore


def make_js_program(body: list[Any]) -> dict[str, Any]:
    return {"type": "Program", "body": body}


def get_parsed_functions_from_source(
    js_source: str, function_names: list[str]
) -> list[Any]:
    functions: list[dict[str, Any]] = []
    parsed_source: Any = parse(js_source)
    for source in parsed_source["body"]:
        if source["type"] == "FunctionDeclaration":
            if source["id"]["name"] in function_names:
                functions.append(source)
    return functions


def translate_tree(tree: dict[str, Any], HEADER: str = DEFAULT_HEADER) -> str:
    return HEADER + cast(str, trans(tree))


class ExtendEvalJS(EvalJs):  # type: ignore
    def exec_pycode(self, code: str) -> None:
        try:
            cache = self.__dict__["cache"]
        except KeyError:
            cache = self.__dict__["cache"] = {}
        hashkey = md5(code.encode("utf-8")).digest()
        try:
            compiled: Union[Any, Any] = cache[hashkey]
        except KeyError:
            compiled = cache[hashkey] = compile(code, "<EvalJS snippet>", "exec")
        exec(compiled, self._context)

    def get_function_to_thread(
        self, function_name: str, **kwargs: Any
    ) -> Coroutine[Any, Any, Any]:
        return to_thread(getattr(self, function_name), **kwargs)

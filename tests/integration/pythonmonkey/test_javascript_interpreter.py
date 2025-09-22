import pytest
from pythonmonkey import eval  # pyright: ignore[reportMissingTypeStubs]

from heliotrope.domain.entities.file import File
from heliotrope.infrastructure.hitomila import HitomiLa
from heliotrope.infrastructure.pythonmonkey import JavaScriptInterpreter
from tests.integration.hitomila.conftest import hitomi_la as hitomi_la


@pytest.mark.asyncio
async def test_javascript_interpreter_init(hitomi_la: HitomiLa):
    interpreter = JavaScriptInterpreter(hitomi_la)

    assert interpreter.hitomi_la == hitomi_la
    assert interpreter.gg_code == ""


@pytest.mark.asyncio
async def test_setup_integration(hitomi_la: HitomiLa):
    interpreter = await JavaScriptInterpreter.setup(hitomi_la)

    assert isinstance(interpreter, JavaScriptInterpreter)
    assert interpreter.hitomi_la == hitomi_la
    assert len(interpreter.gg_code) > 0


@pytest.mark.asyncio
async def test_get_common_js(javascript_interpreter: JavaScriptInterpreter):
    result = await javascript_interpreter.get_common_js()
    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_get_gg_js(javascript_interpreter: JavaScriptInterpreter):
    result = await javascript_interpreter.get_gg_js()

    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_parse_common_js(javascript_interpreter: JavaScriptInterpreter):
    js = """
function subdomain_from_url(url) {
    if (url) {
        if (url){
            return "subdomain";
        }
        if (url) {
            return "subdomain";
        }
    }
    return "subdomain";
}
function url_from_url(url) {
    return "url";
}
function full_path_from_hash(hash) {
    return "full_path";
}
function real_full_path_from_hash(hash) {
    return "real_full_path";
}
function url_from_hash(hash) {
    return "url_from_hash";
}
function url_from_url_from_hash(galleryid, image, dir, ext, base) {
    return "url_from_url_from_hash";
}
function rewrite_tn_paths(tn_paths) {
    return "rewrite_tn_paths";
}
    """
    parsed_functions = javascript_interpreter.parse_common_js(js)

    assert "function subdomain_from_url" in parsed_functions
    assert "function url_from_url" in parsed_functions
    assert "function full_path_from_hash" in parsed_functions
    assert "function real_full_path_from_hash" in parsed_functions
    assert "function url_from_hash" in parsed_functions
    assert "function url_from_url_from_hash" in parsed_functions
    assert "function rewrite_tn_paths" in parsed_functions


@pytest.mark.asyncio
async def test_refresh_gg_js(javascript_interpreter: JavaScriptInterpreter):
    javascript_interpreter.gg_code = ""
    await javascript_interpreter.refresh_gg_js()

    assert javascript_interpreter.gg_code != ""
    assert len(javascript_interpreter.gg_code) > 0


@pytest.mark.asyncio
async def test_evaluate_common_js(javascript_interpreter: JavaScriptInterpreter):
    await javascript_interpreter.evaluate_common_js()

    target_functions = [
        "subdomain_from_url",
        "url_from_url",
        "full_path_from_hash",
        "real_full_path_from_hash",
        "url_from_hash",
        "url_from_url_from_hash",
        "rewrite_tn_paths",
    ]

    for func in target_functions:
        eval(
            f"if (typeof {func} !== 'function') {{ throw new Error('{func} not defined'); }}"
        )


@pytest.mark.asyncio
async def test_image_url_from_image_avif(
    javascript_interpreter: JavaScriptInterpreter,
    hitomi_la: HitomiLa,
):

    test_file = File.from_dict(
        {
            "hasavif": True,
            "hash": "4c519d488b39e33aa503ac650084eb03c4b61e64778c488cdec0462f378f83d3",
            "height": 1821,
            "name": "01.jpg",
            "width": 1290,
            "hasjxl": False,
            "haswebp": True,
            "single": False,
        }
    )

    result = javascript_interpreter.image_url_from_image(2033723, test_file, True)
    response = await hitomi_la.session.request("GET", result, headers=hitomi_la.headers)
    assert result.endswith(".avif")
    assert isinstance(result, str)
    assert response.status == 200


@pytest.mark.asyncio
async def test_image_url_from_image_webp(
    javascript_interpreter: JavaScriptInterpreter,
    hitomi_la: HitomiLa,
):

    test_file = File.from_dict(
        {
            "hasavif": True,
            "hash": "4c519d488b39e33aa503ac650084eb03c4b61e64778c488cdec0462f378f83d3",
            "height": 1821,
            "name": "01.jpg",
            "width": 1290,
            "hasjxl": False,
            "haswebp": True,
            "single": False,
        }
    )

    result = javascript_interpreter.image_url_from_image(2033723, test_file, False)
    response = await hitomi_la.session.request("GET", result, headers=hitomi_la.headers)
    assert result.endswith(".webp")
    assert isinstance(result, str)
    assert response.status == 200

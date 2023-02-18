from unittest import mock

from esmerald_timing.integrations import EsmeraldScopeToName
from timing_asgi.utils import PathToName

from esmerald import APIView, Gateway, Request, route
from esmerald.applications import Esmerald
from esmerald.responses import JSONResponse


def test_esmerald_scope_metric_route_found(scope):
    @route("/something", methods=["GET"])
    def something() -> JSONResponse:
        return JSONResponse({})

    @route("/something_else", methods=["GET"])
    def something_else() -> JSONResponse:
        return JSONResponse({})

    esmerald_app = Esmerald(routes=[Gateway(handler=something), Gateway(handler=something_else)])

    metric_namer = EsmeraldScopeToName("myapp", esmerald_app, fallback=mock.MagicMock())
    assert metric_namer(scope(path="/something")) == "myapp.test_esmerald_scope_to_name.something"
    assert (
        metric_namer(scope(path="/something_else"))
        == "myapp.test_esmerald_scope_to_name.something_else"
    )
    assert not metric_namer.fallback.called


def test_esmerald_scope_metric_class_based_endpoint(scope):
    class HowClassy(APIView):
        path = "/"

        @route("/howclassy", methods=["GET"])
        def classy(self, request: Request) -> JSONResponse:
            return JSONResponse({})

    esmerald_app = Esmerald(routes=[Gateway(handler=HowClassy)])

    metric_namer = EsmeraldScopeToName("myapp", esmerald_app, fallback=mock.MagicMock())
    assert metric_namer(scope(path="/howclassy")) == "myapp.test_esmerald_scope_to_name.howclassy"


def test_esmerald_scope_metric_uses_name_if_found(scope):
    @route("/fancy", methods=["GET"])
    def fancy(request: Request) -> JSONResponse:
        return JSONResponse({})

    esmerald_app = Esmerald(
        routes=[
            Gateway(
                handler=fancy,
                name="this.is.fancy",
            )
        ]
    )

    metric_namer = EsmeraldScopeToName("myapp", esmerald_app, fallback=mock.MagicMock())
    assert metric_namer(scope(path="/fancy")) == "myapp.test_esmerald_scope_to_name.this.is.fancy"


def test_esmerald_scope_metric_route_not_found(esmerald_app, scope):
    metric_namer = EsmeraldScopeToName("myapp", esmerald_app, fallback=mock.MagicMock())
    assert metric_namer(scope(path="/something")) == metric_namer.fallback.return_value


def test_esmerald_scope_metric_fallback_is_path_to_name(esmerald_app, scope):
    metric_namer = EsmeraldScopeToName("myapp", esmerald_app)
    assert isinstance(metric_namer.fallback, PathToName)

from typing import TYPE_CHECKING, Any, Callable, Optional, Union

from starlette.routing import Match
from timing_asgi.interfaces import MetricNamer
from timing_asgi.utils import PathToName

if TYPE_CHECKING:
    from starlette.types import Scope

    from esmerald.applications import Esmerald


class EsmeraldScopeToName(MetricNamer):
    """Class which extracts a suitable metric name from a matching Starlette route.

    Uses the route name if it has one, but otherwise constructs a name based on the
    full module + method/class path.

    Falls back to either a provided fallback callable, or uses PathToName, which is the
    TimingMiddleware default.

    This integration was based on the one for starlette.
    https://github.com/steinnes/timing-asgi/blob/master/timing_asgi/integrations/starlette.py
    """

    def __init__(
        self,
        prefix: str,
        esmerald_app: "Esmerald",
        fallback: Union[Optional[Callable[..., Any]], Any] = None,
    ) -> None:
        self.prefix = prefix
        self.app = esmerald_app

        if fallback is None:
            fallback = PathToName(self.prefix)

        self.fallback = fallback

    def __call__(self, scope: "Scope") -> Any:
        route = None

        for _route in self.app.router.routes:
            if _route.matches(scope)[0] == Match.FULL:
                route = _route
                break

        if route is not None:
            return f"{self.prefix}.{route.handler.fn.__module__}.{route.name}"
        else:
            return self.fallback(scope)

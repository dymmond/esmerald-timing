import uvicorn
from esmerald_datadog.integrations import EsmeraldScopeToName
from timing_asgi import TimingClient, TimingMiddleware

from esmerald import Gateway, Request, get
from esmerald.applications import Esmerald
from esmerald.responses import PlainTextResponse


class PrintTimings(TimingClient):
    def timing(self, metric_name, timing, tags):
        print(metric_name, timing, tags)


@get("/")
def homepage(request: Request) -> PlainTextResponse:
    return PlainTextResponse("Welcome to Esmerald!")


app = Esmerald(routes=[Gateway(handler=homepage)])

app.add_middleware(
    TimingMiddleware,
    client=PrintTimings(),
    metric_namer=EsmeraldScopeToName(prefix="myapp", esmerald_app=app),
)

if __name__ == "__main__":
    uvicorn.run(app)

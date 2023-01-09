# Esmerald Timing

<p align="center">
  <a href="https://esmerald.dymmond.com"><img src="https://res.cloudinary.com/dymmond/image/upload/v1671718628/esmerald/img/logo-gr_oyr4my.png" alt='Esmerald'></a>
</p>

<p align="center">
    <em>🚀 ASGI integration with TimingASGIMiddleware for Esmerald . 🚀</em>
</p>

<p align="center">
<a href="https://github.com/dymmond/esmerald-timing/workflows/Test%20Suite/badge.svg?event=push&branch=main" target="_blank">
    <img src="https://github.com/dymmond/esmerald-timing/workflows/Test%20Suite/badge.svg?event=push&branch=main" alt="Test Suite">
</a>

<a href="https://pypi.org/project/esmerald-timing" target="_blank">
    <img src="https://img.shields.io/pypi/v/esmerald?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

<a href="https://pypi.org/project/esmerald-timing" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/esmerald-timing.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**Esmerald Documentation**: [https://esmerald.dymmond.com](https://esmerald.dymmond.com) 📚

**Esmerald Source Code**: [https://github.com/dymmond/esmerald](https://github.com/dymmond/esmerald)

---

## Motivation

This is an Esmerald integration to use the [TimingMiddleware](https://github.com/steinnes/timing-asgi).

[TimingMiddleware](https://github.com/steinnes/timing-asgi) for ASGI is useful for automatic
instrumentation of ASGI endpoints.

This package is an extension allowing the integration with Esmerald.

## Requirements

* Python 3.7 +
* [Esmerald](https://esmerald.dymmond.com)

## Usage

```python
import uvicorn
from esmerald_timing.integrations import EsmeraldScopeToName
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
```

Running this example and sending some requests:

```shell
$ python app.py
INFO:     Started server process [18769]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     127.0.0.1:58132 - "GET / HTTP/1.1" 200 OK
myapp.__main__.homepage 0.0009038448333740234 ['http_status:200', 'http_method:GET', 'time:wall']
myapp.__main__.homepage 0.0008970000000000367 ['http_status:200', 'http_method:GET', 'time:cpu']
myapp.favicon.ico 0.0006134510040283203 ['http_status:404', 'http_method:GET', 'time:wall']
myapp.favicon.ico 0.0006120000000000569 ['http_status:404', 'http_method:GET', 'time:cpu']
INFO:     127.0.0.1:58132 - "GET / HTTP/1.1" 200 OK
myapp.__main__.homepage 0.000881195068359375 ['http_status:200', 'http_method:GET', 'time:wall']
myapp.__main__.homepage 0.0008829999999999671 ['http_status:200', 'http_method:GET', 'time:cpu']
INFO:     127.0.0.1:58132 - "GET / HTTP/1.1" 200 OK
myapp.__main__.homepage 0.0014600753784179688 ['http_status:200', 'http_method:GET', 'time:wall']
myapp.__main__.homepage 0.0014729999999998356 ['http_status:200', 'http_method:GET', 'time:cpu']
```

from contextlib import AsyncExitStack, asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.dependencies.utils import get_dependant, solve_dependencies


# TODO
# review https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/
def solve_lifespan(lifespan):
    @asynccontextmanager
    async def _solve_lifespan(app: FastAPI):
        # A fake request for solve_dependencies
        request = Request(
            scope={
                "type": "http",
                "http_version": "1.1",
                "method": "GET",
                "scheme": "http",
                "path": "/",
                "raw_path": b"/",
                "query_string": b"",
                "root_path": "",
                "headers": ((b"X-Request-Scope", b"lifespan"),),
                "client": ("localhost", 8000),
                "server": ("localhost", 8000),
                "state": app.state,
            }
        )
        dependant = get_dependant(path="/", call=lifespan)

        async with AsyncExitStack() as async_exit_stack:
            solved_deps = await solve_dependencies(
                request=request,
                dependant=dependant,
                async_exit_stack=async_exit_stack,
                embed_body_fields=False,
            )

            ctxmgr = asynccontextmanager(lifespan)
            async with ctxmgr(**solved_deps.values) as value:
                yield value

    return _solve_lifespan

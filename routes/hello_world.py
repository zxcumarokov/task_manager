from fastapi import APIRouter


class HelloWorldRouter:
    def __init__(self):
        self.router = APIRouter()
        self.router.add_api_route(
            path="/",
            endpoint=self.read_root,
            methods=["GET"],
        )

    async def read_root(self):
        return {"Hello": "World"}

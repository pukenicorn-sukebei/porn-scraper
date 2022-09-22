from fastapi.openapi.utils import get_openapi
from app.main import app
import json


def generate():
    with open('openapi/openapi.json', 'w') as f:
        openapi_json = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes
        )
        json.dump(openapi_json, f)


if __name__ == "__main__":
    generate()

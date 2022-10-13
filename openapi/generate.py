from fastapi.openapi.utils import get_openapi
from app import app
import yaml


def generate():
    with open('openapi/openapi.yml', 'w') as f:
        openapi_spec = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            routes=app.routes
        )
        yaml.dump(openapi_spec, f)


if __name__ == "__main__":
    generate()

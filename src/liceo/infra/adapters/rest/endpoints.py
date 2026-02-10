from fastapi import APIRouter
from opentelemetry import metrics, trace


class RestGroupSpec:
    def __init__(self, path: str, name: str, description: str):
        self.path = path
        self.name = name
        self.description = description

    def metadata(self):
        return {"name": self.name, "description": self.description}

    def create_router(self):
        return APIRouter(prefix=self.path, tags=[self.name])

    def _get_metrics_root_name(self):
        return self.name.lower()

    def tracer(self):
        root_name = self._get_metrics_root_name()
        return trace.get_tracer(
            instrumenting_module_name="{}.tracer".format(root_name),
            attributes={"service_name": root_name},
        )

    def metrics(self):
        root_name = self._get_metrics_root_name()
        return metrics.get_meter(
            name="{}.metrics".format(root_name),
            attributes={"service_name": root_name},
        )


def open_api_permissions(permissions: list[str]) -> dict:
    return {"x-permissions-required": permissions}

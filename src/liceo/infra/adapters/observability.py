from dataclasses import dataclass

from opentelemetry import metrics, trace


@dataclass
class Observability:
    name: str

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

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from liceo.infra.domain.vo import OptiakConfiguration


def init_tracing(cfg: OptiakConfiguration):
    resource = Resource.create(
        attributes={SERVICE_NAME: cfg.observability.service_name}
    )
    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint=cfg.observability.traces_url)
    )
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(processor)

    reader = PeriodicExportingMetricReader(
        exporter=OTLPMetricExporter(endpoint=cfg.observability.metrics_url),
        export_interval_millis=10000,
        export_timeout_millis=10000,
    )
    meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
    trace.set_tracer_provider(tracer_provider)
    metrics.set_meter_provider(meterProvider)

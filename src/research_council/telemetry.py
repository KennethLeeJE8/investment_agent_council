"""OpenTelemetry spans exported only to the current run's local JSONL file."""

import json
from pathlib import Path

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, SpanExporter, SpanExportResult


class JsonlExporter(SpanExporter):
    def __init__(self, path: Path):
        self.path = path

    def export(self, spans):
        with self.path.open("a", encoding="utf-8") as stream:
            for span in spans:
                stream.write(
                    json.dumps(
                        {
                            "name": span.name,
                            "trace_id": format(span.context.trace_id, "032x"),
                            "span_id": format(span.context.span_id, "016x"),
                            "start_time": span.start_time,
                            "end_time": span.end_time,
                            "attributes": dict(span.attributes or {}),
                        }
                    )
                    + "\n"
                )
        return SpanExportResult.SUCCESS

    def shutdown(self):
        pass


def local_tracer(path: Path):
    provider = TracerProvider(
        resource=Resource({"service.name": "research-council"}), shutdown_on_exit=False
    )
    provider.add_span_processor(SimpleSpanProcessor(JsonlExporter(path)))
    return provider, provider.get_tracer("research_council")

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter 
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

import os

SERVICE_NAME = "fastapi-service"
OTLP_EXPORTER_ENDPOINT = os.getenv("OTLP_EXPORTER_ENDPOINT", "")


def initialize_tracer():
    resource = Resource.create({"service.name": SERVICE_NAME})
    trace_provider = TracerProvider(resource=resource)

    otlp_exporter = OTLPSpanExporter(endpoint=OTLP_EXPORTER_ENDPOINT, insecure=True)
    span_processor = BatchSpanProcessor(otlp_exporter)
    trace_provider.add_span_processor(span_processor)

    console_processor = BatchSpanProcessor(ConsoleSpanExporter())
    trace_provider.add_span_processor(console_processor)
    trace.set_tracer_provider(trace_provider)

def instrument_all(app,engine):
    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument(
        engine=engine,
        enable_commenter=True,
        commenter_options={"traceparent": "true"}
    )

def get_tracer(name: str = __name__):
    return trace.get_tracer(name)
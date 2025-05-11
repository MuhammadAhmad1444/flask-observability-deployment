from flask import Flask, request
from opentelemetry import metrics, trace
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import time

app = Flask(__name__)

# OpenTelemetry Setup
resource = Resource(attributes={"service.name": "flask-app"})
metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[PrometheusMetricReader()]))
meter = metrics.get_meter("flask-app")
tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)))
trace.set_tracer_provider(tracer_provider)
FlaskInstrumentor().instrument_app(app)

# Custom Metric
request_counter = meter.create_counter("http_requests_total", description="Total HTTP Requests")
request_duration = meter.create_histogram("http_request_duration_seconds", description="Request processing time")

@app.route('/')
def home():
    with trace.get_tracer(__name__).start_as_current_span("home"):
        start_time = time.time()
        request_counter.add(1, {"method": request.method, "endpoint": "/"})
        time.sleep(0.1)  # Simulate work
        duration = time.time() - start_time
        request_duration.record(duration, {"method": request.method, "endpoint": "/"})
        return "Welcome to the Flask App!"

@app.route('/error')
def error():
    with trace.get_tracer(__name__).start_as_current_span("error"):
        request_counter.add(1, {"method": request.method, "endpoint": "/error"})
        return "Internal Server Error", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
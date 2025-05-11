Observability Setup
This document outlines the steps to set up observability for the Flask web application using OpenTelemetry, Prometheus, and Grafana.
Prerequisites

Docker and Docker Compose installed
Python 3.9+

Setup Instructions

Install Dependencies

Install Python dependencies listed in requirements.txt:pip install -r requirements.txt




Run Services with Docker Compose

Start the Flask app, Prometheus, Grafana, and Jaeger:docker-compose up --build




Access Services

Flask App: http://localhost:5000
Prometheus: http://localhost:9090
Grafana: http://localhost:3000 (default login: admin/admin)
Jaeger: http://localhost:16686


Configure Grafana

Add Prometheus as a data source in Grafana (URL: http://prometheus:9090).
Import or create a dashboard with the following metrics:
HTTP Request Rate: rate(http_requests_total[5m])
Error Rate: rate(http_requests_total{status=~"5.."}[5m])
Latency (p95/p99): histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
Custom Metric: sum(rate(http_request_duration_seconds_sum[5m]))





Metrics Collected

HTTP Request Rate: Total requests per second, segmented by method and endpoint.
Error Rate: Rate of 4xx/5xx responses.
Latency: 95th and 99th percentile of request durations.
Custom Metric: Total request processing time (http_request_duration_seconds).

Configuration Files

app.py: Flask app with OpenTelemetry instrumentation.
prometheus.yml: Prometheus configuration to scrape metrics from the Flask app.
docker-compose.yml: Defines services for the app, Prometheus, Grafana, and Jaeger.

Screenshots
(Note: Screenshots of Grafana dashboards should be added here after setup. Run the app, configure Grafana, and capture dashboards showing the metrics above.)
Testing Observability

Access http://localhost:5000 and http://localhost:5000/error to generate metrics.
View traces in Jaeger at http://localhost:16686.
Query metrics in Prometheus and visualize in Grafana.


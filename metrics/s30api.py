from lennoxs30api.metrics import Metrics
from lennoxs30api.s30api_async import lennox_system, lennox_zone
from prometheus_client import Gauge

from .helper import extract_timestamp


class metrics:
    def __init__(self):
        namespace = "s30api"
        self.error_count = Gauge(
            name="errors_total",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.message_count = Gauge(
            name="messages_total",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.receive_count = Gauge(
            name="receive_total",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.send_count = Gauge(
            name="send_total",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.http_2xx_count = Gauge(
            name="http_2xx_total",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.http_4xx_count = Gauge(
            name="http_4xx_total",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.http_5xx_count = Gauge(
            name="http_5xx_total",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.timeouts = Gauge(
            name="timeouts_total",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.server_disconnects = Gauge(
            name="server_disconnects_total",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.client_response_errors = Gauge(
            name="client_response_errors_total",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.connection_errors = Gauge(
            name="connection_errors_total",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.last_receive_time = Gauge(
            name="last_receive_timestamp_seconds",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.last_send_time = Gauge(
            name="last_send_timestamp_seconds",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.last_error_time = Gauge(
            name="last_error_timestamp_seconds",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.last_reconnect_time = Gauge(
            name="last_reconnect_timestamp_seconds",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.last_message_time = Gauge(
            name="last_message_timestamp_seconds",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.last_metric_time = Gauge(
            name="last_metric_timestamp_seconds",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.sibling_message_drop = Gauge(
            name="sibling_message_drop_total",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.sender_message_drop = Gauge(
            name="sender_message_drop_total",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.bytes_in = Gauge(
            name="bytes_in",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.bytes_out = Gauge(
            name="bytes_out",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )

    def update_metrics(
        self, metrics: Metrics, zone: lennox_zone, system: lennox_system
    ):
        self.error_count.labels(system=system.name, zone=zone.name).set(
            metrics.error_count
        )
        self.message_count.labels(system=system.name, zone=zone.name).set(
            metrics.message_count
        )
        self.receive_count.labels(system=system.name, zone=zone.name).set(
            metrics.receive_count
        )
        self.send_count.labels(system=system.name, zone=zone.name).set(
            metrics.send_count
        )
        self.http_2xx_count.labels(system=system.name, zone=zone.name).set(
            metrics.http_2xx_cnt
        )
        self.http_4xx_count.labels(system=system.name, zone=zone.name).set(
            metrics.http_4xx_cnt
        )
        self.http_5xx_count.labels(system=system.name, zone=zone.name).set(
            metrics.http_5xx_cnt
        )
        self.timeouts.labels(system=system.name, zone=zone.name).set(metrics.timeouts)
        self.server_disconnects.labels(system=system.name, zone=zone.name).set(
            metrics.server_disconnects
        )
        self.client_response_errors.labels(system=system.name, zone=zone.name).set(
            metrics.client_response_errors
        )
        self.connection_errors.labels(system=system.name, zone=zone.name).set(
            metrics.connection_errors
        )
        self.last_receive_time.labels(system=system.name, zone=zone.name).set(
            extract_timestamp(metrics.last_receive_time)
        )
        self.last_send_time.labels(system=system.name, zone=zone.name).set(
            extract_timestamp(metrics.last_send_time)
        )
        self.last_error_time.labels(system=system.name, zone=zone.name).set(
            extract_timestamp(metrics.last_error_time)
        )
        self.last_reconnect_time.labels(system=system.name, zone=zone.name).set(
            extract_timestamp(metrics.last_receive_time)
        )
        self.last_message_time.labels(system=system.name, zone=zone.name).set(
            extract_timestamp(metrics.last_message_time)
        )
        self.last_metric_time.labels(system=system.name, zone=zone.name).set(
            extract_timestamp(metrics.last_metric_time)
        )
        self.sibling_message_drop.labels(system=system.name, zone=zone.name).set(
            metrics.sibling_message_drop
        )
        self.sender_message_drop.labels(system=system.name, zone=zone.name).set(
            metrics.sender_message_drop
        )
        self.bytes_in.labels(system=system.name, zone=zone.name).set(metrics.bytes_in)
        self.bytes_out.labels(system=system.name, zone=zone.name).set(metrics.bytes_out)

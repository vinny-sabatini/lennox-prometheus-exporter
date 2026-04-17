import logging

from lennoxs30api.s30api_async import lennox_system, lennox_zone
from prometheus_client import Gauge

from .helper import set_value_or_zero

logger = logging.getLogger(__name__)


class metrics:
    def __init__(self):
        namespace = "lennox"
        self.current_temperature = Gauge(
            name="current_temperature",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.current_humidity = Gauge(
            name="current_humidity",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.cool_set_point = Gauge(
            name="cool_set_point",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.heat_set_point = Gauge(
            name="heat_set_point",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.target_temperature = Gauge(
            name="target_temperature",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        self.outdoor_temperature = Gauge(
            name="outdoor_temperature",
            documentation="testing",
            namespace=namespace,
            labelnames=["system", "zone"],
        )
        # hvac["mode"] = zone.getSystemMode()
        # hvac["op"] = zone.tempOperation
        # hvac["demand"] = float(zone.demand) #force it to a float as it will be when on
        # hvac["fan"] = zone.fan
        # hvac["aux"] = zone.aux

    def update_metrics(self, zone: lennox_zone, system: lennox_system):
        self.current_temperature.labels(system=system.name, zone=zone.name).set(
            set_value_or_zero(zone.getTemperature())
        )
        self.current_humidity.labels(system=system.name, zone=zone.name).set(
            set_value_or_zero(zone.getHumidity())
        )
        self.cool_set_point.labels(system=system.name, zone=zone.name).set(
            set_value_or_zero(zone.getCoolSP())
        )
        self.heat_set_point.labels(system=system.name, zone=zone.name).set(
            set_value_or_zero(zone.getHeatSP())
        )
        self.target_temperature.labels(system=system.name, zone=zone.name).set(
            set_value_or_zero(zone.getTargetTemperatureF())
        )
        self.outdoor_temperature.labels(system=system.name, zone=zone.name).set(
            set_value_or_zero(system.outdoorTemperature)
        )

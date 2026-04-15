#!/usr/bin/env python

# Modules

import logging
import os
import asyncio
import signal

from lennoxs30api.s30exception import S30Exception
from lennoxs30api import s30api_async
from prometheus_client import start_http_server, Gauge

CURRENT_TEMPERATURE = Gauge("current_temperature", "testing")
CURRENT_HUMIDITY = Gauge("current_humidity", "testing")
COOL_SET_POINT = Gauge("cool_set_point", "testing")
HEAT_SET_POINT = Gauge("heat_set_point", "testing")
TARGET_TEMPERATURE = Gauge("target_temperature", "testing")
OUTDOOR_TEMPERATURE = Gauge("outdoor_temperature", "testing")
S30API_ERROR_COUNT = Gauge("s30api_error_count", "testing")
S30API_MESSAGE_COUNT = Gauge("s30api_message_count", "testing")
S30API_RECEIVE_COUNT = Gauge("s30api_receive_count", "testing")
S30API_SEND_COUNT = Gauge("s30api_send_count", "testing")
S30API_HTTP_2XX_COUNT = Gauge("s30api_http_2xx_cnt", "testing")
S30API_HTTP_4XX_COUNT = Gauge("s30api_http_4xx_cnt", "testing")
S30API_HTTP_5XX_COUNT = Gauge("s30api_http_5xx_cnt", "testing")
S30API_TIMEOUTS = Gauge("s30api_timeouts", "testing")
S30API_SERVER_DISCONNECTS = Gauge("s30api_server_disconnects", "testing")
S30API_CLIENT_RESPONSE_ERRORS = Gauge("s30api_client_response_errors", "testing")
S30API_CONNECTION_ERRORS = Gauge("s30api_connection_errors", "testing")
S30API_LAST_RECEIVE_TIME = Gauge("s30api_last_receive_time", "testing")
S30API_LAST_SEND_TIME = Gauge("s30api_last_send_time", "testing")
S30API_LAST_ERROR_TIME = Gauge("s30api_last_error_time", "testing")
S30API_LAST_RECONNECT_TIME = Gauge("s30api_last_reconnect_time", "testing")
S30API_LAST_MESSAGE_TIME = Gauge("s30api_last_message_time", "testing")
S30API_LAST_METRIC_TIME = Gauge("s30api_last_metric_time", "testing")
S30API_SIBLING_MESSAGE_DROP = Gauge("s30api_sibling_message_drop", "testing")
S30API_SENDER_MESSAGE_DROP = Gauge("s30api_sender_message_drop", "testing")
S30API_BYTES_IN = Gauge("s30api_bytes_in", "testing")
S30API_BYTES_OUT = Gauge("s30api_bytes_out", "testing")


# Global Variables
running = True

logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
)
rootLogger = logging.getLogger()
rootLogger.setLevel(level=logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
consoleHandler.setLevel(logging.INFO)
rootLogger.addHandler(consoleHandler)
logger = logging.getLogger(__name__)

# Helper Functions


# This task gets messages from S30 and processes them
async def message_pump_task(s30api: s30api_async) -> None:
    global running

    try:
        # Login and establish connection
        await s30api.serverConnect()
        # For each S30 found, initiate the data subscriptions.
        for lsystem in s30api.system_list:
            await s30api.subscribe(lsystem)
    # Catch errors and exit this task.
    except S30Exception as e:
        logger.error("Failed to connect error " + str(e))
        return
    while running:
        # Checks for new messages and processes them which may update the state of zones, etc.
        try:
            await s30api.messagePump()
            await asyncio.sleep(1)
        # Intermittent errors due to Lennox servers, etc, may occur, log and keep pumping.
        except S30Exception as e:
            logger.error("Message pump error " + str(e))
    else:
        await s30api.shutdown()
        logger.info("shutdown")


# This task periodically polls the API for data and prints it.  These calls are just accessing local state, that
# may get updated by the message pump task.
async def api_poller_task(s30api: s30api_async):
    global running

    wait = 1  # the default wait until everything gets set up, then 1 minute
    while running:
        logger.debug("API Poller Task")
        try:
            for lsystem in s30api.system_list:
                for zone in lsystem.zone_list:
                    if zone.getTemperature() != None:
                        wait = 60  # wait 1 minute after everything is set up

                        # TODO: Don't report ready until we get here
                        # Otherwise these will all report 0
                        # TODO: Try to move metric logic to functions
                        # TODO: Cleaner way to set with default (maybe this is better with functions)
                        CURRENT_TEMPERATURE.set(
                            zone.getTemperature() if zone.getTemperature() else 0
                        )
                        CURRENT_HUMIDITY.set(
                            zone.getHumidity() if zone.getHumidity() else 0
                        )
                        COOL_SET_POINT.set(zone.getCoolSP() if zone.getCoolSP() else 0)
                        HEAT_SET_POINT.set(zone.getHeatSP() if zone.getHeatSP() else 0)
                        TARGET_TEMPERATURE.set(
                            zone.getTargetTemperatureF()
                            if zone.getTargetTemperatureF()
                            else 0
                        )
                        OUTDOOR_TEMPERATURE.set(
                            lsystem.outdoorTemperature
                            if lsystem.outdoorTemperature
                            else 0
                        )

                        # id = zone.unique_id
                        # hvac = {}
                        # hvac["dt"] = int(time.time())
                        # hvac["mode"] = zone.getSystemMode()
                        # hvac["op"] = zone.tempOperation
                        # hvac["demand"] = float(zone.demand) #force it to a float as it will be when on
                        # hvac["fan"] = zone.fan
                        # hvac["aux"] = zone.aux
                        # logger.debug(hvac)
                        S30API_ERROR_COUNT.set(s30api.metrics.error_count)
                        S30API_MESSAGE_COUNT.set(s30api.metrics.message_count)
                        S30API_RECEIVE_COUNT.set(s30api.metrics.receive_count)
                        S30API_SEND_COUNT.set(s30api.metrics.send_count)
                        S30API_HTTP_2XX_COUNT.set(s30api.metrics.http_2xx_cnt)
                        S30API_HTTP_4XX_COUNT.set(s30api.metrics.http_4xx_cnt)
                        S30API_HTTP_5XX_COUNT.set(s30api.metrics.http_5xx_cnt)
                        S30API_TIMEOUTS.set(s30api.metrics.timeouts)
                        S30API_SERVER_DISCONNECTS.set(s30api.metrics.server_disconnects)
                        S30API_CLIENT_RESPONSE_ERRORS.set(
                            s30api.metrics.client_response_errors
                        )
                        S30API_CONNECTION_ERRORS.set(s30api.metrics.connection_errors)
                        S30API_LAST_RECEIVE_TIME.set(
                            s30api.metrics.last_receive_time.timestamp()
                        )
                        S30API_LAST_SEND_TIME.set(
                            s30api.metrics.last_send_time.timestamp()
                        )
                        S30API_LAST_ERROR_TIME.set(
                            s30api.metrics.last_error_time.timestamp()
                        )
                        S30API_LAST_RECONNECT_TIME.set(
                            s30api.metrics.last_receive_time.timestamp()
                        )
                        S30API_LAST_MESSAGE_TIME.set(
                            s30api.metrics.last_message_time.timestamp()
                        )
                        S30API_LAST_METRIC_TIME.set(
                            s30api.metrics.last_metric_time.timestamp()
                        )
                        S30API_SIBLING_MESSAGE_DROP.set(
                            s30api.metrics.sibling_message_drop
                        )
                        S30API_SENDER_MESSAGE_DROP.set(
                            s30api.metrics.sender_message_drop
                        )
                        S30API_BYTES_IN.set(s30api.metrics.bytes_in)
                        S30API_BYTES_OUT.set(s30api.metrics.bytes_out)

        except Exception as e:
            logger.error("Exception " + str(e))
        await asyncio.sleep(wait)  # wait 1 minute and get the latest state


async def multiple_tasks(s30api):
    input_coroutines = [
        message_pump_task(s30api),
        api_poller_task(s30api),
    ]
    res = await asyncio.gather(*input_coroutines, return_exceptions=True)
    return res


def terminate(signal, frame):
    global running
    logger.info("SIGTERM received")
    running = False


def logout(signal, frame):
    global running
    logger.info("SIGINT received")
    running = False


def main():
    app_id = os.getenv("LENNOX_APP_ID", "")
    ip_address = os.getenv("LENNOX_IP_ADDRESS", "")

    # TODO: Setup readiness, liveness, and metrics endpoints
    start_http_server(8000)

    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGINT, logout)
    s30api = s30api_async("none", "none", app_id, ip_address)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(multiple_tasks(s30api))
    logger.info("Program Ended")


if __name__ == "__main__":
    main()

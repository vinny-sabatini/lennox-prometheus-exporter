#!/usr/bin/env python

import asyncio
import logging
import os
import signal
import sys

from lennoxs30api import s30api_async
from lennoxs30api.s30exception import S30Exception
from prometheus_client import start_http_server

from metrics import lennox, s30api

lennox_metrics = lennox.metrics()
s30api_metrics = s30api.metrics()

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
                        lennox_metrics.update_metrics(zone, lsystem)
                        s30api_metrics.update_metrics(s30api.metrics, zone, lsystem)

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
    ip_address = os.getenv("LENNOX_IP_ADDRESS", "")
    if not ip_address:
        logger.error("Must set LENNOX_IP_ADDRESS environment variable")
        sys.exit(1)

    app_id = os.getenv("LENNOX_APP_ID", "")
    if not app_id:
        logger.error("Must set LENNOX_APP_ID environment variable")
        sys.exit(1)

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

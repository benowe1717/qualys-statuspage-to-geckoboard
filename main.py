#!/usr/bin/env python3
import logging
import logging.config
import os
import socket
from datetime import datetime

from src.classes.file_checker import FileChecker
from src.classes.geckoboard import GeckboardApi
from src.classes.statuspage_api import StatusPageApi
from src.constants import constants


def get_hostname() -> str:
    hostname = socket.gethostname()
    if not hostname:
        return 'localhost'
    return hostname


def get_pid() -> int:
    pid = os.getpid()
    if pid > 0:
        return pid
    return -1


def get_logging_config(file: str) -> str:
    try:
        fc = FileChecker(file)
        if not fc.is_file():
            return ''

        if not fc.is_readable():
            return ''

        return fc.file
    except BaseException:
        print(f'Unable to locate {file} or {file} is invalid!')
        return ''


def main():
    logging_conf = './src/configs/logging.conf'
    filepath = get_logging_config(logging_conf)
    if not filepath:
        exit(1)

    logging.config.fileConfig(filepath)
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.event_date = datetime.now().strftime(constants.EVENT_DATE_FORMAT)
        record.hostname = get_hostname()
        record.program = constants.PROGRAM_NAME
        record.pid = get_pid()
        return record

    logging.setLogRecordFactory(record_factory)
    logger = logging.getLogger(constants.PROGRAM_NAME)

    logger.info('Starting script...')

    credentials_file = './data/credentials.yaml'
    statuspage = StatusPageApi(credentials_file)
    geckboard = GeckboardApi(credentials_file)

    logger.info('Getting unresolved incidents...')
    result = statuspage.get_unresolved_incidents()
    if not result:
        exit(1)

    if len(statuspage.incidents) > 0:
        logger.info(f'There are {len(statuspage.incidents)} to parse...')
        messages = []
        status = 'DOWN'

        logger.info('Getting all Platforms...')
        result = statuspage.get_component_groups()
        if not result:
            exit(1)

        for incident in statuspage.incidents:
            impact = incident['impact']
            if impact == 'maintenance':
                logger.info('This incident is a maintenace post, skipping...')
                continue

            product_name = ''
            platform_name = ''
            for component in incident['components']:
                product_name = component['name']
                platform_id = component['group_id']
                platform_name = ''
                for platform in statuspage.platforms:
                    if platform_id == platform[0]:
                        platform_name = platform[1]

            logger.info('Found an outage incident!')
            logger.info('Building message for Geckoboard...')
            msg = geckboard.build_msg(
                status,
                platform_name=platform_name,
                product_name=product_name)
            if not msg:
                continue

            messages.append(msg)

        if len(messages) > 0:
            logger.info('Formatting all outages into a single message...')
            msg = ''.join(messages)

            logger.info('Pushing message to Geckoboard widget...')
            result = geckboard.push_to_widget(msg)
            if not result:
                exit(1)

    else:
        logger.info('There are no active outages!')
        status = 'OK'

        logger.info('Building message for Geckoboard...')
        msg = geckboard.build_msg(status)
        if not msg:
            exit(1)

        logger.info('Pushing message to Geckoboard widget...')
        result = geckboard.push_to_widget(msg)  # type: ignore
        if not result:
            exit(1)

    logger.info('Script completed successfully!')


if __name__ == '__main__':
    main()

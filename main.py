#!/usr/bin/env python3
from src.classes.geckoboard import GeckboardApi
from src.classes.statuspage_api import StatusPageApi


def main():
    credentials_file = './data/credentials.yaml'
    statuspage = StatusPageApi(credentials_file)
    geckboard = GeckboardApi(credentials_file)
    result = statuspage.get_unresolved_incidents()
    if not result:
        exit(1)

    if len(statuspage.incidents) > 0:
        messages = []
        status = 'DOWN'
        result = statuspage.get_component_groups()
        if not result:
            exit(1)

        for incident in statuspage.incidents:
            impact = incident['impact']
            if impact == 'maintenance':
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

            msg = geckboard.build_msg(
                status,
                platform_name=platform_name,
                product_name=product_name)
            if not msg:
                continue

            messages.append(msg)

        if len(messages) > 0:
            msg = ''.join(messages)
            result = geckboard.push_to_widget(msg)
            if not result:
                exit(1)

    else:
        status = 'OK'
        msg = geckboard.build_msg(status)
        if not msg:
            exit(1)

        result = geckboard.push_to_widget(msg)  # type: ignore
        if not result:
            exit(1)


if __name__ == '__main__':
    main()

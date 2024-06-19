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

    print(statuspage.incidents)


if __name__ == '__main__':
    main()

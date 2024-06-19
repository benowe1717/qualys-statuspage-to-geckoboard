# Qualys Status Page Posts to Geckoboard

Qualys Status Page Posts to Geckboard is a `tool` that scrapes posts made to a public `StatusPage.io` website and pushes those to a custom `Geckboard` widget.

This makes it easy to include current outages or planned maintenance windows on the TVs mounted in the office that show other key performance indicators and important messages.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Install all requirements from `requirements.txt` in the Installing section
- Supported Operating Systems:
  - Debian 11/12
  - Ubuntu 20.04/22.04 LTS
  - Zorin OS 16+
- Supported Python3 versions:
  - Python 3.8.10+

## Installing

To install `Qualys Status Page Posts to Geckoboard`, follow these steps:

- Install all required libraries using the `requirements.txt` file and `pip3`:
`pip3 install -r requirements.txt`

- Supply the necessary credentials in ONE of TWO ways:
1. Fill in the supplied credentials.yaml template located at `./src/configs/credentials.yaml`
2. Create a credentials.yaml file anywhere you'd like
Fill in the yaml file as:
```
credentials:
  statuspage:
    apikey:
    host:
    pageid:
  geckoboard:
    apikey:
    host:
    widgetkey:
```

## Configuration

## Using

## Contributing to Qualys Status Page Posts to Geckoboard

To contribute to `Qualys Status Page Posts to Geckboard`, follow these steps:

1. Fork this repository
2. Create a branch: `git checkout -b <branch_name>`
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the Pull Request

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## Contributors

Thanks to the following people who have contributed to this project:

- [@benowe1717](https://github.com/benowe1717)

## Contact

For help or support on this repository, follow these steps:

- Fill out an issue [here](https://github.com/benowe1717/qualys-statuspage-to-geckoboard/issues)

## License

This project uses the following license: [GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

## Sources

- https://github.com/scottydocs/README-template.md/blob/master/README.md
- https://choosealicense.com/
- https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/

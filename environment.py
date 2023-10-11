import os


class Environment:
    DEV = 'dev'
    PROD = 'prod'

    URLS = {
        DEV: 'https://playground.learnqa.ru/api_dev',
        PROD: 'https://playground.learnqa.ru/api'
    }

    def __init__(self):
        try:
            self.env = os.environ['ENV']
        except KeyError:
            self.env = self.DEV

    def get_base_url(self):
        if self.env in self.URLS:
            return self.URLS[self.env]
        else:
            raise Exception(f"Unknown value of ENV variable {self.env}")


ENV_OBJECT = Environment()

"""
$env:ENV = "prod"
echo $env:ENV
python -m pytest tests/
"""
"""
docker --version
docker pull python 
docker build -t pytest_runner .
docker run --rm --mount type=bind,src=C:\\Users\\мвидео\\PycharmProjects\\Test-Automation-REST-API,target=/tests_project/ pytest_runner pytest
"""

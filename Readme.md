<a href="https://github.com/Badx86/LearnQA_Python_API/actions/workflows/API-tests.yml">
    <img alt="tests" src="https://github.com/Badx86/LearnQA_Python_API/actions/workflows/API-tests.yml/badge.svg">
</a>
<a href="https://github.com/Badx86/LearnQA_Python_API/actions/workflows/LearnQA-schedule.yml">
    <img alt="tests" src="https://github.com/Badx86/LearnQA_Python_API/actions/workflows/LearnQA-schedule.yml/badge.svg">
</a>
<a href="https://badx86.github.io/LearnQA_Python_API/">
    <img alt="Allure-report" src="https://img.shields.io/badge/Allure%20Report-deployed-green">
</a>
<a href="https://www.python.org/doc/versions/">
    <img alt="Python Version" src="https://img.shields.io/badge/python-3.11-blue">
</a>  
<a href="https://pypi.org/project/selenium">
    <img alt="dependency - selenium" src="https://img.shields.io/badge/dependency-selenium-blue?logo=selenium&logoColor=white">
</a>  
<a href="https://pypi.org/project/pytest">
    <img alt="dependency - pytest" src="https://img.shields.io/badge/dependency-pytest-blue?logo=pytest&logoColor=white">
</a>  

# Test Automation for REST API

Данный проект представляет собой набор автоматических тестов для REST API. Тесты реализованы на Python с использованием библиотеки `pytest` и интегрированы с системой отчетности `Allure`.

## Установка

Перед началом убедитесь, что у вас установлены следующие компоненты:

- Python
- Docker
- Allure

## Запуск тестов

### 1. Запуск тестов локально

$env:ENV = "prod"  
echo $env:ENV  
python -m pytest tests/

docker --version  
docker pull python  
docker build -t pytest_runner .  
docker run --rm --mount type=bind,src=C:\\Users\\LearnQA_Python_API,target=/tests_project/ pytest_runner pytest

Генерация отчетов с помощью Allure:

python -m pytest --alluredir=test_results/ tests/  
allure serve test_results/

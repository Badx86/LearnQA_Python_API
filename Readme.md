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

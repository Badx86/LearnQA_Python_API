
$env:ENV = "prod"
echo $env:ENV
python -m pytest tests/

docker --version
docker pull python 
docker build -t pytest_runner .
docker run --rm --mount type=bind,src=C:\\Users\\мвидео\\PycharmProjects\\Test-Automation-REST-API,target=/tests_project/ pytest_runner pytest

python -m pytest --alluredir=test_results/ tests/
allure serve test_results/

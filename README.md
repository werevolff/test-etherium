# test-etherium

## Установка зависимостей:

Проект использует для работы [pyPoetry](https://python-poetry.org/docs/) и [pyenv](https://github.com/pyenv/pyenv)

1. Установите [pyenv](https://github.com/pyenv/pyenv), после чего выполните:

```
pyenv install 3.8.2
pyenv global pypy-3.8.2
```

2. Установите [pyPoetry](https://python-poetry.org/docs/). Выполните:

```
poetry env use ~/.pyenv/shims/python
```

3. Скачайте репозиторий проекта и перейдите в его корень. Выполните:

```
poetry install
```

Если вы будете разворачивать проект на продакшене, выполните:

```
poetry install --no-dev
```

Линтеры и тесты будут не доступны для production.

В выводе команды будет присутствовать путь к созданной poetry виртуальной среде
python. Например,

```
/home/<YOUR_USER>/.cache/pypoetry/virtualenvs/test-etherium-oX205Vkg-py3.8/
```

4. Выполните:

```
source /home/<YOUR_USER>/.cache/pypoetry/virtualenvs/test-etherium-oX205Vkg-py3.8/bin/activate
```

где `/home/<YOUR_USER>/.cache/pypoetry/virtualenvs/test-etherium-oX205Vkg-py3.8/bin/activate` -
это путь, полученный в п. 3 инструкции.

5. Создайте на вашем сервере PostgreSQL базу данных для работы с проектом [Документация](https://postgrespro.ru/docs/postgresql/9.6/sql-createtable)

6. В корне проекта находится файл env.example. Скопируйте его в файл .env в той же директории.
   Откройте файл и измените переменные:
    1. DEFAULT_DATABASE - на корректную ссылку, обеспечивающую доступ к созданной вами базе.
    2. FERNET_KEY - вы можете сгененрировать свой ключ, пользуясь методом generate_key для [Fernet](https://cryptography.io/en/latest/fernet/)
    3. W3_PROVIDER_URL - поменяйте на URL для вашего провайдера Web3py (https://web3py.readthedocs.io/en/stable/providers.html)

7. Выполните:

```
python src/manage.py migrate
```

## Тесты и линтеры:

Вы можете выполнить тесты, запустив:

```
pytest src
```

Выполнить линтеры можно, выполнив команды

```
flake8 src
mypy src
```

## Запуск проекта:

Для локального запуска проекта используйте команду

```
python src/manage.py runserver
```

Сервер разработки будет запущен по адресу

`http//127.0.0.1:8000`

Документация к АПИ будет доступна по адресу:

`http//127.0.0.1:8000/api/schema/redoc/`

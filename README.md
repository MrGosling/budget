# Expense Tracker API

Проект создан для отслеживания расходов с их последующей аналитикой.


### Как установить

Python3 должен быть уже установлен.
MongoDB должна быть установлена и запущена, для этого необходимо ввести ряд команд:

* Чтобы установить актуальный пакет MongoDB, необходимо добавить его в список репозиториев. Но предварительно следует импортировать открытый ключ для MongoDB в вашу систему. Для этого используйте следующую команду:

```curl -fsSL https://pgp.mongodb.com/server-7.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg --dearmor```


* Теперь добавьте репозиторий MongoDB 7.0 в директорию /etc/apt/sources.list.d:```

```echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list```


* В результате вы создадите файл с именем mongodb-org-7.0.list. Для просмотра его содержимого можно использовать команду cat находясь в директории `/etc/apt/sources.list.d/:`

```cd /etc/apt/sources.list.d/```
```cat mongodb-org-7.0.list```


* Просмотр содержимого файла mongodb-org-7.0.list
Затем обновите локальный список пакетов, в результате чего репозиторий MongoDB 7.0 будет добавлен в систему:

```sudo apt update```


* Далее уже можно будет запустить установку непосредственно пакета MongoDB:

```sudo apt install mongodb-org```


* По окончании установки следующей командой можно проверить версию установленного пакета:

```mongod --version```


* Просмотр версии установленного пакета MongoDB
При установке служба MongoDB по умолчанию будет отключена. Её включение производится при помощи системной утилиты systemctl:

```sudo systemctl start mongod```


* Убедиться в том, что сервис работает, можно посмотрев его состояние:

```sudo systemctl status mongod```


### Зависимости

1. Установить необходимые библиотеки

```pip install -r requirements.txt```

2. Создайте базу данных, выполнив команду в терминале:

```python3 database.py```


### Запуск

1. Запустите приложение командой:

```python3 main.py```

2. Для просмотра эндпоинтов с помощью swagger:

* Перейдите по [ссылке](https://mrgosling.github.io/budget/)

3. Сервер будет доступен по адресу `http://localhost:8000/`


### Цель проекта

Код написан в образовательных целях студентами онлайн-бакалавриата ТюмГУ совместно с Нетологией.

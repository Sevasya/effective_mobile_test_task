# Backend-приложение с кастомной аутентификацией и разграничениями прав доступа

Этот проект реализует **собственную систему аутентификации и авторизации (RBAC)** без использования стандартных инструментов Django `auth`. 

## Стек технологий:
- Django
- DRF
- Docker
- PostgreSQL

### Клонируйте проект:
```bash
git clone https://github.com/Sevasya/effective_mobile_test_task.git
cd effective_mobile_test_task
```

В данной папке создайте файл .env (Я работаю в VS Code, в другом редакторе могут быть другие команды)

```bash
code .env 
```

В данный файл скопируйте данный код и замените значения логина, пароля и ключа на свои:

```bash
POSTGRES_USER=YOUR_USERNAME
POSTGRES_PASSWORD=YOUR_PASSWORD
SECRET_KEY=YOUR_SECRET_KEY
```

Создайте виртуальное окружение и активируйте его:
```bash
py -m virtualenv env
.\env\Scripts\activate
```

Установите зависимости:
```bash
pip install -r .\requirements.txt
```

Запустите образ PostgreSQL (убедитесь, что Docker на Вашем компьтере запущен):

```bash
docker-compose up -d
```

Далее применяем миграции:
```bash
cd .\effective_mobile\
py manage.py makemigrations objects
py manage.py makemigrations users 
py manage.py migrate
```

Создаем тестовые данные:
```bash
py manage.py init_rbac
py manage.py init_objects
```

Запускаем сервер:
```bash
py manage.py runserver
```

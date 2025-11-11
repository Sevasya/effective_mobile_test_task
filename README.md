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

### В данной папке создайте файл .env (Я работаю в VS Code, в другом редакторе могут быть другие команды)

```bash
code .env 
```

### В данный файл скопируйте данный код и замените значения логина, пароля и ключа на свои:

```bash
POSTGRES_USER=YOUR_USERNAME
POSTGRES_PASSWORD=YOUR_PASSWORD
SECRET_KEY=YOUR_SECRET_KEY
```

### Создайте виртуальное окружение и активируйте его:
```bash
py -m virtualenv env
.\env\Scripts\activate
```

### Установите зависимости:
```bash
pip install -r .\requirements.txt
```

### Запустите образ PostgreSQL (убедитесь, что Docker на Вашем компьтере запущен):

```bash
docker-compose up -d
```

### Далее применяем миграции:
```bash
cd .\effective_mobile\
py manage.py makemigrations objects
py manage.py makemigrations users 
py manage.py migrate
```

### Создаем тестовые данные:
```bash
py manage.py init_rbac
py manage.py init_objects
```

### Запускаем сервер:
```bash
py manage.py runserver
```

### По адресу 127.0.0.1:8000/docs представлены все эндпоинты приложения

Мы создали трех пользователей:

1.  Email: admin@example.com 
    Пароль: admin123
2.  Email: user1@example.com 
    Пароль: user123
3.  Email: user2@example.com 
    Пароль: user123

Первый - администратор, остальные - рядовые пользователи

Администратор имеет доступ абсолютно ко всему, в том числе к редактированию прав доступа.

Изначально у ролей (а их всего две - admin и user) стоят такие ограничения:

```bash
read_all_permission = True
read_exact_permission = True
```

Это позволяет им просматривать как конкретные товары, так и каждый отдельный товар.

Администратор может изменить данные параметры, тем самым ограничив доступ к просмотру всех товаров, отдельного товара или и того, и другого сразу.

Заказы пользователь видит только свои, к чужим у него нет доступа. Администратор может посмотреть любой заказ.

### Тестовые данные также содержат три товара (products):

```bash
{"id": 1, "name": "Laptop"}
{"id": 2, "name": "Phone"}
{"id": 3, "name": "Tablet"}
```

### А также заказы:

```bash
{"id": 1, "name": "Laptop", "owner": user1, "quantity": 2}
{"id": 2, "name": "Phone", "owner": user2, "quantity": 1}
```

Что позволяет увидеть приложение в действии.

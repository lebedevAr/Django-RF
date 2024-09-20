# Инструкция по запуску

## 1. Клонирование репозитория: 
```
git clone git@github.com:lebedevAr/Django-RF.git
```

## 2. Установка requirements.txt
```
cd Django-RF/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
## 3. Выполнение миграций
```
cd backend/
python manage.py makemigrations tasks
python manage.py migrate
```
## 4. Запуск сервера
```
python manage.py runserver
```
**Тестирование:** Команда выполняется также находясь в директории backend/
```
 python manage.py test tasks/
```

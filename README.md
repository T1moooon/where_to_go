# Where to Go

Сервис для отображения мест на карте с возможностью управления контентом через админку.

## Установка и запуск

1. **Создайте виртуальное окружение и установите зависимости**:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install requirements.txt
    ```

2. **Создайте файл `.env`**:
    ```python
    SECRET_KEY=ваш_секретный_ключ # обязательлно для запуска сервера
    DEBUG=True # В продакшне установите False
    ALLOWED_HOSTS=localhost,127.0.0.1,ваш-домен.com # Разделяйте хосты запятыми, без пробелов
    ```

3. **Запуск**:
    ```bash
    python manage.py migrate
    python manage.py runserver
    python manage.py load_place http://адрес/файла.json # Добавить локацию в бд
    ```
# vk-app-chatbot

Это простой backend-сервис на FastAPI для обработки событий Callback API ВКонтакте. Приложение принимает и обрабатывает различные такие события, как подтверждение Callback API, разрешение на отправку сообщений, событие набора текста и новые сообщения, отправляя приветственные ответы или обрабатывая вложения.

## Требования

- Python 3.9+
- [vk-tunel](https://dev.vk.com/ru/libraries/tunnel) 
  

## Настройка переменных окружения (.env)
Добавьте файл `.env`, указав там:
```dotenv
VK_TOKEN=your_vk_api_token
CONFIRMATION_TOKEN=your_confirmation_token
GROUP_ID=your_group_id
SECRET_KEY=your_secret_key
```

* `VK_TOKEN`. Можно взять в настройках вашего сообщества ВКонтакте в разделе "Работа с API"
* `CONFIRMATION_TOKEN`. Указывается в настройках Callback API вашего сообщества
* `GROUP_ID`. Можно найти также в Callback API вашего сообщества или в основной информации настройках сообщества
* `API_VERSION` не обязательна.

## Запуск сервера

1. Устаналиваем зависимости
```bash
pip install -r requirements.txt
```

2. Запускаем приложение с помощью `uvicorn`
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8088 --reload
```

Для работы с локальным сервером можно воспользоваться тунеллированием через [vk-tunel](https://dev.vk.com/ru/libraries/tunnel).

Запуск:
```bash
vk-tunel 8088
```

В настройках Callback API в сообществе ВКонтакте, вставьте URL полученный от vk-tunel, с добавлением маршрута `/vk_callback`

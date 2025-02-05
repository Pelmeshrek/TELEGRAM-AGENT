# Bot-Manager: AI-Agent for Telegram

---

## Содержание (Table of Contents)

1. [Описание проекта (Project Description)](#описание-проекта-project-description)
2. [Возможности (Features)](#возможности-features)
3. [Технологии (Technologies)](#технологии-technologies)
4. [Установка и настройка (Installation and Setup)](#установка-и-настройка-installation-and-setup)
   - [1. Загрузка модели Ollama (Downloading the Ollama Model)](#1-загрузка-модели-ollama-downloading-the-ollama-model)
   - [2. Запуск Ollama (Running Ollama)](#2-запуск-ollama-running-ollama)
   - [3. Установка зависимостей Python (Install Python Dependencies)](#3-установка-зависимостей-python-install-python-dependencies)
   - [4. Telegram API (Telegram API Credentials)](#4-telegram-api-telegram-api-credentials)
5. [Использование (Usage)](#использование-usage)
6. [Инструкция по получению Telegram API ID и Hash (How to Get Telegram API ID and Hash)](#инструкция-по-получению-telegram-api-id-и-hash-how-to-get-telegram-api-id-and-hash)
7. [Лицензия (License)](#лицензия-license)
8. [Контакты и обратная связь (Contact and Feedback)](#контакты-и-обратная-связь-contact-and-feedback)

---

## Описание проекта (Project Description)

**Bot-Manager** — это Telegram-бот, который:
1. Отвечает на личные сообщения в заданном стиле (определяется переменной `SYSTEM_PROMPT`).
2. Отправляет краткую сводку (summary) в «Избранное» (Saved Messages), где формат сводки определяется переменной `SUMMARY_SYSTEM_PROMPT`.

Основной механизм работы — взаимодействие с локально развернутой моделью через [Ollama](https://ollama.com/). Вы задаёте стиль ответа и вид получаемой сводки, а бот автоматически отвечает на входящие сообщения.

---

## Возможности (Features)

- **Гибкая настройка ответа**: Задавайте стиль, тон и формат AI-ответов.
- **Автоматическая отправка сводки**: Bot-Manager формирует краткий обзор (summary) и пересылает его в «Избранное».
- **Локальная модель**: Для генерации ответов используется модель, запущенная на вашем компьютере через [Ollama](https://ollama.com/), что обеспечивает большую приватность и контроль над процессом.
- **Поддержка нескольких языков**: Код можно адаптировать как под русский, так и под английский язык (и не только).

---

## Технологии (Technologies)

- **Python** (3.9+)
- **Telethon** или **Pyrogram** (для взаимодействия с Telegram API)
- **[Ollama](https://ollama.com/)** (для запуска локальной модели)
- **OpenAI O1** / **Google Gemini** (опционально, если интеграция нужна для дополнительных функций)

---

## Установка и настройка (Installation and Setup)

Ниже описаны шаги по установке и первичному запуску бота:

### 1. Загрузка модели Ollama (Downloading the Ollama Model)

1. Перейдите на сайт [Ollama](https://ollama.com/) и скачайте подходящую модель.  
   *Пример:* Выбираем модель **phi4**.

2. Сохраните модель в удобном для вас месте. Запомните путь к файлу модели (или имя модели, если Ollama сохраняет её в дефолтном каталоге).

### 2. Запуск Ollama (Running Ollama)

1. Откройте **Windows PowerShell** или другую консоль.
2. Выполните команду:
   ```bash
   ollama run <имя_вашей_модели>
   ```
   Замените `<имя_вашей_модели>` на конкретное имя (например, `phi4`).
3. После проверки работы модели завершите процесс и запустите службу Ollama:
   ```bash
   ollama serve
   ```
   Это позволит боту обращаться к модели через локальный сервер.

### 3. Установка зависимостей Python (Install Python Dependencies)

1. Убедитесь, что у вас установлен **Python 3.9+** (в идеале — последняя версия).
2. Склонируйте или скачайте данный репозиторий.
3. В корне проекта создайте виртуальное окружение (рекомендуется):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Для Linux/Mac
   # или
   venv\Scripts\activate      # Для Windows
   ```
4. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Telegram API (Telegram API Credentials)

1. Получите **API ID** и **API Hash**, следуя инструкции [ниже](#инструкция-по-получению-telegram-api-id-и-hash-how-to-get-telegram-api-id-and-hash).
2. Создайте в корне проекта `.env` файл или используйте любой другой способ хранения переменных окружения. Добавьте в него:
   ```
   API_ID=123456
   API_HASH=abc123def456
   PHONE=+1234567890
   ```
   *(PHONE — ваш номер телефона, привязанный к Telegram)*

---

## Использование (Usage)

1. Запустите Ollama:
   ```bash
   ollama serve
   ```
2. Запустите Python-скрипт:
   ```bash
   python main.py
   ```
   *или любое другое название вашего основного бота-файла.*
3. При первом запуске Telegram-библиотека (Telethon или Pyrogram) запросит авторизацию:
   - Введите **номер телефона**.
   - Введите **код**, полученный в Telegram.
   - (Если у вас есть **пароль**, введите его тоже.)
4. После успешной авторизации бот будет автоматически:
   - Отвечать на **личные сообщения** согласно вашему `SYSTEM_PROMPT`.
   - Отправлять сводку в «Избранное» в соответствии с `SUMMARY_SYSTEM_PROMPT`.

---

## Инструкция по получению Telegram API ID и Hash (How to Get Telegram API ID and Hash)

1. **Создайте Telegram-аккаунт**  
   Убедитесь, что у вас есть зарегистрированный аккаунт в Telegram.

2. **Зайдите на Telegram Developers Platform**  
   Перейдите на сайт [my.telegram.org](https://my.telegram.org/).  
   Введите номер телефона, к которому привязан ваш Telegram.  
   Введите код, полученный в Telegram.

3. **Создайте новое приложение**  
   - На главной странице выберите **API Development Tools**.  
   - Заполните форму:  
     - **App title**: (напр. MyApp)  
     - **Short name**: (напр. myapp)  
   - Нажмите **Create Application**.

4. **Получите свои API ID и API Hash**  
   После создания приложения будут доступны:  
   - **API ID** (например, `12345678`)  
   - **API Hash** (например, `abc123def456ghi789jkl`)

5. **Сохраните эти данные**  
   Вам понадобятся эти значения для подключения к Telegram API.

---

## Лицензия (License)

Данный проект распространяется по свободной лицензии на ваше усмотрение (MIT, Apache 2.0 и т.д.). В репозитории можно добавить соответствующий лицензионный файл, если это необходимо.

---

## Контакты и обратная связь (Contact and Feedback)

- **Автор:** [@YourTelegramUsername](https://t.me/YourTelegramUsername)  
- **GitHub:** [YourGitHubProfile](https://github.com/YourGitHubProfile)  
- Любые вопросы, предложения или найденные ошибки присылайте в **Issues** репозитория или в личные сообщения.

---

**Спасибо за использование Bot-Manager!** Если этот проект оказался полезным, не забудьте поставить звёздочку на GitHub, чтобы поддержать его развитие. Good luck and have fun!

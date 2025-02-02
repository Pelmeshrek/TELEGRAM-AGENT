
---

# Bot-Manager: AI Agent Telegram Bot

![Bot-Manager Banner](https://via.placeholder.com/800x200?text=Bot-Manager)  
*Ваш персональный AI-агент для Telegram, отвечающий в заданном стиле и отправляющий сводки!*

---

## О проекте / About

Привет всем!  
Я – 16-летний школьник, и это мой первый проект, связанный с AI-агентами. Bot-Manager – это Telegram-бот, который:
- **Отвечает на сообщения** в личных чатах, используя стиль, заданный переменной `SYSTEM_PROMPT`.
- **Отправляет краткую сводку** в раздел «Избранное», оформленную согласно переменной `SUMMARY_SYSTEM_PROMPT`.

Некоторые фрагменты кода были созданы с помощью [OpenAI O1](https://openai.com/) и [Google Gemini](https://ai.google/).  
All code variables are clearly named, so setting up the project should be straightforward!

---

## Особенности / Features

- **Лёгкая настройка:** Понятные имена переменных позволяют быстро разобраться с конфигурацией.
- **Гибкая персонализация:** Задавайте уникальный стиль для ответов через `SYSTEM_PROMPT` и `SUMMARY_SYSTEM_PROMPT`.
- **Автоматическая сводка:** Получайте краткие сводки сообщений в «Избранном».
- **Билингвальная документация:** Инструкции на русском и английском языках.

---

## Установка / Installation

### 1. Загрузка модели / Download a Model

- Перейдите на [Ollama](https://ollama.com/) и скачайте подходящую модель (например, `phi4`).
- Visit [Ollama](https://ollama.com/) and download a model that suits you (e.g., `phi4`).

### 2. Запуск модели / Run the Model

Откройте Windows PowerShell и выполните следующие команды:

```bash
ollama run <your_model>
ollama serve

Замените <your_model> на название скачанной модели.


---

3. Установка библиотек и настройка Telegram / Install Libraries & Configure Telegram

Установите необходимые библиотеки. Проверьте наличие файла requirements.txt или следуйте дополнительным инструкциям.

Получите API-ключи Telegram – API ID и API Hash (подробности ниже).

Авторизуйтесь: введите свой номер, код из Telegram и, если требуется, пароль.



---

Получение Telegram API ID и API Hash

Шаги для получения ключей:

1. Создайте Telegram-аккаунт / Create a Telegram Account
Убедитесь, что у вас есть зарегистрированный аккаунт, так как ключи привязаны к вашему профилю.
Make sure you have a registered Telegram account.


2. Войдите на платформу разработчиков / Log in to Telegram Developers Platform

Перейдите на my.telegram.org.

Войдите, используя номер, привязанный к Telegram, и введите код, который вам пришёл.

Visit my.telegram.org.

Log in with your phone number and enter the code sent via Telegram.



3. Создайте новое приложение / Create a New Application

Выберите API Development Tools на главной странице.

Заполните форму:

App title: Название вашего приложения (например, MyApp).

Short name: Краткое название (например, myapp).


Нажмите Create Application.

On the main page, select API Development Tools.

Fill in the form:

App title: Your app's name (e.g., MyApp).

Short name: A short name (e.g., myapp).


Click Create Application.



4. Получите API ID и API Hash / Retrieve API ID and API Hash
После создания приложения вам будут предоставлены:

API ID: (например, 12345678)

API Hash: (например, abc123def456ghi789jkl)



5. Сохраните данные / Save Your Details
Запишите API ID и API Hash в безопасном месте — они понадобятся для работы с Telegram API через библиотеки, такие как Telethon или Pyrogram.
Save these details securely—they are required for using the Telegram API with libraries like Telethon or Pyrogram.




---

Использование / Usage

1. Запустите код проекта.
После настройки модели и получения ключей Telegram, запустите основной скрипт проекта.


2. Автоматические ответы и сводки.
Бот будет отвечать на личные сообщения согласно переменным SYSTEM_PROMPT и SUMMARY_SYSTEM_PROMPT и отправлять краткие сводки в «Избранное».


3. Наслаждайтесь!
Если возникнут вопросы или проблемы, не стесняйтесь создавать issue или обращаться за помощью.




---

Вклад / Contributing

Ваши идеи и предложения очень приветствуются! Если вы нашли баг или хотите предложить улучшения, создайте issue или отправьте pull request.


---

Лицензия / License

Этот проект распространяется под лицензией MIT License.


---

Спасибо за внимание и удачи в использовании Bot-Manager!
Thank you for checking out Bot-Manager and happy coding!

---

Вы можете дополнительно настроить этот README, добавив, например, ссылки на документацию или графику, соответствующую теме проекта. Надеюсь, этот вариант сделает ваш репозиторий более привлекательным и информативным!


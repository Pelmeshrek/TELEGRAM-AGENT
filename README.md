


Всем здравсвтуйте. Не судите строго, я школьник, мне 16, и это мой первый "проект", связанный с ИИ-агентами. Это моя работа, но некоторые фрагменты были сделанны с помощью openai o1 и Google Gemini.

Bot-Manager это бот, который будет отвечать на сообщения в заданном стиле и отправлять сводку написавшему.

ИИ-агент отвечает на сообщения, написанные в личных сообщениях, в выбранном стиле, заданном в переменной SYSTEM_PROMPT. ИИ-агент отправляет краткую сводку во вкладку «Избранное», отредактированную в соответствии с переменной SUMMARY_SYSTEM_PROMPT.

Все переменные в коде названы понятно, так что вопросов о том, куда и что вводить, у вас не должно возникнуть.

Вот инструкция:

1. скачиваете подходящую Вам модель с сайта https://ollama.com/ (в моем случа phi4).


2. как скачается в Windows Powershell пишите команду ollama run (ваша модель).


3. затем пишите ollama serve и в целом первая часть готова (ну у меня проблем не было).


4. устанавливаете библиотеки, получаете Ваши api и тп аккаунта телеграм (инструкцию на это от ЧАТА ГПТ после основной части).


5. авторизуетесь, как запустите код и все работает! (телефоный номер, код который пришел Вам в тг, и пароль если есть)


6. сводка приходит в избранные.




---

Hello everyone! Please don't judge me too harshly—I'm a high school student, 16 years old, and this is my first "project" related to AI agents. This is my work, but some parts of the code was written by OpenAI O1 and Google Gemini.

Bot-Manager is a bot that responds to messages in a specified style and sends a summary to the user who wrote them.

The AI agent responds to messages written in private chats in the selected style defined by the SYSTEM_PROMPT variable. The AI agent sends a brief summary to the "Favorites" tab, edited according to the SUMMARY_SYSTEM_PROMPT variable.

All variables in the code are clearly named, so you shouldn't have any questions about where and what to enter.

Here are the instructions:

1. Download a model that suits you from the website https://ollama.com/ (in my case, phi4).


2. Once downloaded, open Windows PowerShell and run the command: ollama run <your_model>.


3. Then, type ollama serve, and the first part is complete (I didn't encounter any issues here).


4. Install the necessary libraries, get your Telegram account API, and so on (Instruction from CHAT GPT is after the main part).


5. Authorize your account, run the code, and everything should work! (phone number, the code you received in Telegram, and the password if applicable)


6. the summary is sent to saved messages.




---

Как получить Telegram API ID и API Hash / How to Get Telegram API ID and API Hash

1. Создайте Telegram-аккаунт / Create a Telegram Account Убедитесь, что у вас есть зарегистрированный аккаунт в Telegram, так как API-ключи связаны с вашим профилем. Make sure you have a registered Telegram account, as the API keys are tied to your profile.


2. Войдите на Telegram Developers Platform / Log in to Telegram Developers Platform



Перейдите на сайт https://my.telegram.org/. Go to https://my.telegram.org/. Войдите, используя свой номер телефона, привязанный к Telegram. Log in using your phone number linked to Telegram. Введите код, который придёт вам в Telegram. Enter the code sent to you via Telegram. 3. Создайте новое приложение / Create a New Application На главной странице выберите "API Development Tools". On the main page, select "API Development Tools". Заполните форму: Fill in the form: App title: Укажите название вашего приложения (например, MyApp). Enter the name of your app (e.g., MyApp). Short name: Укажите краткое название (например, myapp). Enter a short name (e.g., myapp). Остальные поля заполняются автоматически, но вы можете указать дополнительные данные. The other fields are filled in automatically, but you can add extra information. Нажмите Create Application. Click Create Application. 4. Получите свои API ID и API Hash / Retrieve Your API ID and API Hash После создания приложения вам будут выданы: After creating the application, you will be provided with:

API ID (например, 12345678) / API ID (e.g., 12345678) API Hash (например, abc123def456ghi789jkl) / API Hash (e.g., abc123def456ghi789jkl) 5. Сохраните эти данные / Save These Details Запишите API ID и API Hash в безопасное место. Эти данные необходимы для работы с Telegram API через сторонние библиотеки, такие как Telethon или Pyrogram. Save the API ID and API Hash in a secure place. These details are required to work with Telegram API via third-party libraries like Telethon or Pyrogram.


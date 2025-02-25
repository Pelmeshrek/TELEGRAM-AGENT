# Bot-Manager: AI-Агент для Telegram (на Telethon + Ollama)

Данный репозиторий содержит **два** файла примеров кода на Python, которые позволяют:
1. Использовать локально развернутую модель через [Ollama](https://ollama.com/) для генерации ответов на сообщения.
2. Периодически отправлять сводку новых сообщений владельцу бота.
3. Вести историю диалога с каждым пользователем (для контекста ответа).

Оба файла используют библиотеку **Telethon** для работы с Telegram API. Разница в том, как происходит авторизация и какие задачи решаются (бот с токеном vs. клиент, который логинится по номеру телефона). Вы можете выбрать подходящий вам вариант кода или адаптировать их под свои нужды.

---

## 1. Описание файлов

1. **`Bot-Manager.py`**

   - Авторизация бота по **токену** (`BOT_TOKEN`).
   - Параметры:
     - `api_id`, `api_hash` — ключи для работы с Telegram API (берутся на [my.telegram.org](https://my.telegram.org/)).
     - `BOT_TOKEN` — токен, выданный [@BotFather](https://t.me/BotFather).
     - `BOT_OWNER_ID` — ваш (ID владельца бота), чтобы бот знал, кому отправлять сводку.
     - `SUMMARY_INTERVAL_SECONDS` — интервал (в секундах), через который бот отправляет сводку.
     - `OLLAMA_API_URL` и `OLLAMA_MODEL` — настройки для взаимодействия с локальным сервером Ollama.
   - Ведётся **история диалога** с пользователями.  
   - Бот **автоматически отвечает** всем, кроме владельца (`BOT_OWNER_ID`), опрашивая модель Ollama.  
   - Каждые `SUMMARY_INTERVAL_SECONDS` минут бот формирует сводку из последних сообщений (хранятся во внутреннем буфере) и отправляет её владельцу.

2. **`main.py`**

   - Авторизация как обычный пользователь (по **номер_телефона** и коду, полученному в Telegram).  
   - Параметры:
     - `api_id`, `api_hash` — аналогично, ключи с [my.telegram.org](https://my.telegram.org/).
     - `UNIFIED_SESSION_NAME` — имя для локальной сессии (Telethon).
     - `BOT_OWNER_ID` — идентификатор владельца, получающий сводки.
     - `SYSTEM_PROMPT`, `SUMMARY_SYSTEM_PROMPT` — тексты промптов для Ollama (ответы «секретаря» и суммаризация сообщений).
     - `MAX_CONTEXT_LENGTH` — лимит хранимых сообщений диалога.
     - `IGNORED_USER_IDS`, `IGNORED_USERNAMES` — списки, кому «секретарь» не отвечает.
     - `new_messages_buffer` — общий буфер, куда собираются сообщения для сводки.
     - `OLLAMA_API_URL`, `OLLAMA_MODEL` — для связи с Ollama.
   - Скрипт имеет два основных обработчика:
     1. **`handle_secretary`**: «Секретарь» — автоматически отвечает пользователям в личных сообщениях, если они не в игнор-листе.
     2. **`handle_summary_collection`**: собирает **все** входящие сообщения (кроме своих собственных) в буфер для дальнейшей суммаризации.
   - Периодически (каждые `SUMMARY_INTERVAL_SECONDS`) запускается задача `summary_loop()`, которая формирует сводку последних сообщений (из `new_messages_buffer`) и отправляет её **владельцу** (`BOT_OWNER_ID`).

Вы можете запускать эти файлы независимо друг от друга или выбрать только один, в зависимости от того, нужна ли вам авторизация через бот-токен либо через свой аккаунт. Оба варианта используют Ollama для генерации ответов и периодической суммаризации.

---

## 2. Возможности и отличия

- **Bot-Manager.py**:
  - Работает как **Telegram-бот** (через токен `BOT_TOKEN`).
  - Хорош для публичного бота, когда пользователи должны писать именно боту, а не лично вам.
  - Каждые 20 минут (по умолчанию) отправляет сводку владельцу.
  - Хранит историю диалога по каждому пользователю в `user_conversations`.

- **main.py**:
  - Работает как **ваш личный клиент** (логин через номер телефона).
  - Позволяет вести «приватного секретаря», который отвечает в ЛС от вашего лица.
  - Имеет списки игнорирования по ID/username.
  - Аналогично, формирует и отправляет сводку владельцу (то есть вам) на регулярной основе.

---

## 3. Установка и настройка

### Шаг 1. Установка Python и зависимостей

1. Установите **Python 3.9+**.
2. Клонируйте или скачайте данный репозиторий.
3. (Опционально) Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   # или
   venv\Scripts\activate      # Windows
   ```
4. Установите зависимости:
   ```bash
   pip install telethon requests
   ```

### Шаг 2. Настройка Ollama

1. Скачайте и установите [Ollama](https://ollama.com/) (следуйте инструкции на сайте).
2. Загрузите модель (например, `phi4`) и проверьте её запуск:
   ```bash
   ollama run phi4
   ```
   Если модель успешно ответила (вида `> `), значит она работает.
3. Остановите процесс и запустите Ollama в режиме сервера:
   ```bash
   ollama serve
   ```
   По умолчанию сервер запустится на `localhost:11434`, что соответствует `OLLAMA_API_URL` в коде.

### Шаг 3. Получение Telegram API ID и API Hash

1. Перейдите на сайт [my.telegram.org](https://my.telegram.org/).
2. Авторизуйтесь по номеру телефона (введите код, который придёт вам в Telegram).
3. Зайдите в **API Development Tools** и создайте новое приложение (App).
4. Сохраните `api_id` и `api_hash` (присвоенные вам) — они понадобятся в коде.

### Шаг 4. Настройка переменных в коде

Откройте один из файлов (например, `Bot-Manager.py`):

- Замените вверху `api_id = 'YOUR_API_ID'` и `api_hash = 'YOUR_API_HASH'` на ваши реальные значения.  
- Укажите `BOT_TOKEN` (выданный BotFather).  
- Укажите `BOT_OWNER_ID` (свой Telegram ID, чтобы вы получали сводку).

Аналогично, если хотите использовать `main.py`, отредактируйте в нём:

- `api_id`, `api_hash`.
- `BOT_OWNER_ID` — чтобы получить сводки.  
- При первом запуске вас попросят ввести **телефон** и **код**, полученный в Telegram; при включённой 2FA — **пароль**.

---

## 4. Запуск

**Запуск `Bot-Manager.py` (бот с токеном):**

1. Убедитесь, что Ollama работает:
   ```bash
   ollama serve
   ```
2. Запустите скрипт:
   ```bash
   python Bot-Manager.py
   ```
3. При первом запуске (если надо) будет создана сессия Telethon. Если в коде требуется ввести `phone`/`code`, сделайте это в консоли. Для бота обычно достаточно токена `BOT_TOKEN`.

**Запуск `main.py` (авторизация через номер телефона):**

1. Также убедитесь, что Ollama работает:
   ```bash
   ollama serve
   ```
2. Запустите скрипт:
   ```bash
   python main.py
   ```
3. Скрипт попросит ввести ваш телефон, код из Telegram и при необходимости пароль 2FA. После успешной авторизации начнётся приём сообщений и периодическая отправка сводок.

---

## 5. Принцип работы сводок

Оба кода реализуют «буфер» для новых сообщений (`new_messages_buffer`). Каждое новое сообщение (не от самого бота/клиента) складывается в этот буфер. Периодически (через `SUMMARY_INTERVAL_SECONDS`) запускается задача, которая:

1. Копирует и очищает `new_messages_buffer`.
2. Передаёт скопированные сообщения в Ollama с **промптом сводки** (`SUMMARY_SYSTEM_PROMPT`).
3. Полученный итоговый текст отправляет **владельцу** (ID = `BOT_OWNER_ID`).

Вы сами можете регулировать частоту отправки (`SUMMARY_INTERVAL_SECONDS`) и объём сообщений для суммаризации (`MAX_MESSAGES_IN_SUMMARY`).

---

## 6. Советы по кастомизации

- **Измените промпты** (`SYSTEM_PROMPT` и `SUMMARY_SYSTEM_PROMPT`) под свой стиль общения и формат суммаризации.
- При необходимости включайте/выключайте ведение полной истории диалога. Увеличение `MAX_CONTEXT_LENGTH` делает ответы более контекстуальными, но может замедлять генерацию.
- В `main.py` есть механизмы игнорирования пользователей по ID и username: `IGNORED_USER_IDS` и `IGNORED_USERNAMES`. Можно дополнить логику — например, игнорировать группы и каналы.

---

## 7. Частые проблемы

1. **Ollama не отвечает**:  
   - Проверьте, что сервер Ollama запущен (`ollama serve`).
   - Убедитесь, что `OLLAMA_API_URL` и `OLLAMA_MODEL` совпадают с вашими настройками.

2. **Телефон или код некорректен** (в `main.py`):  
   - Убедитесь, что формат номера телефона: `+71234567890`.  
   - Код должен быть точно таким, как в Telegram-сообщении (без лишних пробелов).

3. **Не отправляются сводки**:  
   - Проверьте, что `BOT_OWNER_ID` — это ваш актуальный числовой Telegram ID (не username).  
   - Убедитесь, что `new_messages_buffer` действительно пополняется (в логе должны быть сообщения).

---

## 9. Обратная связь

- Автор: *Telegram - @TimZlush*
- Любые вопросы и предложения направляйте личные сообщения.  
- Если вам понравился проект, поставьте звёздочку (★) на GitHub!

---

**Удачного использования Bot-Manager!**  
Пусть ваш AI-агент эффективно помогает в Telegram, а периодические сводки упростят анализ переписки.

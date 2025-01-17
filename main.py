# -*- coding: utf-8 -*-
import asyncio
import logging
import sys
import io
import datetime
import json
import requests

from telethon.tl.types import Channel
from telethon import TelegramClient, events
from telethon.errors import (
    SessionPasswordNeededError,
    PhoneCodeInvalidError,
    PhoneNumberInvalidError
)

# ------------------------------------------------------------------
# Настройки вывода, чтобы корректно обрабатывалась кириллица
# Output settings for correct Cyrillic text handling
# ------------------------------------------------------------------
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

# ------------------------------------------------------------------
# Параметры и константы
# Parameters and constants
# ------------------------------------------------------------------

my_id = 'yourid'  # Used to skip our own messages in the summary handler

# Лимит на количество сообщений, которые отдаём в сводку (чтобы не перегружать модель)
# Limit of messages for the summary (avoid overloading the model)
MAX_MESSAGES_IN_SUMMARY = 100

api_id = 'yourid'   # Ваш API_ID (Your Telegram API_ID)
api_hash = 'yourhash'  # Ваш API_HASH (Your Telegram API_HASH)
UNIFIED_SESSION_NAME = 'unified_session_name'  # Имя сессии для Telethon (Telethon session name)

# URL Ollama (локальный сервер)
# Ollama API endpoint (local server)
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi4:latest"

# ID владельца бота (вам будут отправляться сводки)
# Bot owner's ID (will receive summaries)
BOT_OWNER_ID = 'yourid'

# Каждые n минут будет отправляться сводка
# Summary sending interval (in seconds)
SUMMARY_INTERVAL_SECONDS = 60*20

# ------------------------------------------------------------------
# Промпты для Ollama
# Prompts for Ollama
# ------------------------------------------------------------------

# Промпт для «секретаря»
# System prompt for "secretary" functionality
SYSTEM_PROMPT = """
neura promt for answering
нейро промт для ответа
"""

# Промпт для сводки
# System prompt for generating message summaries
SUMMARY_SYSTEM_PROMPT = """
promt for summary
промт для суммаризации
"""

# ------------------------------------------------------------------
# Дополнительные настройки
# Additional settings
# ------------------------------------------------------------------

# Максимальное количество сообщений в истории для «секретаря»
# Max number of messages in context history
MAX_CONTEXT_LENGTH = 5

# Словарь для хранения контекста (истории) ответов «секретаря»
# Dictionary to store user context (conversation history)
# Format: {user_id: [{"role": "user", "content": "..."},
#                   {"role": "assistant", "content": "..."}]}
user_contexts = {}

# Список ID пользователей, которым не отвечаем
# List of user IDs to ignore
IGNORED_USER_IDS = [111, 222]

# Список username, которым не отвечаем
# List of usernames to ignore
IGNORED_USERNAMES = ["", "", ""]

# Список (буфер) новых сообщений для сводки
# Buffer with new messages for summary
new_messages_buffer = []

# Логирование
# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация Telethon-клиента
# Telethon client initialization
client = TelegramClient(UNIFIED_SESSION_NAME, api_id, api_hash)


# ------------------------------------------------------------------
# Функции для работы с Ollama (ответы «секретаря» и сводка)
# Functions for interacting with Ollama (secretary responses and summary)
# ------------------------------------------------------------------

async def generate_response(prompt, user_id, model=OLLAMA_MODEL):
    """
    Генерация ответа при помощи Ollama (логика «секретаря»).
    Generate a response using Ollama (secretary logic).
    """
    headers = {"Content-Type": "application/json"}
    context = user_contexts.get(user_id, [])

    # Собираем полный промпт
    # Build the full prompt
    full_prompt = f"{SYSTEM_PROMPT}\n"

    # Добавляем последние сообщения (для контекста)
    # Add the last messages for context
    if context:
        full_prompt += "\nПоследние сообщения для контекста:\n"
        for msg in context[-MAX_CONTEXT_LENGTH:]:
            if msg["role"] == "user":
                full_prompt += f"Я: {msg['content']}\n"
            else:
                full_prompt += f"Ты: {msg['content']}\n"

    full_prompt += f"Я: {prompt}\nТы: "

    data = {
        "model": model,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(data), timeout=120)
        response.raise_for_status()
        response_json = response.json()

        if response_json.get("done"):
            if "response" in response_json:
                # Сохраняем историю (Store the conversation in context)
                user_contexts.setdefault(user_id, []).append({"role": "user", "content": prompt})
                user_contexts[user_id].append({"role": "assistant", "content": response_json["response"]})
                return response_json["response"]
            else:
                return "Ошибка: Некорректный ответ от Ollama."
        else:
            return "Ошибка: Генерация не завершена."
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе к Ollama: {e}"
    except Exception as e:
        return f"Неизвестная ошибка: {e}"


def summarize_messages_with_ollama(messages):
    """
    Отправляет список сообщений в модель Ollama для краткого резюме (сводки).
    Sends a list of messages to the Ollama model for a brief summary.
    """
    # Обрезаем число сообщений (Truncate the message list)
    messages_to_summarize = messages[:MAX_MESSAGES_IN_SUMMARY]

    # Превращаем список сообщений в строку (Convert the message list to a single string)
    messages_text = "\n".join(
        f"• [{m['chat_title'] or 'ЛС/группа'}] {m['sender_name']}: {m['text']}"
        for m in messages_to_summarize
    )

    # Собираем полный промпт (Build the full prompt)
    full_prompt = (
        f"{SUMMARY_SYSTEM_PROMPT}\n\n"
        f"Вот новые сообщения:\n\n"
        f"{messages_text}\n\n"
        f"Кратко опиши, о чём речь в сообщениях:\n"
    )

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": full_prompt,
        "stream": False
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(OLLAMA_API_URL, headers=headers, data=json.dumps(payload), timeout=120)
        response.raise_for_status()
        response_json = response.json()

        if response_json.get("done") and "response" in response_json:
            return response_json["response"]
        else:
            return "Ошибка: модель не вернула корректный результат."
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе к Ollama: {e}"


# ------------------------------------------------------------------
# Обработчики событий (Handlers)
# Event handlers
# ------------------------------------------------------------------

@client.on(events.NewMessage(incoming=True))
async def handle_secretary(event):
    """
    Обработчик «секретаря»: отвечает пользователям в приватном чате
    (если они не в игнор-листе).
    "Secretary" handler: replies to users in private chat
    (if they are not in the ignore list).
    """
    if event.is_private:
        user_id = event.sender_id
        user_entity = await client.get_entity(user_id)
        username = user_entity.username if user_entity.username else "NoUsername"
        user_message = event.raw_text

        # Проверяем, игнорируем ли пользователя
        # Check if the user is ignored
        if user_id in IGNORED_USER_IDS or username in IGNORED_USERNAMES:
            logger.info(f"Пользователь {user_id} (username: {username}) в игнор-листе. Не отвечаем.")
            return

        # Генерируем ответ с помощью Ollama (Generate a response via Ollama)
        response_text = await generate_response(user_message, user_id)

        # Отправляем ответ (Send the reply)
        try:
            await event.reply(response_text)
            logger.info("Ответ секретаря отправлен пользователю.")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")


@client.on(events.NewMessage)
async def handle_summary_collection(event):
    """
    Обработчик для сбора сообщений, которые затем пойдут в сводку.
    Handler for collecting messages that will be summarized later.
    """
    global my_id
    if my_id is None:
        me = await client.get_me()
        my_id = me.id

    sender = await event.get_sender()
    if sender.id == my_id:
        return  # Пропускаем собственные сообщения (Skip own messages)

    # Обработка имени отправителя (Process the sender name)
    if isinstance(sender, Channel):
        sender_name = getattr(sender, 'title', "Канал без названия")
    else:
        sender_name = sender.username if sender.username else (sender.first_name or "Неизвестный пользователь")

    # Получаем название чата (Get chat title)
    if event.is_group or event.is_channel:
        chat = await event.get_chat()
        chat_title = getattr(chat, 'title', "Группа/Канал без названия")
    else:
        chat_title = None

    message_text = event.raw_text

    new_messages_buffer.append({
        "dt": datetime.datetime.now(),
        "sender_id": sender.id,
        "sender_name": sender_name,
        "chat_title": chat_title,
        "text": message_text
    })


# ------------------------------------------------------------------
# Периодическая задача для сводки
# Periodic task for generating and sending summaries
# ------------------------------------------------------------------

async def summary_loop():
    """
    Бесконечный цикл: каждые SUMMARY_INTERVAL_SECONDS формируем сводку
    из new_messages_buffer и отправляем её владельцу бота (BOT_OWNER_ID).
    Infinite loop: every SUMMARY_INTERVAL_SECONDS, generate a summary
    from new_messages_buffer and send it to the bot owner (BOT_OWNER_ID).
    """
    while True:
        await asyncio.sleep(SUMMARY_INTERVAL_SECONDS)

        if not new_messages_buffer:
            logger.info("Нет новых сообщений, сводка не сформирована.")
            continue

        # Копируем и очищаем глобальный буфер
        # Copy and clear the global buffer
        messages_to_summarize = new_messages_buffer.copy()
        new_messages_buffer.clear()

        # Генерируем сводку (Generate the summary)
        summary_text = summarize_messages_with_ollama(messages_to_summarize)

        # Отправляем результат владельцу бота
        # Send the result to the bot owner
        try:
            await client.send_message(BOT_OWNER_ID, summary_text)
            logger.info("Сводка отправлена владельцу бота.")
        except Exception as e:
            logger.error(f"Не удалось отправить сводку: {e}")


# ------------------------------------------------------------------
# Функция авторизации
# Authorization function
# ------------------------------------------------------------------

async def login():
    """
    Авторизация в Telegram через Telethon.
    Authorize in Telegram via Telethon.
    """
    try:
        await client.connect()
        if not await client.is_user_authorized():
            phone = input("Введите номер телефона (пример: +71234567890): ")
            try:
                await client.send_code_request(phone)
                code = input("Введите код из Telegram: ")
                await client.sign_in(phone, code)
            except SessionPasswordNeededError:
                password = input("Введите пароль двухфакторной аутентификации: ")
                await client.sign_in(password=password)
            except PhoneCodeInvalidError:
                logger.error("Введён неверный код подтверждения.")
                return False
            except PhoneNumberInvalidError:
                logger.error("Введён неверный номер телефона.")
                return False
        logger.info("Успешно авторизованы в Telegram!")
        return True
    except Exception as e:
        logger.error(f"Ошибка при авторизации: {e}")
        return False


# ------------------------------------------------------------------
# Основная функция
# Main function
# ------------------------------------------------------------------

async def main():
    authorized = await login()
    if not authorized:
        return

    # Запускаем фоновую задачу по сбору сводки
    # Launch a background task for summary collection
    asyncio.create_task(summary_loop())

    logger.info("Единый бот запущен. Ожидаем сообщения...")
    await client.run_until_disconnected()


# Запуск
# Entrypoint
if __name__ == "__main__":
    asyncio.run(main())

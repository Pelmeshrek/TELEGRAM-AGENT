# -*- coding: utf-8 -*-
"""
Telethon-based bot example with:
1) Periodic summary to the bot owner via Ollama
2) Dialogue history for each user
3) Real-time responses to users (except the owner)

В этом файле:
1) Периодическая отправка сводки владельцу бота через Ollama
2) Хранение истории диалога для каждого пользователя
3) Мгновенные ответы пользователям (кроме владельца)
"""

import asyncio
import logging
import sys
import io
import datetime
import json
import requests

from telethon import TelegramClient, events
from telethon.tl.types import Channel

# ------------------------------------------------------------------
# Настройка вывода в консоль (чтобы корректно работала кириллица)
# ------------------------------------------------------------------
# Setting up console output to correctly handle Cyrillic characters.
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')

# ------------------------------------------------------------------
# Параметры и константы / Parameters & constants
# ------------------------------------------------------------------

# Replace these with your actual values
api_id = 'YOUR_API_ID'            # Ваш api_id (от my.telegram.org)
api_hash = 'YOUR_API_HASH'        # Ваш api_hash
BOT_TOKEN = '1234567:ABC-xyz_bot' # Токен бота из BotFather

BOT_OWNER_ID = 123456789          # Telegram ID владельца бота (the owner's Telegram ID)
SUMMARY_INTERVAL_SECONDS = 60 * 20  # Каждые 20 минут шлем сводку / every 20 minutes

# URL Ollama (локальный сервер) / local Ollama server
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "phi4:latest"      # Example model name in Ollama

# Промпт для суммаризации (summary) / Prompt for summarizing messages
SUMMARY_SYSTEM_PROMPT = """
Вы — краткий суммаризатор переписки...
"""

# Промпт для общения с пользователями / Prompt for user responses
CHAT_SYSTEM_PROMPT = """
Вы — дружелюбный помощник...
"""

# Лимит сообщений в суммаризации / Max number of messages in summary
MAX_MESSAGES_IN_SUMMARY = 100

# Глобальный буфер для новых сообщений (для последующей суммаризации)
# A global buffer to store messages for future summarization
new_messages_buffer = []

# Словарь, где для каждого user_id храним историю диалога
# Dictionary to store conversation history per user_id
# Structure: user_id -> [(role, text), (role, text), ...]
user_conversations = {}

# Логирование / Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация Telethon-клиента (бот-сессия) / Telethon client initialization
client = TelegramClient('bot_session', api_id, api_hash)


# ------------------------------------------------------------------
# Функции для работы с Ollama / Ollama-related functions
# ------------------------------------------------------------------

def summarize_messages_with_ollama(messages):
    """
    Отправляет список сообщений в модель Ollama для краткого резюме (сводки).
    Sends a list of messages to Ollama model to get a short summary.
    """
    messages_to_summarize = messages[:MAX_MESSAGES_IN_SUMMARY]

    # Превращаем список сообщений в один текст / Convert list of messages into one text chunk
    messages_text = "\n".join(
        f"• [{m['chat_title'] or 'ЛС/группа'}] {m['sender_name']}: {m['text']}"
        for m in messages_to_summarize
    )

    # Формируем промпт / Construct the prompt
    full_prompt = (
        f"{SUMMARY_SYSTEM_PROMPT}\n\n"
        f"Вот новые сообщения:\n\n"
        f"{messages_text}\n\n"
        f"Кратко опиши, о чём речь в сообщениях:"
    )

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        response_json = response.json()
        if response_json.get("done") and "response" in response_json:
            return response_json["response"].strip()
        else:
            return "Ошибка: модель не вернула корректный результат."
    except requests.exceptions.RequestException as e:
        return f"Ошибка при запросе к Ollama: {e}"


def generate_user_prompt_history(user_id):
    """
    Формируем текст промпта на основе истории диалога пользователя с ботом.
    Build a prompt text from the conversation history between user and bot.
    """
    history = user_conversations.get(user_id, [])

    # Чтобы не перегружать модель, ограничиваем длину истории
    # Limit the conversation history to avoid overloading the model
    max_history_length = 10
    if len(history) > max_history_length:
        history = history[-max_history_length:]

    # Формируем «плоский» текст из сообщений / Construct a single text with roles
    history_str = ""
    for role, text in history:
        if role == "user":
            history_str += f"Пользователь: {text}\n"  # "User"
        else:
            history_str += f"Бот: {text}\n"           # "Assistant"

    return history_str


def generate_response_for_user(user_id, user_message):
    """
    Генерирует ответ для пользователя с учётом всей (обрезанной) истории.
    Generates a response for the user based on (truncated) conversation history.
    """
    # Получаем текст предыдущих сообщений
    # Get previous conversation text
    history_text = generate_user_prompt_history(user_id)

    # Добавляем текущее сообщение пользователя в промпт
    # Append current user message to the prompt
    full_prompt = (
        f"{CHAT_SYSTEM_PROMPT}\n\n"
        f"{history_text}"
        f"Пользователь: {user_message}\n\n"
        f"Бот:"
    )

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        resp = requests.post(OLLAMA_API_URL, json=payload, timeout=120)
        resp.raise_for_status()
        resp_json = resp.json()
        if resp_json.get("done") and "response" in resp_json:
            return resp_json["response"].strip()
        else:
            return "Извините, я сейчас не могу ответить."  # "Sorry, I can't answer now."
    except requests.exceptions.RequestException as e:
        return f"Извините, не получилось запросить модель: {e}"


# ------------------------------------------------------------------
# Обработчик входящих сообщений / Incoming message handler
# ------------------------------------------------------------------

@client.on(events.NewMessage(incoming=True))
async def handle_incoming_message(event):
    """
    Обрабатывает каждое входящее сообщение.
    For each incoming message, update the conversation history,
    store the message for the summary, and optionally respond via Ollama.
    """
    sender = await event.get_sender()

    # Пропускаем сообщения самого бота / Ignore messages from the bot itself
    if sender and sender.is_self:
        return

    # Получаем имя отправителя / Get sender name
    if isinstance(sender, Channel):
        sender_name = getattr(sender, 'title', "Канал без названия")
    else:
        sender_name = (
            sender.username
            if sender and sender.username
            else (sender.first_name if sender and sender.first_name else "Неизвестный")
        )

    # Получаем название чата, если это группа/канал / Get chat title if it's a group/channel
    if event.is_group or event.is_channel:
        chat = await event.get_chat()
        chat_title = getattr(chat, 'title', "Группа/Канал без названия")
    else:
        chat_title = None

    message_text = event.raw_text

    # Добавляем сообщение в буфер для суммаризации
    # Add the message to the summary buffer
    new_messages_buffer.append({
        "dt": datetime.datetime.now(),
        "sender_id": sender.id if sender else 0,
        "sender_name": sender_name,
        "chat_title": chat_title,
        "text": message_text
    })

    # Обновляем историю диалога (если это не канал) / Update conversation history (if not a channel)
    user_id = sender.id if sender else 0
    if not isinstance(sender, Channel):
        user_conversations.setdefault(user_id, []).append(("user", message_text))

    # Если не владелец бота - отвечаем / If not the bot owner, respond
    if user_id != BOT_OWNER_ID:
        response_text = generate_response_for_user(user_id, message_text)
        # Добавляем ответ бота в историю / Add assistant reply to conversation
        user_conversations[user_id].append(("assistant", response_text))
        await event.reply(response_text)


# ------------------------------------------------------------------
# Периодическая задача для сводки / Periodic summary task
# ------------------------------------------------------------------

async def summary_loop():
    """
    Бесконечный цикл, каждые SUMMARY_INTERVAL_SECONDS формируем и отправляем сводку.
    Endless loop: every SUMMARY_INTERVAL_SECONDS we create and send a summary to BOT_OWNER_ID.
    """
    while True:
        await asyncio.sleep(SUMMARY_INTERVAL_SECONDS)

        if not new_messages_buffer:
            logger.info("Нет новых сообщений, сводка не сформирована. / No new messages, no summary.")
            continue

        # Копируем и очищаем буфер / Copy and clear the buffer
        messages_to_summarize = new_messages_buffer.copy()
        new_messages_buffer.clear()

        # Генерируем сводку / Generate summary
        summary_text = summarize_messages_with_ollama(messages_to_summarize)

        # Отправляем сводку владельцу / Send summary to the owner
        try:
            await client.send_message(BOT_OWNER_ID, summary_text)
            logger.info("Сводка отправлена владельцу. / Summary sent to the owner.")
        except Exception as e:
            logger.error(f"Не удалось отправить сводку / Failed to send summary: {e}")


# ------------------------------------------------------------------
# Основная функция / Main function
# ------------------------------------------------------------------

async def main():
    # Запускаем клиента как бот / Start the client as a bot
    await client.start(bot_token=BOT_TOKEN)

    # Запускаем фоновую задачу для периодической сводки / Start the background summary task
    asyncio.create_task(summary_loop())

    logger.info("Бот запущен / Bot started. Waiting for incoming messages...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())

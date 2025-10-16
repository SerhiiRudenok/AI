from django.shortcuts import render
import re
import os
import requests
from django.http import JsonResponse
from dotenv import load_dotenv


# =================================================================
# ||                   ТЕКСТОВИЙ ЧАТ-БОТ                         ||
# =================================================================
def text_chat_bot(user_input: str, context_messages: list) -> str:
    load_dotenv()  # завантажує .env
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise RuntimeError("Відсутній API ключ. Будь ласка, встановіть змінну середовища GROQ_API_KEY.")

    MODEL = "llama-3.3-70b-versatile"
    GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

    system_prompt = (
        "Ти — розумний і доброзичливий український асистент. "
        "Тебе звуть Умка. Відповідай коротко, але по суті, природною українською мовою."
    )

    # формуємо історію діалогу: system + попередні повідомлення + нове
    messages = [{"role": "system", "content": system_prompt}] + context_messages + [
        {"role": "user", "content": user_input}
    ]

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512,
        "stream": False
    }

    try:
        res = requests.post(GROQ_URL, headers=headers, json=payload)
        if res.status_code != 200:
            return "Вибач, сталася помилка при зверненні до Штучного Інтелекту!"
        data = res.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return "Вибач, сталася помилка при зверненні до Штучного Інтелекту!"


# =================================================================
# ||              ГОЛОВНА СТОРІНКА З ЧАТ-БОТОМ                   ||
# =================================================================
def index_page(request):
    # 1. Отримуємо історію з сесії
    if request.method == "POST":
        chat_history = request.session.get("chat_history", [])
        user_input_original = request.POST.get("user_input", "")
        user_input = re.sub(r"\s+", " ", user_input_original).strip()

        # 2. Команда для очищення чату
        if (user_input.lower() == "очистити чат") or (user_input.lower() == "очисти чат"):
            request.session["chat_history"] = []
            return JsonResponse({"cleared": True})

        # 3. Отримуємо відповідь від чат-бота (з контекстом)
        response = text_chat_bot(user_input, chat_history)

        # 4. Зберігаємо історію в сесії
        chat_history.append({"role": "user", "content": user_input_original})
        chat_history.append({"role": "assistant", "content": response})
        request.session["chat_history"] = chat_history
        request.session.modified = True  # оновлюємо сесію


        return JsonResponse({"bot": response})

    request.session["chat_history"] = []
    return render(request, "myapp/index.html", {"chat_history": []})
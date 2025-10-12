from django.shortcuts import render
from datetime import datetime
import pytz  # для роботи з часовими поясами
import random
import re

# Випадкові відповіді
random_responses = [
    # Приказки
    "Не той друг, що медом маже, а той, що правду каже.",
    "Без труда нема плода.",
    "Слово — не горобець, вилетить — не впіймаєш.",
    "Де сила не візьме, там розум допоможе.",

    # Жарти
    "Мозок — це як парашут: працює лише коли відкритий!",
    "Не хвилюйся, якщо щось не працює — можливо, воно просто відпочиває.",
    "Інтернет — це місце, де ти шукаєш одне, а знаходиш меми.",
    "Краще бути оптимістом і помилятись, ніж песимістом і мати рацію.",

    # Філософські цитати
    "Світ змінюється не тими, хто чекає, а тими, хто діє.",
    "Мудрість приходить не з віком, а з досвідом.",
    "Той, хто знає мету — знайде шлях.",
    "Щастя — це не пункт призначення, а спосіб подорожі.",
    "Найдовша дорога починається з першого кроку."
]

# Історія чату
chat_history = {}

def index_page(request):
    if request.method == "POST":
        user_input_original = request.POST.get("user_input", "")
        user_input = re.sub(r"[^\wа-яіїєґ\s]+", "", user_input_original.strip().lower())
        user_input = re.sub(r"\s+", " ", user_input).strip()

        # Київський час
        kyiv_tz = pytz.timezone("Europe/Kyiv")
        now_kyiv = datetime.now(kyiv_tz)

        if user_input == "дата":
            response = now_kyiv.strftime("%d.%m.%Y")
        elif user_input == "час":
            response = now_kyiv.strftime("%H:%M:%S")
        elif user_input == "очистити чат":
            chat_history.clear()
            response = ""
        else:
            last_response = list(chat_history.values())[-1]["bot"] if chat_history else None
            response = random.choice(random_responses)
            while response == last_response:
                response = random.choice(random_responses)

        if user_input != "очистити чат":
            index = len(chat_history)
            chat_history[index] = {
                "user": user_input_original,
                "bot": response
            }

    context = {
        "chat_history": chat_history.values()
    }
    return render(request, "myapp/index.html", context)
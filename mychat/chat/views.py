from django.shortcuts import render
from django.http import JsonResponse

from .models import Message
from .classifier import find_program


def index(request):

    messages = Message.objects.all().order_by("created_at")

    return render(
        request,
        "chat/index.html",
        {"messages": messages}
    )


def send_message(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST only"})

    text = request.POST.get("message")

    Message.objects.create(
        role="user",
        text=text
    )

    program = find_program(text)

    if program:

        bot_reply = f"""
🎓 Подходящая программа

Название: {program.name}

Код специальности: {program.code}

Стоимость: {program.price:,} руб.

Срок обучения: {program.duration}

Будущая профессия:
{program.profession}
"""

    else:

        bot_reply = """
Не удалось подобрать программу.

Попробуйте подробнее описать:
- кем хотите работать
- что вам нравится
- какие предметы интересны
"""

    Message.objects.create(
        role="bot",
        text=bot_reply
    )

    return JsonResponse({
        "user": text,
        "bot": bot_reply
    })

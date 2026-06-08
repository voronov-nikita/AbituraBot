# chat/management/commands/import_programs.py

import csv

from django.core.management.base import BaseCommand
from chat.models import Program


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        with open(r"C:\Users\voron\Desktop\Учеба\4 семестр\курсовая\AbituraBot\mychat\chat\programs.csv", encoding="utf-8") as f:

            reader = csv.DictReader(f)

            for row in reader:

                Program.objects.create(
                    name=row["название программы"],
                    price=row["стоимость обучения"],
                    code=row["код специальности"],
                    duration=row["время обучения"],
                    profession=row["профессия"]
                )
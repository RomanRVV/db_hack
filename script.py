from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid)
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
import random
import sys


def find_schoolkid(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.filter(full_name__contains=schoolkid_name).get()
        return schoolkid
    except MultipleObjectsReturned:
        print(f'С именем {schoolkid_name}, есть сразу несколько учеников, пожалуйста, укажите полное ФИО')
        sys.exit()
    except ObjectDoesNotExist:
        print('Такого ФИО нет в базе данных')
        sys.exit()


def fix_marks(schoolkid_name):
    schoolkid = find_schoolkid(schoolkid_name)
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for bad_mark in bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def remove_chastisements(schoolkid_name):
    schoolkid = find_schoolkid(schoolkid_name)
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid_name, subject):
    schoolkid = find_schoolkid(schoolkid_name)
    commendations = ["Молодец!",
                     "Отлично!",
                     "Хорошо!",
                     "Гораздо лучше, чем я ожидал!",
                     "Ты меня приятно удивил!",
                     "Великолепно!", "Прекрасно!",
                     "Ты меня очень обрадовал!",
                     "Именно этого я давно ждал от тебя!",
                     "Сказано здорово – просто и ясно!",
                     "Ты, как всегда, точен!",
                     "Очень хороший ответ!",
                     "Талантливо!",
                     "Ты сегодня прыгнул выше головы!",
                     "Я поражен!",
                     "Уже существенно лучше!",
                     "Потрясающе!",
                     "Замечательно!",
                     "Прекрасное начало!",
                     "Так держать!",
                     "Ты на верном пути!",
                     "Здорово!",
                     "Это как раз то, что нужно!",
                     "Я тобой горжусь!",
                     "С каждым разом у тебя получается всё лучше!",
                     "Мы с тобой не зря поработали!",
                     "Я вижу, как ты стараешься!",
                     "Ты растешь над собой!",
                     "Ты многое сделал, я это вижу!",
                     "Теперь у тебя точно все получится!"
                     ]
    lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
                                   group_letter=schoolkid.group_letter,
                                   subject__title=subject).order_by("?").first()
    commendation = random.choice(commendations)
    if lesson:
        Commendation.objects.create(text=commendation,
                                    created=lesson.date,
                                    schoolkid=schoolkid,
                                    subject=lesson.subject,
                                    teacher=lesson.teacher)
    else:
        print(f'Предмета {subject} нет в дневнике.\nПроверьте правильность написания предмета')
        sys.exit()

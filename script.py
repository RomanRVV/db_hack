from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid)
import random
import sys


COMMENDATIONS = ["Молодец!",
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


def find_schoolkid(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        return schoolkid
    except Schoolkid.MultipleObjectsReturned:
        print(f'С именем {schoolkid_name}, есть сразу несколько учеников, пожалуйста, укажите полное ФИО')
        sys.exit()
    except Schoolkid.DoesNotExist:
        print('Такого ФИО нет в базе данных')
        sys.exit()


def fix_marks(schoolkid_name):
    schoolkid = find_schoolkid(schoolkid_name)
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid_name):
    schoolkid = find_schoolkid(schoolkid_name)
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid_name, subject):
    schoolkid = find_schoolkid(schoolkid_name)
    lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
                                   group_letter=schoolkid.group_letter,
                                   subject__title=subject).order_by("?").first()
    commendation = random.choice(COMMENDATIONS)
    if lesson:
        Commendation.objects.create(text=commendation,
                                    created=lesson.date,
                                    schoolkid=schoolkid,
                                    subject=lesson.subject,
                                    teacher=lesson.teacher)
    else:
        print(f'Предмета {subject} нет в дневнике.\nПроверьте правильность написания предмета')
        sys.exit()

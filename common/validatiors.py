from datetime import date
from rest_framework.exceptions import ValidationError


def validate_age(birthday):
    if not birthday:
        raise ValidationError('Дата Рождения не указана!')

    if isinstance(birthday, str):
        birthday = date.fromisoformat(birthday)

    today = date.today()
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    if age < 18:
        raise ValidationError('Возраст должен быть не менее 18 лет!')
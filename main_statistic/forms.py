from django import forms


class CalendarForm(forms.Form):
    """
    Форма для вибору дати.

    Цей клас форми використовується для збору дати від користувача
    через поле вводу з типом 'date'.

    Attributes:
        date (forms.DateField): Поле для вибору дати.
    """

    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,  # Поле не є обов'язковим для заповнення
        label="",  # Порожній ярлик, оскільки поле буде відображатися без заголовка
    )

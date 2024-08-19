from django.db import models


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=250,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )
    price = models.IntegerField(
        verbose_name='Стоимость'
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )
    course = models.ForeignKey(
        to='Course',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""
    CHOICES = [('1', '1 group'), ('2', '2 group'), ('3', '3 group'), ('4', '4 group'), ('5', '5 group'),
               ('6', '6 group'), ('7', '7 group'), ('8', '8 group'), ('9', '9 group'), ('10', '10 group'), ]

    course = models.ForeignKey(
        to='Course',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        to='users.CustomUser',
        on_delete=models.CASCADE
    )
    group = models.CharField(
        max_length=4,
        choices=CHOICES
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)

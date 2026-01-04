from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .utilities import get_timestamp_path


# -------------------- Пользователь --------------------

class AdvUser(AbstractUser):
    is_activated = models.BooleanField(
        default=True, db_index=True, verbose_name='Прошел активацию?'
    )
    send_messages = models.BooleanField(
        default=True, verbose_name='Слать оповещения о новых комментариях?'
    )

    subscribed_rubrics = models.ManyToManyField(
        'SubRubric',
        blank=True,
        related_name='subscribers',
        verbose_name='Категории писем'
    )

    def delete(self, *args, **kwargs):

        for bb in self.bb_set.all():
            bb.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


# -------------------- Базовая модель (наследование) --------------------
# поля унаследуются в Bb/Comment.

class BaseContent(models.Model):
    is_active = models.BooleanField(
        default=True, db_index=True, verbose_name='Выводить на экран?'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Опубликовано'
    )

    class Meta:
        abstract = True


# -------------------- Рубрики --------------------

class Rubric(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name='Название')
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name='Порядок')


    super_rubric = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='subrubrics',
        verbose_name='Надрубрика'
    )

    class Meta:
        ordering = ('order', 'name')
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'

    def __str__(self):
        return self.name


class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)


class SuperRubric(Rubric):
    objects = SuperRubricManager()

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Надрубрика'
        verbose_name_plural = 'Надрубрики'


class SubRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)


class SubRubric(Rubric):
    objects = SubRubricManager()

    def __str__(self):
        #  "Надрубрика - Подрубрика"
        return f'{self.super_rubric.name} - {self.name}'

    class Meta:
        proxy = True
        ordering = ('super_rubric__order', 'super_rubric__name', 'order', 'name')
        verbose_name = 'Подрубрика'
        verbose_name_plural = 'Подрубрики'


# -------------------- Объявления --------------------

class Bb(BaseContent):
    rubric = models.ForeignKey(
        SubRubric, on_delete=models.PROTECT, verbose_name='Рубрика'
    )
    title = models.CharField(max_length=40, verbose_name='Товар')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(default=0, verbose_name='Цена')
    contacts = models.TextField(verbose_name='Контакты')

    image = models.ImageField(
        blank=True, upload_to=get_timestamp_path, verbose_name='Изображение'
    )

    author = models.ForeignKey(
        AdvUser, on_delete=models.CASCADE, verbose_name='Автор объявления'
    )

    def delete(self, *args, **kwargs):

        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class AdditionalImage(models.Model):
    bb = models.ForeignKey(
        Bb, on_delete=models.CASCADE, verbose_name='Объявление'
    )
    image = models.ImageField(
        upload_to=get_timestamp_path, verbose_name='Изображение'
    )

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'

    def __str__(self):
        return f'Доп. изображение к: {self.bb_id}'


# -------------------- Комментарии  --------------------
# BaseContent (наследование полей)

class Comment(BaseContent):
    bb = models.ForeignKey(
        Bb, on_delete=models.CASCADE, verbose_name='Объявление', related_name='comments'
    )
    author = models.CharField(max_length=30, verbose_name='Автор')
    content = models.TextField(verbose_name='Содержание')

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author}: {self.content[:30]}'


# -------------------- Полиморфные связи  --------------------
# Универсальный комментарий/заметка, который можно прикрепить К ЛЮБОМУ объекту:
# к Bb, к Rubric, к AdvUser и т.п.

class UniversalComment(BaseContent):

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст')

    # полиморфная ссылка:
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Тип объекта'
    )
    object_id = models.PositiveIntegerField(verbose_name='ID объекта')
    target = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Универсальный комментарий'
        verbose_name_plural = 'Универсальные комментарии'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author}: {self.text[:30]}'
from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Hello(CMSPlugin):
    guest_name = models.CharField(max_length=50, default='Guest')


COMPETITION_TYPE = (
    (1, 'Фотоконкурс'),
    (2, 'Литературный конкурс'),
    (3, 'Видеоконкурс'),
    (4, 'Аудиоконкурс'),
)


class Profile(models.Model):
    """Расширили стандартную пользовательскую модель"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField('номер телефона', max_length=15, null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.get_full_name()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Competition(models.Model):
    """Модель конкурса"""
    title = models.CharField('название конкурса', max_length=100, null=False, blank=False)
    comp_type = models.IntegerField('тип конкурса', default=1, choices=COMPETITION_TYPE)
    start_date = models.DateTimeField('дата и время начала', null=False, blank=False)
    end_date = models.DateTimeField('дата и время окончания', null=False, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_competitions', verbose_name='кем организован')
    is_active = models.BooleanField('активен', default=False)

    class Meta:
        verbose_name = 'Конкурс'
        verbose_name_plural = 'Конкурсы'


class ParticipateRequest(models.Model):
    """Модель заявки на участие"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_requests', verbose_name='пользователь')
    competition = models.ForeignKey('Competition', on_delete=models.CASCADE, related_name='competition_part_requests', verbose_name='конкурс')
    approved = models.BooleanField('одобрено', default=False)
    comment = models.TextField('комментарий')
    content = models.FileField('файл', upload_to='upload/')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Vote(models.Model):
    """Абстрактная модель 'Голос' разрешающая МtM между 'Пользователем' и 'Заявкой' """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes', verbose_name='пользователь')
    request = models.ForeignKey('ParticipateRequest', related_name='participate_votes', verbose_name='заявка')

    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'
        unique_together = ('user', 'request')

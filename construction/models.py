from django.db import models


class Building(models.Model):
    address = models.TextField(
        verbose_name='Адрес',
        blank=False,
        unique=True,
    )

    built = models.IntegerField(
        verbose_name='Год постройки',
        blank=False,
    )

    class Meta:
        db_table = 'construction_buildings'
        verbose_name = 'Строение'
        verbose_name_plural = 'Строение'

    def __str__(self):
        return f'Дом №{self.id} Адрес {self.address} {self.built}'


class Job(models.Model):
    bricks_amount = models.IntegerField(
        verbose_name='Количество кирпичей',
        blank=False,
    )
    execution_time = models.DateTimeField(
        verbose_name='Время выполнения',
        blank=False,
    )
    building = models.ForeignKey(
        Building,
        verbose_name='Строение',
        on_delete=models.CASCADE,
        related_name='jobs',
    )

    class Meta:
        db_table = 'construction_jobs'
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return f'Дом №{self.building.id} {self.bricks_amount} {self.execution_time}'

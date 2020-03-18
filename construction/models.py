from django.db import models


class Building(models.Model):
    address = models.TextField(
        verbose_name='Адрес',
        blank=False,
        unique=True,
    )

    built = models.DateTimeField(
        verbose_name='Дата постройки',
        blank=False,
    )

    class Meta:
        db_table = 'construction_buildings'
        verbose_name = 'Здание'
        verbose_name_plural = 'Здания'

    def __str__(self):
        return f'№{self.id} {self.address} {self.built}'


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
        verbose_name='Здание',
        on_delete=models.CASCADE,
        related_name='jobs',
        null=False,
    )

    class Meta:
        db_table = 'construction_jobs'
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'

    def __str__(self):
        return f'Дом №{self.building.id} {self.bricks_amount} {self.execution_time}'

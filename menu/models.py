from django.db import models

class Dish(models.Model):
    name = models.CharField('料理名', max_length=100)
    last_cooked_date = models.DateField('最後に作った日', null=True, blank=True)
    memo = models.TextField('メモ・ポイント', blank=True)

    def __str__(self):
        return self.name
from django.db import models

class Dish(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, blank=True, default='')  # 空文字を許可
    last_cooked_date = models.DateField(null=True, blank=True)
    memo = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name
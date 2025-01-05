from django.db import models


class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    category = models.CharField(
        max_length=50,
        choices=[
            ('parser', 'Парсер'),
            ('blog', 'Блог'),
            ('general', 'Общие вопросы'),
        ],
        default='general',
        verbose_name="Категория"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQ"


from django.db import models

# Create your models here.

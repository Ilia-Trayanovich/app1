from django.db import models

class ParserStatus(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('running', 'Выполняется'),
        ('completed', 'Завершено'),
        ('failed', 'Ошибка'),
    ]
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    last_run = models.DateTimeField(null=True, blank=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Статус: {self.get_status_display()}, Последний запуск: {self.last_run or 'не запускался'}"

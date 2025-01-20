from django.db import models

class SMScode(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='sms_code')
    sms_code = models.TextField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.sms_code
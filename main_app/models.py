from django.db import models

class Accounts(models.Model):
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=231)
    account_type = models.CharField(max_length=123)
    class Meta:
        #proxy = True
        unique_together = (("email","account_type"))

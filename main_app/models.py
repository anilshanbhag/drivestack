from django.db import models

class Accounts(models.Model):
    id = models.CharField(primary_key=True,max_length=1000)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=231)
    account_type = models.CharField(max_length=123)
    account_data = models.TextField()

    class Meta:
        #proxy = True
        unique_together = (("email","account_type"))

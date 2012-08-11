from django.db import models

class Accounts(models.Model):
    email = models.CharField()
    name = models.CharField()
    account_type = models.CharField()

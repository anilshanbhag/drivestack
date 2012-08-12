from django.db import models

class Accounts(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=231)
    account_type = models.CharField(max_length=123)
    account_data = models.TextField()

    class Meta:
        #proxy = True
        unique_together = (("email","account_type"))

class SharingInfo(models.Model):
    shared_by = models.CharField(max_length=1000)
    shared_with = models.CharField(max_length=1000)
    shared_from_drive = models.CharField(max_length=1000)
    file_path_or_id = models.CharField(max_length=1000)
    file_name = models.CharField(max_length=1000)


       

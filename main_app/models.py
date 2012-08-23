from django.db import models
import datetime

class Accounts(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=231)
    account_type = models.CharField(max_length=123)
    account_data = models.TextField()
    created = models.DateTimeField(editable = False)
    modified = models.DateTimeField()

    class Meta:
        #proxy = True
        unique_together = (("email","account_type"))

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        super(Accounts, self).save(*args, **kwargs)

class SharingInfo(models.Model):
    shared_by = models.CharField(max_length=1000)
    shared_with = models.CharField(max_length=1000)
    shared_from_drive = models.CharField(max_length=1000)
    file_path_or_id = models.CharField(max_length=1000)
    file_name = models.CharField(max_length=1000)


       

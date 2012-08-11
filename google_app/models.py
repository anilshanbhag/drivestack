from django.db import models
class GoogleData(models.Model):
    id = models.CharField(primary_key=True,max_length=1000)
    uid = models.CharField(max_length=400)
    email = models.CharField(max_length=400)

    access_token = models.CharField(max_length=400)
    client_id = models.CharField(max_length=400)
    client_secret = models.CharField(max_length=400)
    refresh_token = models.CharField(max_length=400)
    token_expiry = models.CharField(max_length=400)
    token_uri = models.CharField(max_length=400)
    user_agent = models.CharField(max_length=400)
    id_token = models.TextField(max_length=400)
	

# Create your models here.

from django.shortcuts import render_to_response
from django.http import HttpResponse

def homepage(request):
    # request.session["name"] = "DSADSADSADSAD"
    return render_to_response('index.html')

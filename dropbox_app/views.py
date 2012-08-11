# Create your views here.
from DropBoxClient import DropBoxClient
def dropboxinterface(request, type):
    if type == "register":
        return DropBoxClient.register(request)

        
        

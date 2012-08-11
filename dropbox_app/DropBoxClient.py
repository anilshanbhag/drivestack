# Include the Dropbox SDK libraries
from dropbox import client, rest, session 
from main_app.models import *
APP_KEY = 'nqqr4e3g6fqiugf' 
APP_SECRET= 'ulw7g239slu521p' 
ACCESS_TYPE = 'dropbox' 
class DropBoxClient:
    # Get your app key and secret from the Dropbox developer website
    
    # ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
    def register(self):
        return self.auth()
        
        
    def auth(self):

        self.sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
        request_token = self.sess.obtain_request_token()
        url = self.sess.build_authorize_url(request_token)
        
        # Make the user sign in and authorize this token
        return url+'&oauth_callback=http%3A%2F%2Fwncc.webfactional.com%2Fdropbox%2Foauthcallback'
        """
        print "url:", url
        print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
        raw_input()
        
        # This will fail if the user didn't visit the above URL and hit 'Allow'
        access_token = sess.obtain_access_token(request_token)
        self.client = client.DropboxClient(sess)
        return """

    def store_access_token(self):
        access_token = self.sess.obtain_access_token(request_token)
        self.client = client.DropboxClient(self.sess)
        return client.account_info()
        #TODO : Return client email,Name,Access info print "linked account:", client.account_info()
        #accounts(
        #return true
        

    def attach_cloud(self,access_token,access_token_secret):
        sess.set_token(access_token,access_token_secret)
        self.client = client.DropboxClient(self.sess)
        return true

    def upload(self,file_name):
        response = client.put_file(file_name, f)
        return true

    def download(self,file_name):
        f, metadata = client.get_file_and_metadata(file_name).read()
        out = open(file_name, 'w')
        out.write(f.read())
        print(metadata)
        return true

        
    


        

    

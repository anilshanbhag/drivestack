# Include the Dropbox SDK libraries
from dropbox import client, rest, session

class DropBoxClient:
	# Get your app key and secret from the Dropbox developer website
	APP_KEY = 'INSERT_APP_KEY_HERE'
	APP_SECRET = 'INSERT_SECRET_HERE'
	
	# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
	ACCESS_TYPE = 'INSERT_ACCESS_TYPE_HERE'
	def register(self):
		registered = auth()
		#TODO : Return client email,Name,Access info
		print "linked account:", client.account_info()
		
		
	def auth(self):
		sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
		request_token = sess.obtain_request_token()
		url = sess.build_authorize_url(request_token)
		
		# Make the user sign in and authorize this token
		print "url:", url
		print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
		raw_input()
		
		# This will fail if the user didn't visit the above URL and hit 'Allow'
		access_token = sess.obtain_access_token(request_token)
		self.client = client.DropboxClient(sess)
		return 

	def attach_cloud(self,access_token,access_token_secret):
		sess.set_token(access_token,access_token_secret)
		self.client = client.DropboxClient(sess)
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

		
	


		

	

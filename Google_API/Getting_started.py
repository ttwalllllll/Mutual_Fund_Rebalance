from Google import Create_Service

CLIENT_SECRET_FILE = 'client_secret_file.json'
API_SERVICE_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

service.users().getProfile(userID='me').execute()




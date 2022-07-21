from email.mime.message import MIMEMessage
from Google_API.Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
sys.path.append("Rebalance_Qtr.py")
import Rebalance_Qtr as reb
from email.mime.base import MIMEBase
from email import encoders

CLIENT_SECRET_FILE = 'Token_Files/client_secret_file.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']


service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


msg = MIMEMultipart()
mail_content = "Attached are the mutual funds that need to be rebalanced."
msg['to'] = 'tyler.wallace@nm.com, logan.michaels@nm.com'
msg['subject'] = 'Rebalance Notification - Mutual Funds Out of Range'
#The body and the attachments for the mail
pdfname1 = 'Graphs.pdf'
pdfname2 = 'Dataframe.pdf'

# open the file in bynary
binary_pdf_1 = open(pdfname1, 'rb')
binary_pdf_2 = open(pdfname2, 'rb')

payload1 = MIMEBase('application', 'octate-stream', Name=pdfname1)
payload1.set_payload((binary_pdf_1).read())

payload2 = MIMEBase('application', 'octate-stream', Name=pdfname2)
payload2.set_payload((binary_pdf_2).read())

# enconding the binary into base64
encoders.encode_base64(payload1)
# enconding the binary into base64
encoders.encode_base64(payload2)

# add header with pdf name
payload1.add_header('Content-Decomposition', 'attachment', filename=pdfname1)
msg.attach(payload1)

# add header with pdf name
payload2.add_header('Content-Decomposition', 'attachment', filename=pdfname2)
msg.attach(payload2)

raw_string = base64.urlsafe_b64encode(msg.as_bytes()).decode()

message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
print(message)
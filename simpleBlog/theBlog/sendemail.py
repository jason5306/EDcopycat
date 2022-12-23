from django.template import loader
from django.conf import settings
from django.core.mail import EmailMessage
import threading

class SendHtmlEmail(threading.Thread):
    """send html email"""
    def __init__(self, subject, html_content, send_from, to_list, fail_silently = False):
        self.subject = subject
        self.html_content = html_content
        self.send_from = send_from
        self.to_list = to_list
        self.fail_silently = fail_silently 
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, self.send_from, self.to_list)
        msg.content_subtype = "html" # Main content is now text/html
        msg.send(self.fail_silently)
        print(self.subject + ' has been sent to ' + str(self.to_list))

def send_email_by_template(subject, module, data, to_list):
    """
        subject: string, subject
        module:  string, template name
        data:    dict,   context data
        to_list: list,   mailing list
    """
    html_content = loader.render_to_string(module, data)
    send_from = settings.DEFAULT_FROM_EMAIL

    send_email = SendHtmlEmail(subject, html_content, send_from, to_list)
    send_email.start() # start thread
    

def send_html_email(subject, html_content, to_list):
    """send html format email"""
    send_from = settings.DEFAULT_FROM_EMAIL
    send_email = SendHtmlEmail(subject, html_content, send_from, to_list)
    send_email.start()

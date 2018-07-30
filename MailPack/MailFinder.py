from utils.CosineTextDist import cosine_dist
from email.parser import Parser
from utils.encryption import *
import datetime
import imaplib
import email
import re


class MailRunner:
    imaps = ['imap.gmail.com', 'imap.yandex.ru']

    def __init__(self, cred, imap=imaps[0], port=imaplib.IMAP4_SSL_PORT):
        """
        Initializes MailRunner class
        :param cred: tuple -> (email -> str, pass -> str)
        :param imap: int or str -> int for predeclared imaps(MailRunner.imaps); str for imap address
        :param port: SSL port of imap (default: 993)
        """
        self.mail = None
        self.cred = cred
        self.imap = MailRunner.imaps[imap] if type(imap) == int else imap
        self.port = port

    def init(self):
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap, self.port)
            self.mail.login(*self.cred)
            self.mail.list()
            self.mail.select("inbox")  # Open folder "INBOX"
        except Exception as ex:
            return ex
        return None

    def get_emails(self, cb, flt="ALL"):
        """
        Process all emails from inbox using flt as filter
        :param cb: Function to verify each email
        :param flt: str -> IMAP filter
        :return: list -> results of running %cb% on each mail
        """
        result, data = self.mail.uid('search', None, flt)  # List all emails by filter
        data = data[0].split()  # Some magic

        xres = []
        for uid in data:
            res = MailRunner.procmail(self.mail, uid)  # Preprocess each mail
            res = cb(res) if cb else res  # Try to run Postprocess function
            xres.append(res)
        return xres

    @staticmethod
    def procmail(m, u):
        """
        Preprocess each mail
        :param m: mail object (self.mail in MailRunner)
        :param u: int -> email uid
        :return: dict
        """
        result, data = m.uid('fetch', u, '(RFC822)')  # Load email by UID
        raw_email = data[0][1]
        try:
            email_message = email.message_from_string(raw_email.decode('utf-8'))  # Decode raw email to Message object

            subj, txt = email.header.decode_header(
                email_message.get('Subject', '<>')), '<>'  # Extract & decode mail subject
            if len(subj) > 0:
                subj = subj[0][0] if type(subj[0][0]) == str else subj[0][0].decode(subj[0][1] or 'utf-8')  # Some magic
                txt = MailRunner.decode_email(raw_email.decode())  # Decode mail body

            date = email_message.get("Date", '<>')

            return {"err": "NA",
                    "date": re.findall('^.*\d+:\d+:\d+', date)[0],  # Data when email was received
                    "subj": subj,  # Subj of email
                    "body": txt,  # email text
                    "to": email_message.get('Delivered-To', '<>'),
                    "from": email.utils.parseaddr(email_message['From'])[1]}
        except UnicodeDecodeError:  # email has non-utf8 symbols
            return {"err": "UDE"}

    @staticmethod
    def decode_email(msg_str):
        """
        Decode mail body
        :param msg_str: mail body
        :return: decoded mail body
        """
        p = Parser()
        message = p.parsestr(msg_str)
        decoded_message = ''
        for part in message.walk():
            charset = part.get_content_charset()
            if part.get_content_type() == 'text/plain':
                part_str = part.get_payload(decode=1)
                decoded_message += part_str.decode(charset)
        return decoded_message


def find(data, cb):
    result = []

    udata = get_cred()
    if not udata['data'] or (udata['data'] and not udata['mail']):
        cb.toast_red("Ошибка анализа почты", "Параметры почты не настроены в разделе НАСТРОЙКИ")
        return result

    mr = MailRunner(udata['cred'], imap=udata['imaphost'], port=udata['imapport'])

    preres = mr.init()
    if preres:
        cb.toast_red("Ошибка анализа почты", "Параметры почты неверны (imap/email/pass)")
    else:
        modifsince = int(get_cred()['mailtime'] or 14)
        date = (datetime.date.today() - datetime.timedelta(modifsince)).strftime(
            "%d-%b-%Y")  # In timedelta choose amount of days ago, one week .

        mails = mr.get_emails(None, '(SINCE {date})'.format(
            date=date))  # Get all emails sorted for data

        for mail in mails:

            if mail['err'] != 'NA':
                continue

            if mail['from'] in data['email'] or \
                    any(filter(lambda x: x > 0.8, map(lambda x: cosine_dist(x, mail['body']), data['text']))):
                result.append({'from': mail['from'], 'date': mail['date'],
                               'subj': mail['subj']})  # Check FROM and TEXT in data from bulletin
                cb.log('Дата получения: {} с темой: {} Исходило от: {}'.format(mail['date'], mail['subj'], mail['from']))
    return result

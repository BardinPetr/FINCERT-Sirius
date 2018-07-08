from multiprocessing import Pool
from pprint import pprint as pp
from email.parser import Parser
import imaplib
import email
import datetime
import pytz
import tzlocal
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
        self.mail = imaplib.IMAP4_SSL(MailRunner.imaps[imap] if type(imap) == int else imap, port)
        self.mail.login(*cred)
        self.mail.list()
        self.mail.select("inbox")  # Open folder "INBOX"

    def get_emails(self, cb, flt="ALL"):
        """
        Process all emails from inbox using flt as filter
        :param cb: Function to verify each email
        :param flt: str -> IMAP filter
        :return: list -> results of running %cb% on each mail
        """
        result, data = self.mail.uid('search', None, flt)  # List all emails by filter
        data = data[0].split()  # Some magic

        # data = (data[::-1])[:10]  # Debug ONLY! --- get 10 first emails

        # pool = Pool(processes=3)
        # res = pool.map(lambda x: MailRunner.procmail(self.mail, x), data)

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
        email_message = email.message_from_string(raw_email.decode('utf-8'))  # Decode raw email to Message object

        subj, txt = email.header.decode_header(
            email_message.get('Subject', '<>')), '<>'  # Extract & decode mail subject
        if len(subj) > 0:
            try:
                subj = subj[0][0] if subj[0][1] is None else subj[0][0].decode(subj[0][1])  # Some magic
                txt = MailRunner.decode_email(raw_email.decode())  # Decode mail body
            except UnicodeDecodeError:  # email has non-utf8 symbols
                return {"err": "UDE"}
        # print(email_message.keys())

        date = email_message.get("Date", '<>')
        if date.find('(') != -1:
            datetime_object = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z (%Z)')
        else:
            datetime_object = datetime.datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %z')

        return {"err": "NA",
                "date": datetime_object,
                "subj": subj,
                "body": txt,
                "to": email_message.get('Delivered-To', '<>'),
                "from": email.utils.parseaddr(email_message['From'])[1]}

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
    local_timezone = tzlocal.get_localzone()

    # mr = MailRunner(("", ""))
    mr = MailRunner((input("Your Gmail addr: "), input("Your Gmail pass: ")))
    # mr.get_emails(None, '(HEADER Received "no-reply@accounts.google.com")')
    # return mr.get_emails(None)

    date = (datetime.date.today() - datetime.timedelta(14)).strftime("%d-%b-%Y")

    # print(date)
    # print(local_timezone)
    mails = mr.get_emails(None, '(SENTSINCE {date})'.format(
        date=date))
    result = []

    for mail in mails:
        if mail['from'] in data['emails']:
            result.append({'from': mail['from'], 'date': mail['date']})

    return mails


# Sun, 8 Jul 2018 07:33:39 +0000 (UTC)

if __name__ == '__main__':
    pp(find({}, None))

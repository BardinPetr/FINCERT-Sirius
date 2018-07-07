from pprint import pprint as pp
import urllib
import imaplib
import base64
import email


class MailRunner:
    imaps = ['imap.gmail.com', 'imap.yandex.ru']

    def __init__(self, imap, cred):
        self.mail = imaplib.IMAP4_SSL(MailRunner.imaps[imap] if type(imap) == int else imap)
        self.mail.login(*cred)
        self.mail.list()
        self.mail.select("inbox")

    def get_emails(self, cb, flt="ALL"):
        result, data = self.mail.uid('search', None, flt)

        data = data[0].split()[:50:-1]

        for uid in data:
            result, data = self.mail.uid('fetch', uid, '(RFC822)')
            raw_email = data[0][1]
            email_message = email.message_from_string(raw_email.decode('utf-8'))

            subj = email.header.decode_header(email_message.get('Subject', '<>'))[0]
            subj =
            subj = urllib.unquote(subj).decode('utf8')

            res = {"to": email_message.get('Delivered-To', '<>'),
                   "from": email.utils.parseaddr(email_message['From'])[1],
                   "subj": subj[0].decode(subj[1]) if subj[1] is not None else "<>",
                   "body": MailRunner.get_first_text_block(email_message)}
            pp(res)

    @staticmethod
    def get_first_text_block(email_message_instance):
        maintype = email_message_instance.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif maintype == 'text':
            return email_message_instance.get_payload()


def find(data, cb):
    mr = MailRunner(0, ("mail", "pass"))
    mr.get_emails(None)


if __name__ == '__main__':
    find({}, None)

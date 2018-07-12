import datetime

from .message import Message
from .utf import encode as encode_utf7, decode as decode_utf7


class Mailbox:

    def __init__(self, gmail, name="INBOX"):
        self.name = name
        self.gmail = gmail
        self.date_format = "%d-%b-%Y"
        self._messages = {}

    def __repr__(self):
        return '<Mailbox {}>'.format(self.external_name)

    @property
    def messages(self):
        return self._messages or self.get_mail()

    @property
    def external_name(self):
        if "external_name" not in vars(self):
            vars(self)["external_name"] = encode_utf7(self.name)
        return vars(self)["external_name"]

    @external_name.setter
    def external_name(self, value):
        if "external_name" in vars(self):
            del vars(self)["external_name"]
        self.name = decode_utf7(value)

    def get_mail(self,
                 **kwargs):

        search = ['ALL']

        kwargs.get('read') and search.append('SEEN')
        kwargs.get('unread') and search.append('UNSEEN')

        kwargs.get('starred') and search.append('FLAGGED')
        kwargs.get('unstarred') and search.append('UNFLAGGED')

        kwargs.get('deleted') and search.append('DELETED')
        kwargs.get('undeleted') and search.append('UNDELETED')

        kwargs.get('draft') and search.append('DRAFT')
        kwargs.get('undraft') and search.append('UNDRAFT')

        kwargs.get('header') and search.extend(
            ['HEADER', kwargs.get('header')[0], kwargs.get('header')[1]])

        kwargs.get('sender') and search.extend(['FROM', kwargs.get('sender')])
        kwargs.get('fr') and search.extend(['FROM', kwargs.get('fr')])
        kwargs.get('from') and search.extend(['FROM', kwargs.get('from')])
        kwargs.get('not_from') and search.extend(['NOT FROM', kwargs.get('not_from')])
        kwargs.get('to') and search.extend(['TO', kwargs.get('to')])
        kwargs.get('cc') and search.extend(['CC', kwargs.get('cc')])

        kwargs.get('subject') and search.extend(
            ['SUBJECT', kwargs.get('subject')])
        kwargs.get('body') and search.extend(['BODY', kwargs.get('body')])

        kwargs.get('label') and search.extend(
            ['X-GM-LABELS', kwargs.get('label')])

        kwargs.get('query') and search.extend(
            ['X-GM-RAW', kwargs.get('query')])

        if 'on' in kwargs and isinstance(kwargs['on'], datetime.datetime):
            kwargs['on'] = kwargs['on'].date()
        if 'before' in kwargs and isinstance(kwargs['before'], datetime.datetime):
            kwargs['before'] = kwargs['before'].date()
        if 'after' in kwargs and isinstance(kwargs['after'], datetime.datetime):
            kwargs['after'] = kwargs['after'].date()

        kwargs.get('before') and search.extend(
            ['BEFORE', kwargs.get('before').strftime(self.date_format)])

        kwargs.get('after') and search.extend(
            ['SINCE', kwargs.get('after').strftime(self.date_format)])

        kwargs.get('on') and search.extend(
            ['ON', kwargs.get('on').strftime(self.date_format)])


        kwargs.get('uid') and search.extend(['UID', kwargs['uid']])

        emails = []

        response, data = self.gmail.imap.uid('SEARCH', *search)
        if response == 'OK':

            # filter out empty strings
            uids = [_f
                    for _f in data[0].split(b' ')
                    if _f]

            for uid in uids:
                if uid not in self._messages:
                    self._messages[uid] = Message(self, uid)
                emails.append(self._messages[uid])

        return emails

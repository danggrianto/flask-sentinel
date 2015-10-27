import os

import mandrill


def send_email(message):
    mandrill_key = os.getenv('MANDRILL_API_KEY')
    if mandrill_key:
        client = mandrill.Mandrill(mandrill_key)
        try:
            client.messages.send(message=message, async=True)
        except mandrill.Error, e:
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
            raise

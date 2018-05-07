# GMail for Python

A Pythonic interface to Google's GMail, with all the tools you'll need. Search, 
read and send multipart emails, archive, mark as read/unread, delete emails, 
and manage labels.

__This library is still under development, so please forgive some of the rough edges__

Heavily inspired by [Kriss "nu7hatch" Kowalik's GMail for Ruby library](https://github.com/nu7hatch/gmail)

## Author

* [Charlie Guo](https://github.com/charlierguo)
* [Girish Ramnani](https://github.com/girishramnani)

## Installation

For now, installation is manual (`pip` support not yet implemented). Supports python 2 and pypy.
`pip` compatible distribution files can be built on your machine with `python setup.py sdist` 


```

git clone git://github.com/girishramnani/gmail.git

```

## Features

* Search emails
* Read emails 
* Emails: label, archive, delete, mark as read/unread/spam, star
* Manage labels

## Basic usage

To start, import the `gmail` library.

    import gmail
    
### Authenticating gmail sessions

To easily get up and running:

    import gmail 

    g = gmail.login(username, password)

Which will automatically log you into a GMail account. 
This is actually a shortcut for creating a new Gmail object:
    
    from gmail import Gmail

    g = Gmail()
    g.login(username, password)
    # play with your gmail...
    g.logout()

You can also check if you are logged in at any time:

    g = gmail.login(username, password)
    g.logged_in # Should be True, AuthenticationError if login fails

### Sending email 

    from gmail import Gmail, Message
    g = Gmail()
    g.login(username, password)

    message = Message.create("Hello",
                             "test@test.com",
                             text="Hello world")
    g.send(message)



### OAuth authentication 

If you have already received an [OAuth2 access token from Google](https://developers.google.com/accounts/docs/OAuth2) for a given user, you can easily log the user in. (Because OAuth 1.0 usage was deprecated in April 2012, this library does not currently support its usage)

    gmail = gmail.authenticate(username, access_token)

### Filtering emails
    
Get all messages in your inbox:

    g.inbox.get_mail()

Get messages that fit some criteria:

    g.inbox.get_mail(after=datetime.date(2013, 6, 18), before=datetime.date(2013, 8, 3))
    g.inbox.get_mail(on=datetime.date(2009, 1, 1)
    g.inbox.get_mail(sender="myfriend@gmail.com") # "from" is reserved, use "fr" or "sender"
    g.inbox.get_mail(to="directlytome@gmail.com")

Combine flags and options:

    g.inbox.get_mail(unread=True, sender="myboss@gmail.com")
    
Browsing labeled emails is similar to working with your inbox.

    g.get_mailbox('Urgent').get_mail()
    
Every message in a conversation/thread will come as a separate message.

    g.inbox.get_mail(unread=True,
                     before=datetime.date(2013, 8, 3),
                     sender="myboss@gmail.com")
    
### Working with emails

Mark news past a certain date as read and archive it:

    emails = g.inbox.get_mail(before=datetime.date(2013, 4, 18),
                              sender="news@nbcnews.com")
    for email in emails:
        email.read() # see other Message methods below
        email.archive()

Delete all emails from a certain person:

    emails = g.inbox.get_mail(sender="junkmail@gmail.com")
    for email in emails:
        email.delete()
     
You can use also `get_label` method instead of `get_mailbox`:

    g.get_label("Faxes").get_mail()

Add a label to a message:

    email.add_label("Faxes")

Download message attachments:

    for attachment in email.attachments:
        print 'Saving attachment: ' + attachment.name
        print 'Size: ' + str(attachment.size) + ' KB'
        attachment.save('attachments/' + attachment.name)
    
There are also few shortcuts to mark messages quickly:

    email.read()
    email.mark_as_read() # alias of email.read()
    email.unread()
    email.mark_as_unread() # alias of email.unread()
    email.spam()
    email.star()
    email.unstar()


### Significant API changes in May 2018

* Mailboxes are now accessed via properties (e.g. `inbox = g.inbox` instead of `g.inbox()`) rather than methods.
* For clarity, the `Mailbox.mail()` method is now called `Mailbox.get_mail()` to emphasize that it's a method, not a property.
* Similarly, `Mailbox.label()` is now `Mailbox.get_label()`.
* `uid` is now supported as a keyword argument for `Mailbox.get_mail()`.


### Roadmap

* Write tests
* Better label support
* Moving between labels/mailboxes
* Intuitive thread fetching & manipulation
* solve issues on the python 3 part ( as it was generated using `2to3` script )
* ~~Sending via Google's SMTP servers (for now, check out https://github.com/paulchakravarti/gmail-sender)~~

## Copyright

* Copyright (c) 2017 Girish Ramnani

See LICENSE for details.


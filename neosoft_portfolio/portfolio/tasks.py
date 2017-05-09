from celery import task
from portfolio.models import Feed
from rssfeed_weekly import RssReader
from django.core.mail import send_mail

@task()
def send_mail_weekly():
    try:	
        feed = Feed.objects.all()
    except Exception as e:
        print(e)
    email_list = []
    if feed :
        for i in feed:
            email_list.append(i.mail)
    rss_reader = RssReader()
    message = 'Your XML Feed are'
    title = rss_reader.text()
    send = send_mail(subject='XML Feed',
                          message='{}'.format(str(message)),
                          from_email='noreply@portfolio.com',
                          recipient_list = email_list,
                          fail_silently = False,
                          html_message = title)
    
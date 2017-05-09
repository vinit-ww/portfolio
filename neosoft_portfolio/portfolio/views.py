from django.template import RequestContext
from django.views.generic import View
from django.core.urlresolvers import resolve
from django.shortcuts import render, get_object_or_404, redirect
from portfolio.models import Project, Technology, ProjectImage,Feed
from django.http import HttpResponse
import urllib
from django.core.mail import send_mail
from rssfeed_weekly import RssReader
import base64
import traceback
from django.contrib import messages

def comment(request, pid=None):
    project = get_object_or_404(Project, **{'id': pid})
    text = '<strong>User :</strong> {} <p>'.format(project.name) + '</p>'
    text += '<strong>Comment :</strong> {} <p>'.format(project.description)+ '</p>'
    return HttpResponse(text)



# Create your views here.
class IndexView(View):
    """
    """
    def get(self, request):
        projects = Project.objects.filter(is_active=True)
        tech_list = Technology.objects.all()
        data = {'projects': projects, 'tech_list': tech_list}
        return render(request, 'pages/index.html', data)

class ProjectDetailsView(View):
    """
    """

    def get(self, request, pid):

        project = get_object_or_404(Project, **{'id': pid})
        return render(request, "pages/project_details.html", {'project': project})

def subscribe_feed(request,data=None):
    email_unicode=None
    email_list = []
    if request.method == 'POST':
        email_unicode = request.POST.get("email")
        name = request.POST.get("firstName") 
        email_list.append('{}'.format(email_unicode)) #convert unicode to string
        data_encoded = base64.b64encode(email_list[0])
        try: 
            feed = Feed(mail=email_list[0],name=name)
            feed.save()
        except Exception as e:
            traceback.print_exc(e)

        url_confirm = '<a href="localhost:8000/feed/?data={}">Confirmation</a>'.format(data_encoded)
        messages.success(request,"A Subscription mail has been send to Your email id", extra_tags='html_safe')
        send = send_mail(subject='Confirmation',
                  message='',
                  from_email='noreply@portfolio.com',
                  recipient_list = email_list,
                  fail_silently = False,
                  html_message = url_confirm)
        
    if request.method == 'GET':
        try:
            data_encoded = request.GET.get("data")
            data_decoded = base64.b64decode(str(data_encoded))
            confirmed = Feed.objects.get(mail=data_decoded)
            email_unicode = confirmed.mail
            email_string = '{}'.format(email_unicode)
            if data_decoded and confirmed:
                rss_reader = RssReader()
                title = rss_reader.text()
                send_mail(subject='XML Feed',
                          message='{}'.format(str(title)),
                          from_email='noreply@portfolio.com',
                          recipient_list = [email_string],
                          fail_silently = False,
                          html_message = title)
                return redirect('index')
        except Exception as e:
            traceback.print_exc(e)
    return redirect('index')

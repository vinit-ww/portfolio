from django.contrib.syndication.views import Feed
from portfolio.models import Project
from django.core.urlresolvers import reverse

class ArticlesFeed(Feed):
  title= "Portfolio"
  link = ""
  description_template = "feed/articles.html"

  def items(self):
      return Project.objects.order_by('-created_date')[:5]

  def item_title(self, item):
      return item.name

  def item_link(self, item):
      return reverse('comment',kwargs = {'pid':item.pk})

  def get_context_data(self, **kwargs):
      context = super(ArticlesFeed, self).get_context_data(**kwargs)
      context['foo'] = 'bar'
      return context


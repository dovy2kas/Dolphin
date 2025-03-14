from django.http import HttpResponse
from django.template import loader

def panel(request):
  template = loader.get_template('panel.html')
  return HttpResponse(template.render())
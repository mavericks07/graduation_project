from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
# Create your views here.


def buy(request):
    template = loader.get_template('buy.html')
    return HttpResponse(template.render())


def consumble(request):
    template = loader.get_template('consumable.html')
    return HttpResponse(template.render())


def self(request):
    template = loader.get_template('self.html')
    return HttpResponse(template.render())

# def classification(request):
#     template = loader.get_template('consumble/classification.html')
#     return HttpResponse(template.render())

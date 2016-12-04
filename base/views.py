from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader


def main(request):
    template = loader.get_template('base.html')
    return HttpResponse(template.render())


def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())


def buy(request):
    template = loader.get_template('buy.html')
    return HttpResponse(template.render())

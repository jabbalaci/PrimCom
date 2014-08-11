# global / local  urls.py
from django.conf.urls import patterns, include, url

# local views.py
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.template.loader import render_to_string

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, JsonResponse

def respond(request):

    return HttpResponse("Hello")

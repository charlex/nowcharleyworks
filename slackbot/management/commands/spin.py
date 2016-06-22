#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import html5lib
from twython import Twython
from bs4 import BeautifulSoup
from django.conf import settings
from fuzzywuzzy import fuzz, process
from django.utils.text import slugify
from rockbot import spotify_conn, twitter_conn
from django.core.management.base import BaseCommand
from django.template.defaultfilters import truncatechars

class Command(BaseCommand):
    help = "Takes a word from Urban Dictionary, searches it on Spotify then \
Tweets the two out"

    def handle(self, *args, **options):
        response = requests.post("https://pozzad-text-spinner.p.mashape.com/textspinner/spin",
          headers={
            "X-Mashape-Key": "qEgnkvwWh4mshIfmA0n6zAbMPOjjp1Tlf7VjsntSR4MBqEosIl",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
          },
          params={
            "text": "\
The day I turned {{5|12|18|21|30|40|55|92}} years old was \
the best birthday of my {{fucking|amazing|underwhelming|unscrupulous}} life!",
            "variationsNum": 50
          }
        )

        print response.status_code
        print response.content

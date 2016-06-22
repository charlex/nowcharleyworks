#!/usr/bin/env python
# -*- coding: utf-8 -*-

import clipboard
import json
import requests
import html5lib
from random import randint
from twython import Twython
from bs4 import BeautifulSoup
from django.conf import settings
from pyfiglet import figlet_format
from fuzzywuzzy import fuzz, process
from django.utils.text import slugify
from rockbot import spotify_conn, twitter_conn
from django.core.management.base import BaseCommand
from django.template.defaultfilters import truncatechars
from StringIO import StringIO
import urllib
from PIL import Image

class Command(BaseCommand):
    help = "Takes a word from Urban Dictionary, searches it on Spotify then \
Tweets the two out"

    def add_arguments(self, parser):
        parser.add_argument('--pk', type=str, nargs="?", default=None)


    def handle(self, *args, **options):
        print "Opening pokedex..."
        if options['pk']:
            pk = int(options['pk'])
        else:
            pk = randint(0,400)

        print pk

        response = requests.get("https://phalt-pokeapi.p.mashape.com/pokemon/%s/" % pk,
            headers={
                "X-Mashape-Key": "qEgnkvwWh4mshIfmA0n6zAbMPOjjp1Tlf7VjsntSR4MBqEosIl",
                "Accept": "application/json"
            }
        )
        pokemon = json.loads(response.content)
        urban = self.get_urban_dictionary_word(pokemon["name"])

        print ""
        print figlet_format(pokemon["name"], font="big")
        if urban["definition"]:
            print "--------------------------------------------------------------------------------"
            print urban["definition"]
            print ""
        print "%s" % urban["url"]

        if urban["photo"]:
            print urban["photo"]
            photo = StringIO(urllib.urlopen(urban["photo"]).read())
            print photo
            response = twitter_conn.upload_media(media=photo)
            twitter_conn.update_status(status=pokemon["name"], media_ids=[response['media_id']])


    def get_urban_dictionary_word(self, term):
        url = "http://www.urbandictionary.com/define.php?term=%s" % term
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        word = soup.title.text[18:]

        try:
            definition = soup.findAll(attrs={"property":"og:description"})[0]["content"]
        except IndexError:
            definition = None

        try:
            url = soup.findAll(attrs={"rel":"canonical"})[0]["href"]
        except IndexError:
            url = None

        try:
            photo = soup.findAll(attrs={"property":"og:image"})[0]["content"]
            print photo
        except IndexError:
            photo = None

        print photo

        return {
            "word": word,
            "definition": definition,
            "url": url,
            "photo": photo
        }

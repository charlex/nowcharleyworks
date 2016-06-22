#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import clipboard
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
        urban = self.get_urban_dictionary_word()
        search_word = urban["word"]
        url = urban["url"]

        search_results = spotify_conn.search(
            q="track:%s" % urban["word"],
            limit=20
        )

        if len(search_results["tracks"]["items"]) == 0:
            # tweet = u"\U0001F4A9 \U0000201C there are no songs for \"%s\" %s" % (
            tweet = u"\u201C%s\u201D is up for grabs on @spotify... just in case you were looking for a song name. %s \u266A" % (
                urban["word"],
                urban["url"]
            )
            print "Tweeting..."
            print tweet
            # twitter_conn.update_status(status=tweet)
            clipboard.copy(tweet)
            return None

        # Get the closest track from the spotify search
        for track in search_results["tracks"]["items"]:
            ratio = fuzz.ratio(urban["word"], track["name"])
            track["match"] = ratio
        closest_track = max(search_results["tracks"]["items"], key=lambda item: item["match"])

        # Get the artist's twitter handle
        user_search = twitter_conn.search_users(
            q="Amateur musician",
            count=20
        )
        if len(user_search) > 0:
            print random.choice(user_search)

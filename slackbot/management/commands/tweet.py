#!/usr/bin/env python
# -*- coding: utf-8 -*-
import clipboard
from rockbot.tweet import get_tweet
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Takes a word from Urban Dictionary, searches it on Spotify then \
Tweets the two out"

    def handle(self, *args, **options):
        tweet = get_tweet()
        clipboard.copy(tweet)

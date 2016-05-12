#!/usr/bin/env python
# -*- coding: utf-8 -*-

import clipboard
import random
import requests
import pprint
import spotipy
import html5lib
from twython import Twython
from bs4 import BeautifulSoup
from django.shortcuts import render
from fuzzywuzzy import fuzz, process
from django.utils.text import slugify
from rockbot import spotify_conn, twitter_conn
from django.template.defaultfilters import truncatechars

def rockbot(request):
    """
    A homepage that lists all the liveblogs.
    """
    urban = get_urban_dictionary_word()
    search_word = urban["word"]
    url = urban["url"]

    search_results = spotify_conn.search(
        q="track:%s" % urban["word"],
        limit=20
    )

    if len(search_results["tracks"]["items"]) == 0:
        amateurs = twitter_conn.search_users(
            q="Amateur musician",
            count=20,
            page=2
        )
        if len(amateurs) > 0:
            amateur = random.choice(amateurs)
            amateur_username = "@%s" % amateur["screen_name"].strip()
        else:
            amateur_username = "someone"

        tweet = u"\u201C%s\u201D is up for grabs on @spotify... just in case %s is looking for a song name. %s \u266A" % (
            urban["word"],
            amateur_username,
            urban["url"]
        )
        print "Tweeting..."
        print tweet
        # twitter_conn.update_status(status=tweet)
        clipboard.copy(tweet)
        context = {
            "tweet": tweet
        }
        return render(request, 'rockbot/rockbot.html', context)

    # Get the closest track from the spotify search
    for track in search_results["tracks"]["items"]:
        ratio = fuzz.ratio(urban["word"], track["name"])
        track["match"] = ratio
    closest_track = max(search_results["tracks"]["items"], key=lambda item: item["match"])

    # spotify_conn.user_playlist_add_tracks("charlex815", "3GO8Uym5sThMEmtFBsgoKr", closest_track["id"])


    # Get the artist's twitter handle
    user_search = twitter_conn.search_users(
        q=closest_track["artists"][0]["name"],
    )
    if len(user_search) > 0:
        username = user_search[0]["screen_name"].strip()
    else:
        username = slugify(closest_track["artists"][0]["name"]).replace("-", "").strip()

    hashtag = slugify(urban["word"]).replace("-", "").strip()

    space_left = 140 - (len(urban["word"]) + len(username) + 55)

    urban["definition"] = truncatechars(urban["definition"].strip(), space_left)

    tweet = u"%s: %s @%s %s %s" % (
        urban["word"],
        u"\U0000201C%s\U0000201D" % urban["definition"].replace('"',"'").replace("\n", "").strip(),
        username,
        urban["url"],
        closest_track["external_urls"]["spotify"],
    )

    print "Tweeting..."
    print tweet

    print closest_track["uri"]

    context = {
        "tweet": tweet,
        "song_url": closest_track["external_urls"]["spotify"]
    }

    return render(request, 'rockbot/rockbot.html', context)

def get_urban_dictionary_word():
    r = requests.get("http://www.urbandictionary.com/random.php")
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

    return {
        "word": word,
        "definition": definition,
        "url": url
    }

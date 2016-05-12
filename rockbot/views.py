import requests
import pprint
import spotipy
import html5lib
from twython import Twython
from fuzzywuzzy import fuzz, process
from bs4 import BeautifulSoup
from rockbot import spotify_conn, twitter_conn
from django.shortcuts import render

def rockbot(request):
    """
    A homepage that lists all the liveblogs.
    """
    urban = get_urban_dictionary_word()
    search_word = urban["word"]
    definition = urban["definition"]

    keep_searching = True
    i = 0
    while keep_searching:
        search_results = spotify_conn.search(
            q="track:%s" % search_word,
            limit=4
        )
        i = i + 1
        if len(search_results["tracks"]["items"]) > 0 or i > 5:
            keep_searching = False

    matchings = {}

    for track in search_results["tracks"]["items"]:
        ratio = fuzz.ratio(search_word, track["name"])
        track["match"] = ratio

    if len(search_results["tracks"]["items"]) == 0:
        return render(request, 'rockbot/rockbot.html')

    closest_track = max(search_results["tracks"]["items"], key=lambda item: item["match"])

    context = {
        "query": search_word,
        "definition": definition,
        "track": closest_track,
        "tracks": search_results["tracks"]["items"],
    }
    tweet = "%s %s" % (search_word, closest_track["external_urls"]["spotify"])
    twitter_conn.update_status(status=tweet)

    return render(request, 'rockbot/rockbot.html', context)

def get_urban_dictionary_word():
    r = requests.get("http://www.urbandictionary.com/random.php")
    soup = BeautifulSoup(r.content, 'html5lib')
    word = soup.title.text[18:]

    try:
        definition = soup.findAll(attrs={"property":"og:description"})[0]["content"]
    except IndexError:
        definition = None

    return {
        "word": word,
        "definition": definition
    }

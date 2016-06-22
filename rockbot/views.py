#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rockbot.tweet import get_tweet

def rockbot(request):
    """
    A homepage that lists all the liveblogs.
    """
    context = {
        "tweet": get_tweet(),
        "song_url": ""
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

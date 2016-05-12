import spotipy
from twython import Twython

default_app_config = 'rockbot.apps.RockBotConfig'

spotify_conn = spotipy.Spotify()

twitter_conn = Twython(
    'J62n4mTFolJzNWTRo0csf5URS',
    '88rJ1HnZglnZekD1D2E4OfgwOvrDtMyAROHFx68UEQZGWAbvVF',
    '723602054388830212-OyS834zAfVzuy9Y3xnIEiHAlATEKHcq',
    'f03L4NCMV7KKkj5WKIKPl08ylLrXg5BMGrEH20gBWNXha'
)

#!/usr/bin/python3


import pydoc
import json
import requests
from pyfzf.pyfzf import FzfPrompt
import argparse
import os

#https://iptv-org.github.io/api/channels.json
#https://iptv-org.github.io/api/streams.json

class Updater(object):
    
    API_URL='https://iptv-org.github.io/api'
    
    def __init__(self, filename, cache_dir, api_url=API_URL) -> None:
        self._filename = filename
        self._cache_dir = cache_dir
        self._api_url = api_url

    def update(self) -> None:
       r = requests.get(self._api_url + '/' + self._filename , allow_redirects=True)
       open(self._cache_dir + '/' + self._filename, 'wb').write(r.content)
    
    @staticmethod
    def run(cache_dir):
        Updater('channels.json', cache_dir).update()
        Updater('streams.json', cache_dir).update()
        Updater('guides.json', cache_dir).update()
        Updater('categories.json', cache_dir).update()
        Updater('languages.json', cache_dir).update()
        Updater('countries.json', cache_dir).update()
        Updater('subdivisions.json', cache_dir).update()
        Updater('regions.json', cache_dir).update()
        Updater('blocklist.json', cache_dir).update()

    @staticmethod
    def merge(cache_dir):
        channels = Channels( cache_dir + '/' + 'channels.json')
        channels.streams =  Streams( cache_dir + '/' + 'streams.json')
        channels.guides= Guides( cache_dir + '/' + 'guides.json')
        channels.categories = Categories( cache_dir + '/' + 'categories.json')
        channels.languages = Languages( cache_dir + '/' + 'languages.json')
        channels.countries = Countries( cache_dir + '/' + 'countries.json')
        channels.subdivisions = SubDivisions( cache_dir + '/' + 'subdivisions.json')
        #regions = Regions( cache_dir + '/' + 'regions.json')
        #blocklist = Blocklist( cache_dir + '/' + 'blocklist.json')
        channels.dump( cache_dir + '/' + 'channels_all.json')
    
class Streams(object):

    def __init__(self, filename) -> None:
        with open(filename) as json_file:
            self._streams = json.load(json_file)
    
    def stream(self, channel_id) -> dict:
        for stream in self._streams:
            if stream['channel'] == channel_id:
                return stream
        return {'channel': channel_id, 'url': 'N/A'}

    def __str__(self) -> str:
        s = ''
        for stream in self._streams:
            s = '{}\t{}\n{}'.format(stream['channel'], stream['url'], s)
        return s

class Guides(object):

    def __init__(self, filename) -> None:
        with open(filename) as json_file:
            self._guides = json.load(json_file)

    def guide(self, channel_id) -> dict:
        for guide in self._guides:
            if guide['channel'] == channel_id:
                return guide
        return {'channel': channel_id, 'url': 'N/A'}

    def __str__(self) -> str:
        s = ''
        for guide in self._guides:
            s = '{}\t{}\n{}'.format(guide['channel'], guide['url'], s)
        return s

class Categories(object):

    def __init__(self, filename) -> None:
        with open(filename) as json_file:
            self._categories = json.load(json_file)

    def category(self, category_id) -> dict:
        for category in self._categories:
            if category['id'] == category_id:
                return category
        return {'id': category_id, 'name': 'N/A'}

    def __str__(self) -> str:
        s = ''
        for category in self._categories:
            s = '{}\t{}\n{}'.format(category['id'], category['name'], s)
        return s

class Languages(object):

    def __init__(self, filename) -> None:
        with open(filename) as json_file:
            self._languages = json.load(json_file)
    
    def language(self, language_code) -> dict:
        for language in self._languages:
            if language['code'] == language_code:
                return language
        return {'code': language_code, 'name': 'N/A'}

    def __str__(self) -> str:
        s = ''
        for language in self._languages:
            s = '{}\t{}\n{}'.format(language['code'], language['name'], s)
        return s


class Countries(object):

    def __init__(self, filename) -> None:
        with open(filename) as json_file:
            self._countries = json.load(json_file)

    def country(self, country_code) -> dict:
        for country in self._countries:
            if country['code'] == country_code:
                return country
        return {'code': country_code, 'name': 'N/A'}

    def __str__(self) -> str:
        s = ''
        for country in self._countries:
            s = '{}\t{}\n{}'.format(country['code'], country['name'], s)
        return s

class SubDivisions(object):

    def __init__(self, filename) -> None:
        with open(filename) as json_file:
            self._subdivisions = json.load(json_file)

    def subdivision(self, subdivision_code) -> dict:
        for subdivision in self._subdivisions:
            if subdivision['code'] == subdivision_code:
                return subdivision
        return {'code': subdivision_code, 'name': 'N/A'}

    def __str__(self) -> str:
        s = ''
        for subdivision in self._subdivisions:
            s = '{}\t{}\n{}'.format(subdivision['code'], subdivision['name'], s)
        return s

class Regions(object):

    def __init__(self, filename) -> None:
        with open(filename) as json_file:
            self._regions = json.load(json_file)

    def region(self, region_code) -> dict:
        for region in self._regions:
            if region['code'] == region_code:
                return region
        return {'code': region_code, 'name': 'N/A' }

    def __str__(self) -> str:
        s = ''
        for region in self._regions:
            s = '{}\t{}\n{}'.format(region['code'], region['name'], s)
        return s

class Blocklist(object):

    def __init__(self, filename) -> None:
        with open(filename) as json_file:
            self._blocklist = json.load(json_file)

    def block(self, channel_id) -> dict:
        for block in self._blocklist:
            if block['channel'] == channel_id:
                return block
        return {'channel': channel_id, 'ref': 'N/A'}

    def __str__(self) -> str:
        s = ''
        for block in self._blocklist:
            s = '{}\t{}\n{}'.format(block['channel'], block['ref'], s)
        return s

class Channels(object):

    def __init__(self, filename) -> None:
        with open(filename) as json_file:
            self._channels = json.load(json_file)
            self._streams = {}
            self._guides = {}
            self._categories = {}
            self._languages = {}
            self._countries = {}
            self._subdivisions = {}
            self._regions = {}
            self._blocklist = {}

    @property
    def streams(self) -> Streams:
        return Streams(self._streams) 

    @streams.setter
    def streams(self, streams) -> None:
        self._streams =  streams
        for channel in self._channels:
            channel['stream'] = self._streams.stream(channel['id'])
   
    @property
    def guides(self) -> Guides:
        return Guides(self._guides) 

    @guides.setter
    def guides(self, guides) -> None:
        self._guides =  guides
        for channel in self._channels:
            channel['guide'] = self._guides.guide(channel['id'])

    def dump(self, filename):
        with open(filename, 'w') as json_file:
            json.dump(self._channels, json_file)

    @property
    def categories(self) -> Categories:
        return Categories(self._categories) 

    @categories.setter
    def categories(self, categories) -> None:
        self._categories =  categories
        for channel in self._channels:
            categories = []
            for category_id in channel['categories']:
                categories.append(self._categories.category(category_id))
            if not categories:
                categories.append(self._categories.category(-1))
            channel['categories'] = categories;

    @property
    def languages(self) -> Languages:
        return Languages(self._languages) 

    @languages.setter
    def languages(self, languages) -> None:
        self._languages =  languages
        for channel in self._channels:
            languages = []
            for language_code in channel['languages']:
                languages.append(self._languages.language(language_code))
            if not languages:
                languages.append(self._languages.language(-1))
            channel['languages'] = languages;

    @property
    def countries(self) -> Countries:
        return Countries(self._countries) 

    @countries.setter
    def countries(self, countries) -> None:
        self._countries =  countries
        for channel in self._channels:
            channel['country'] = self._countries.country(channel['country']);

    @property
    def subdivisions(self) -> SubDivisions:
        return SubDivisions(self._subdivisions) 

    @subdivisions.setter
    def subdivisions(self, subdivisions) -> None:
        self._subdivisions =  subdivisions
        for channel in self._channels:
            channel['subdivision'] = self._subdivisions.subdivision(channel['subdivision']);

    @staticmethod
    def pad_str(s, max_len)->str:
        if len(s) > max_len:
            return s[:max_len] + '.'
        else:
            n = max_len - len(s)
            return s + ''.join([char * n for char in ' '])


    def channel_list(self) -> list:
        ch_list = []
        for channel in self._channels:
            if channel['stream']['url'] == 'N/A':
                continue
            ch = '{}\t{}\t{}\t{}\t{}'.format(
                    Channels.pad_str(channel['name'], 24),#49
                    Channels.pad_str(channel['categories'][0]['name'], 13),
                    Channels.pad_str(channel['languages'][0]['name'], 16),
                    Channels.pad_str(channel['country']['name'], 16), 
                    channel['stream']['url'],
                    )
            ch_list.append(ch)
        return ch_list

    def __str__(self) -> str:
        s = ''
        for channel in self._channels:
            if channel['stream']['url'] == 'N/A':
                continue
            s = '{}\t{}\t{}\t{}\t{}\n{}'.format(
                    channel['name'], 
                    channel['categories'][0]['name'],
                    channel['languages'][0]['name'],
                    channel['country']['name'], 
                    channel['stream']['url'],
                    s)
        return s

    def pager(self):
        pydoc.pager(channels.__str__())


parser = argparse.ArgumentParser(
                    prog = 'pytermv',
                    description = 'What the program does',
                    epilog = 'Text at the bottom of help')

parser.add_argument('-c', '--cache-dir', default=os.path.expanduser( '~' ) + '/.cache/pytermv', help='path to cache directory')
parser.add_argument('-f', '--full_screen', action='store_true', help='run in full-screen mode')
parser.add_argument('-s', '--term_swallow', action='store_true', help='hide controlling terminal while playing')
parser.add_argument('-u', '--update', action='store_true',  help='update the channels database')
args = parser.parse_args()

if not os.path.exists(args.cache_dir):
    os.makedirs(args.cache_dir)
    args.update = True

if args.update:
    Updater.run(args.cache_dir)
    Updater.merge(args.cache_dir)

channels = Channels(args.cache_dir + '/' + 'channels_all.json')

mpv_args='{}{}'.format('-f ' if args.full_screen else '', '-s ' if args.term_swallow else '')

SCRIPT_DIRNAME = os.path.dirname(os.path.abspath(__file__))

fzf = FzfPrompt()
channel = fzf.prompt(
        channels.channel_list(),
        '-e -i --reverse --cycle --with-nth="1..-2" {} {} {} {} {}'.format(
            '--bind "alt-]:execute-silent('+SCRIPT_DIRNAME+'/player.sh -b ' + mpv_args + ' {})"',
            '--bind "enter:execute('+SCRIPT_DIRNAME+'/player.sh ' + mpv_args + ' {})"',
            '--bind "double-click:execute('+SCRIPT_DIRNAME+'/player.sh ' + mpv_args + '{})"',
            '--header="Select channel (press Escape to exit)"',
            '-q ""'
            )
        )


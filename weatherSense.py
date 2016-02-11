#!/usr/bin/env python

import sys
import os
import shutil
import pywapi
import datetime
import time
from TwitterAPI import TwitterAPI
import urllib3
import json


def add_tags(songs):

    count = 0
    my_dict = {}

    print '\n*** Enter the mood parameters seperated by comma ***\n'
    set_slow = raw_input('Enter temperature range for the SLOW tag > ').split(',')
    set_medium = raw_input('Enter temperature range for the MEDIUM tag > ').split(',')
    set_fast = raw_input('Enter temperature range for the FAST tag > ').split(',')
    print '\n'

    set_slow = map(int, set_slow)
    set_medium = map(int, set_medium)
    set_fast = map(int, set_fast)

    add_folders()

    while (count < 5):#len(songs)):

        tag = raw_input('Enter the Tag you wish to add to this song : ' + songs[count] + '\n>').lower()

        if str(tag) == 'slow' or str(tag) == 'medium' or str(tag) == 'fast':
            my_dict.setdefault(tag, [])
            my_dict[tag].append(songs[count])
            count = count + 1

        else:
            print 'Not a Valid Tag'

    while True:

        tmp1 = os.listdir('/home/netman/project/music')
        #print tmp1
        #print '\n'
        time.sleep(10)
        playlist_modified(tmp1, my_dict)
        generate_playlist(my_dict, set_slow, set_medium, set_fast)


def add_folders():

    tmp = '/home/netman/project/music/'
    folder = os.listdir(tmp)

    try:

        if os.path.exists(tmp + 'slow_folder'):
            pass
        else:
            os.mkdir(tmp + 'slow_folder')

        if os.path.exists(tmp + 'medium_folder'):
            pass
        else:
            os.mkdir(tmp + 'medium_folder')

        if os.path.exists(tmp + 'fast_folder'):
            pass
        else:
            os.mkdir(tmp + 'fast_folder')

    except:
        pass


def playlist_modified(tmp1, my_dict):

    tmp2 = os.listdir('/home/netman/project/music')


    if len(tmp1) > len(tmp2):
        z = set(tmp1).difference(set(tmp2))
        print '\nExisting Tracks Deleted: {}\n'.format(z)

    elif len(tmp1) < len(tmp2):
        z = set(tmp2).difference(set(tmp1))
        print '\nNew Tracks Added: {}\n'.format(z)

        count = 0

        while count < len(z):

            new_song = list(z)
            tag = raw_input('Enter the Tag you wish to add to this song: ' + new_song[count] + '\n>').lower()

            if str(tag) == 'slow' or str(tag) == 'medium' or str(tag) == 'fast':
                my_dict.setdefault(tag, [])
                my_dict[tag].append(new_song[count])
                count = count + 1

            else:
                print 'Not a Valid Tag'

    else:
        pass

    return my_dict


def generate_playlist(my_dict, set_slow, set_medium, set_fast):

    tmp1 = '/home/netman/project/music/'

    current = int(get_yahoo_weather())
    print 'Current Temperature is: {}\n Generating Playlist.....'.format(current)

    print type(set_medium[0]), type(set_slow[1])

    if current >= set_slow[0] and current <= set_slow[1]:
        get_dict = my_dict.get('slow')
        for slow in get_dict:
            if os.path.exists(tmp1 + slow):
                shutil.copy(tmp1 + slow, tmp1 + 'slow_folder')

            else:
                pass

    elif current >= set_medium[0] and current <= set_medium[1]:
        get_dict = my_dict.get('medium')
        for slow in get_dict:
            if os.path.exists(tmp1 + slow):
                shutil.copy(tmp1 + slow, tmp1 + 'medium_folder')

            else:
                pass

    elif current >= set_fast[0] and current <= set_fast[1]:
        print my_dict.get('high')
        for slow in get_dict:
            if os.path.exists(tmp1 + slow):
                shutil.copy(tmp1 + slow, tmp1 + 'fast_folder')

            else:
                pass


def copy_files(get_dict, tmp1, folder):

    pass


def get_yahoo_weather():

    yahoo_result = pywapi.get_weather_from_yahoo('80302')
    return yahoo_result['condition']['temp']


def tweet_msg():

    consumer_key = ''
    consumer_secret = ''
    access_token_key = ''
    access_token_secret = ''

    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

    r = api.request('statuses/update', {'status':'Hello!This is a tweet!'})
    print r.status_code

def main():

    urllib3.disable_warnings()
    music = '/home/netman/project/music'
    os.chdir(music)
    songs = sorted(os.listdir(music))
    print '''THANKS FOR USING WEATHER ADAPTIVE MUSIC PLAYER
          TAGS : SLOW, MEDIUM, FAST
    '''
    add_tags(songs)

if __name__ == '__main__':
    sys.exit(main())

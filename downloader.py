#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Downloads and logs a playlist file
#
# Requires youtube_dl
#

from __future__ import unicode_literals

import youtube_dl
from shutil import copyfile
import logging


PLAYLIST_FILE = "playlist.txt"
PLAYLIST_DELIMITER = ";"

DOWNLOAD_DIR = "downloads/"
COOKIE_FILE = "cookies.txt"

LOG_FILE = "plist.log"
LOG_ERROR_FILE = "plist_error.log"


def progress_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')
        Log.status(d['filename'], d['status'])


ydl_settings = {
    'cookiefile': COOKIE_FILE,
    'noplaylist' : True,
    'progress_hooks': [progress_hook],
    'default_search': "ytsearch",
    'writesubtitles': True,
}


# Log events
class Log:

    @staticmethod
    def error(error, url):
        logging.basicConfig(level=logging.ERROR,
                            filename=LOG_ERROR_FILE,
                            filemode='a',
                            format='%(asctime)s %(message)s')
        logging.error("----------------------------------------  ERROR  ---------------------------------------------")
        logging.error(url + ".................." + str(error))

    @staticmethod
    def status(filename, status):
        logging.basicConfig(level=logging.INFO,
                            filename=LOG_FILE,
                            filemode='a',
                            format='%(asctime)s %(message)s')
        logging.info(filename+"................"+status)

    @staticmethod
    def message(message):
        logging.basicConfig(level=logging.INFO,
                            filename=LOG_FILE,
                            filemode='a',
                            format='%(message)s')
        logging.info("-----------------------------------------------------------")
        logging.info("--------------- " + message + " --------------------------")
        logging.info("-----------------------------------------------------------")


# Download a single item in the DOWNLOAD directory
def dl_item(output, url):
    ydl_settings['outtmpl'] = DOWNLOAD_DIR + output + '/%(playlist_index)s.%(title)s.%(ext)s'

    try:
        with youtube_dl.YoutubeDL(ydl_settings) as ydl:
            ydl.download([url])
    except Exception, e:
        Log.error(e, url)


# Remove first line in the PLAYLIST_FILE
def update_playlist():
    f = open(str(PLAYLIST_FILE)).readlines()
    open(str(PLAYLIST_FILE), str('w')).writelines(f[1:])


# Download items in the PLAYLIST_FILE
# Will remove the item once completed in the PLAYLIST_FILE
def start_download():
    lines = [line.rstrip('\n') for line in open(PLAYLIST_FILE)]
    copyfile(PLAYLIST_FILE, PLAYLIST_FILE + ".bk")

    Log.message("DOWNLOAD STARTED")
    for item in lines:
        i = item.split(PLAYLIST_DELIMITER)
        if i.__len__() == 2:
            dl_item(i[0], i[1])
            update_playlist()
    Log.message("DOWNLOAD COMPLETE")


# Execute
start_download()

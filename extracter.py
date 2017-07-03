#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Extracts titles and urls of an html file
# Write the results in the PLAYLIST_DEST file
# ex: title;url\n
#
# Requires BeautifulSoup
#

import codecs
from bs4 import BeautifulSoup

PLAYLIST_SRC = codecs.open('playlist.html')
PLAYLIST_DEST = 'playlist.txt'
DELIMITER= ';'

# Get the item info
#   - item_container
#       - item_link, url
#           - loop until we hit the final tag ['a']
#       - item_name, folder name
#           - loop until we hit the final tag ['']
pl_query = {
    'selector': {
        'item_container': [
            ['ol', 'class', 'qlist ui-sortable'],
        ],
        'item_link': [
            # tag name with an attribute ex: ['div', 'id', 'rico_is_awesome']
            ['div', 'class', 'qPreview'],
            ['a'], ##  Required
        ],
        'item_name': [
            ['div', 'class', 'qCourse'],
            ['a'], ##  Required
        ]
    },
}


def get_playlist():
    playlist = {}
    soup = BeautifulSoup(PLAYLIST_SRC.read(), "html.parser")

    # get course list
    for selector in pl_query['selector']['item_container']:
        soup = get_item_url(selector, soup)

    # get course items
    for course in soup:
        url = course
        for selector in pl_query['selector']['item_link']:
            url = get_item_url(selector, url)

        title = course
        for selector in pl_query['selector']['item_name']:
            title = get_item_name(selector, title)

        if course:
            playlist[normalise(title)] = url

    return playlist


def get_item_url(selector, soup):
    if selector.__len__() == 1:
        for v in soup.find_all(selector[0]):
            return v.get('href')
    else:
        return soup.find(selector[0], { selector[1], selector[2] })


def get_item_name(selector, soup):
    if selector.__len__() == 1:
        for v in soup.find_all(selector[0]):
            return v.get_text()
    else:
        return soup.find(selector[0], { selector[1], selector[2] })


def normalise(value):
    return str(value) \
        .replace(':', '-') \
        .replace(' ', '_') \
        .replace('\t','')


def save_playlist():
    file = open(PLAYLIST_DEST, 'w')
    playlist = get_playlist()

    for title, url in playlist.iteritems():
        if title != 'None' and url != 'None':
            file.write(str(title) + DELIMITER + str(url) + '\n')


# Execute
save_playlist()

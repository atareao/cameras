#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# comun.py
#
# This file is part of Cameras
#
# Copyright (C) 2016
# Lorenzo Carbonell Cerezo <lorenzo.carbonell.cerezo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import locale
import gettext
import sys

__author__ = 'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'
__date__ = '$13/03/2016'
__copyright__ = 'Copyright (c) 2016 Lorenzo Carbonell'
__license__ = 'GPLV3'
__url__ = 'http://www.atareao.es'
######################################


def is_package():
    return __file__.find('src') < 0

######################################
PARAMS = {'cameras': [
            {'url': 'http://webcamsdemexico.net/puertovallarta2/live.jpg',
             'x': 200,
             'y': 200,
             'scale': 100,
             'refresh-time': 10,
             'onwidgettop': False,
             'showintaskbar': False,
             'onalldesktop': True,
             'on': True
             },
            {'url': 'http://213.162.193.213/alacant.jpg',
             'x': 400,
             'y': 200,
             'scale': 100,
             'refresh-time': 10,
             'onwidgettop': False,
             'showintaskbar': False,
             'onalldesktop': True,
             'on': True
             },
            {'url': 'http://213.162.193.213/desafio.jpg',
             'x': 600,
             'y': 200,
             'scale': 100,
             'refresh-time': 10,
             'onwidgettop': False,
             'showintaskbar': False,
             'onalldesktop': True,
             'on': True
             }
          ],
          'autostart': False,
          'theme': 'light',
          'webcam-x': 200,
          'webcam-y': 200,
          'webcam-onwidgettop': False,
          'webcam-showintaskbar': False,
          'webcam-onalldesktop': False,
          'webcam-on': False,
          'webcam-show': False,
          }

APP = 'cameras'
APP_CONF = APP + '.conf'
APPNAME = 'Cameras'
CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.config')
CONFIG_APP_DIR = os.path.join(CONFIG_DIR, APP)
CONFIG_FILE = os.path.join(CONFIG_APP_DIR, APP_CONF)
#########################################

# check if running from source
if is_package():
    USRDIR = '/opt/extras.ubuntu.com/cameras/'
    ROOTDIR = os.path.join(USRDIR, 'share')
    LANGDIR = os.path.join(ROOTDIR, 'locale-langpack')
    APPDIR = os.path.join(ROOTDIR, APP)
    SOCIALDIR = os.path.join(APPDIR, 'social')
    ICONDIR = os.path.join(ROOTDIR, 'icons')
    IMAGESDIR = os.path.join(APPDIR, 'images')
    CHANGELOG = os.path.join(APPDIR, 'changelog')
    AUTOSTARTO = os.path.join(APPDIR,
                              'extras-cameras-autostart.desktop')
else:
    ROOTDIR = os.path.dirname(__file__)
    LANGDIR = os.path.normpath(os.path.join(ROOTDIR, '../template1'))
    APPDIR = ROOTDIR
    DATADIR = os.path.normpath(os.path.join(ROOTDIR, '../data'))
    ICONDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/icons'))
    IMAGESDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/images'))
    SOCIALDIR = os.path.normpath(os.path.join(ROOTDIR, '../data/social'))
    DEBIANDIR = os.path.normpath(os.path.join(ROOTDIR, '../debian'))
    CHANGELOG = os.path.join(DEBIANDIR, 'changelog')
    AUTOSTARTO = os.path.join(DATADIR,
                              'extras-cameras-autostart.desktop')
AUTOSTART_DIR = os.path.join(CONFIG_DIR, 'autostart')
AUTOSTARTD = os.path.join(AUTOSTART_DIR,
                          'extras-cameras-autostart.desktop')
ICON = os.path.join(ICONDIR, 'cameras.svg')
f = open(CHANGELOG, 'r')
line = f.readline()
f.close()
pos = line.find('(')
posf = line.find(')', pos)
VERSION = line[pos + 1:posf].strip()
if not is_package():
    VERSION = VERSION + '-src'
####
try:
    current_locale, encoding = locale.getdefaultlocale()
    language = gettext.translation(APP, LANGDIR, [current_locale])
    language.install()
    print(language)
    if sys.version_info[0] == 3:
        _ = language.gettext
    else:
        _ = language.ugettext
except Exception as e:
    print(e)
    _ = str
APPNAME = _(APPNAME)

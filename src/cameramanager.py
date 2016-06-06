#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# camerawidget.py
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

import gi
try:
    gi.require_version('Gst', '1.0')
    gi.require_version('Gtk', '3.0')
    gi.require_version('GstVideo', '1.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gst
from gi.repository import GdkX11
from gi.repository import GstVideo
from gi.repository import GObject
from configurator import Configuration
from camerawidget import CameraWidget
from webcamwidget import WebcamWidget
from preferences_dialog import PreferencesDialog


class CameraManager():

    def __init__(self):
        self.cameras = []
        self.wcw = None

    def start(self):
        configuration = Configuration()
        if configuration.get('webcam-show'):
            self.wcw = WebcamWidget()
            self.wcw.connect('preferences', self.on_preferences)
            self.wcw.show()
        cameras = configuration.get('cameras')
        if len(cameras) > 0:
            for acamera in cameras:
                if 'on' not in acamera.keys() or acamera['on'] is True:
                    cm = CameraWidget(acamera)
                    cm.connect('preferences', self.on_preferences)
                    cm.show()
                    cm.start_updater()
                    self.cameras.append(cm)

    def on_preferences(self, data):
        cm = PreferencesDialog()
        ans = cm.run()
        if ans == Gtk.ResponseType.ACCEPT:
            cm.save_preferences()
            cm.destroy()
            self.stop()
            self.start()
        elif ans == Gtk.ResponseType.CLOSE:
            cm.destroy()
            self.stop()
            exit(0)
        else:
            cm.destroy()

    def stop(self):
        if self.wcw is not None:
            self.wcw.stop()
            self.wcw = None
        for camera in self.cameras:
            camera.stop()


def main():
    import time
    GLib.threads_init()
    Gst.init(None)
    cm = CameraManager()
    cm.start()
    Gtk.main()
    cm.stop()
    exit(0)


if __name__ == '__main__':
    main()

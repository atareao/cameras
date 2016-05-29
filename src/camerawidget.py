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
    gi.require_version('Gtk', '3.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf
import os
import cairo
import datetime
import requests
from PIL import Image
import requests
import threading
import time
import comun
from configurator import Configuration
from preferences_dialog import PreferencesDialog


class Downloader(threading.Thread, GObject.GObject):
    __gsignals__ = {
        'downloaded': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (
            bool, object, float, float)),
        }

    def __init__(self, url, scale):
        GObject.GObject.__init__(self)
        threading.Thread.__init__(self)
        self.daemon = True
        self.url = url
        self.scale = scale

    def run(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                loader = GdkPixbuf.PixbufLoader()
                loader.write(response.content)
                loader.close()
                pixbuf = loader.get_pixbuf()
                height = pixbuf.get_height() * self.scale / 100.0
                width = pixbuf.get_width() * self.scale / 100.0
                scaled_buf = pixbuf.scale_simple(
                    width, height, GdkPixbuf.InterpType.BILINEAR)
                if scaled_buf:
                    surface = cairo.ImageSurface(
                        cairo.FORMAT_ARGB32,
                        scaled_buf.get_width(),
                        scaled_buf.get_height())
                    context = cairo.Context(surface)
                    Gdk.cairo_set_source_pixbuf(context, scaled_buf, 0, 0)
                    context.paint()
                    self.emit('downloaded', True, surface, width, height)
                    return
        except Exception as e:
            print(e)
        self.emit('downloaded', False, None, -1, -1)
        return


class CameraWidget(Gtk.Window):
    __gsignals__ = {
        'pinit': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (bool,)),
        'preferences': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        }

    def __init__(self, camera):
        Gtk.Window.__init__(self)
        self.camera = camera
        self.set_title('Camera')
        # self.set_icon_from_file(comun.ICON)
        if os.environ.get('DESKTOP_SESSION') == "ubuntu":
            self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        else:
            self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.supports_alpha = False
        self.set_decorated(False)
        self.set_border_width(0)
        self.set_accept_focus(False)
        self.set_app_paintable(True)
        self.set_skip_pager_hint(True)
        self.set_role('')
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual is not None and screen.is_composited():
            self.set_visual(visual)
        self.add_events(Gdk.EventMask.ALL_EVENTS_MASK)
        self.connect('button-press-event', self.button_press)
        self.connect('draw', self.on_expose, None)
        self.connect('configure-event', self.configure_event)
        self.connect('screen-changed', self.screen_changed)
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self.add(vbox)
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        vbox.pack_start(hbox, False, False, 10)
        button = Gtk.Button()
        button.connect('clicked', self.on_button_clicked)
        hbox.pack_start(button, False, False, 10)
        self.pin = Gtk.Image()
        button.add(self.pin)
        button.set_name('pin')
        on_button = Gtk.Button()
        on_button.connect('clicked', self.on_button_on_clicked)
        hbox.pack_end(on_button, False, False, 10)
        self.on = Gtk.Image()
        on_button.add(self.on)
        on_button.set_name('on')
        #
        # self.image = Gtk.Image()
        # vbox.pack_start(self.image, True, True, 0)
        #
        self.datetime = datetime.datetime.utcnow()
        self.filename = None
        self.temperature = None
        self.location = None
        self.parse_time = False
        self.surface = None
        self.updater = 0
        #
        style_provider = Gtk.CssProvider()
        css = """
            #pin{
                opacity:0.05;
                border-image: none;
                background-image: none;
                background-color: rgba(0, 0, 0, 0);
                border-radius: 0px;
            }
            #pin:hover {
                transition: 1000ms linear;
                opacity:1.0;
                border-image: none;
                background-image: none;
                background-color: rgba(0, 0, 0, 0);
                border-radius: 0px;
            }
            #on{
                opacity:0.05;
                border-image: none;
                background-image: none;
                background-color: rgba(0, 0, 0, 0);
                border-radius: 0px;
            }
            #on:hover {
                transition: 1000ms linear;
                opacity:1.0;
                border-image: none;
                background-image: none;
                background-color: rgba(0, 0, 0, 0);
                border-radius: 0px;
            }
        """
        style_provider.load_from_data(css.encode('UTF-8'))
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.is_above = camera['onwidgettop']
        self.set_keep_above(camera['onwidgettop'])
        self.is_set_keep_above(camera['onwidgettop'])
        self.set_keep_below(not camera['onwidgettop'])
        if camera['onalldesktop']:
            self.stick()
        else:
            self.unstick()
        self.move(camera['x'], camera['y'])
        self.on.set_from_pixbuf(
            GdkPixbuf.Pixbuf.new_from_file_at_scale(
                os.path.join(comun.IMAGESDIR, 'on.svg'), 50, 50, 1))
        self.screen_changed(self)
        self.show_all()

    def is_set_keep_above(self, keep_above):
        print(keep_above)
        x, y = self.get_position()
        print(x, y)
        self.set_keep_above(keep_above)
        self.set_keep_below(not keep_above)
        if keep_above:
            self.pin.set_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    os.path.join(comun.IMAGESDIR, 'pinin.svg'), 36, 72, 1))
        else:
            self.pin.set_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    os.path.join(comun.IMAGESDIR, 'pinup.svg'), 36, 36, 1))
        self.hide()
        self.show()
        self.move(x, y)
        print(x, y)

    def screen_changed(self, widget, old_screen=None):
        # To check if the display supports alpha channels, get the colormap
        screen = widget.get_screen()
        visual = screen.get_rgba_visual()
        if visual is None or not widget.is_composited():
            self.supports_alpha = False
        else:
            self.supports_alpha = True
        return False

    def configure_event(self, widget, event):
        self.save_preferences()

    def button_press(self, widget, event):
        print(event.button)
        if event.button == 1:
            self.begin_move_drag(
                1, int(event.x_root), int(event.y_root), event.time)
            return True
        elif event.button == 3:
            self.emit('preferences')
            return True
        return False

    def on_button_on_clicked(self, widget):
        configuration = Configuration()
        x, y = self.get_position()
        cameras = configuration.get('cameras')
        for index, acamera in enumerate(cameras):
            if acamera['url'] == self.camera['url']:
                acamera['on'] = False
                cameras[index] = acamera
        configuration.save()
        self.stop()

    def on_button_clicked(self, widget):
        self.is_above = not self.is_above
        self.emit('pinit', self.is_above)
        self.is_set_keep_above(self.is_above)

    def on_downloaded(self, downloader, is_ok, surface, width, height):
        if is_ok is True:
            self.width = width
            self.height = height
            self.resize(width, height)
            self.surface = surface
            GObject.idle_add(self.queue_draw)

    def on_expose(self, widget, cr, data):
        if self.surface is not None:
            cr.save()
            cr.set_operator(cairo.OPERATOR_CLEAR)
            cr.rectangle(0.0, 0.0, *widget.get_size())
            cr.fill()
            cr.restore()
            cr.save()
            cr.set_source_surface(self.surface)
            cr.paint()
            cr.restore()

    def save_preferences(self):
        configuration = Configuration()
        x, y = self.get_position()
        cameras = configuration.get('cameras')
        for index, acamera in enumerate(cameras):
            if acamera['url'] == self.camera['url']:
                acamera['x'] = x
                acamera['y'] = y
                acamera['onwidgettop'] = self.is_above
                cameras[index] = acamera
        configuration.save()

    def stop(self):
        self.stop_updater()
        self.destroy()

    def start_updater(self):
        if self.updater > 0:
            GLib.source_remove(self.updater)
        self.update()
        self.updater = GLib.timeout_add_seconds(self.camera['refresh-time'],
                                                self.update)

    def stop_updater(self):
        if self.updater > 0:
            GLib.source_remove(self.updater)
            self.updater = 0

    def update(self):
        downloader = Downloader(self.camera['url'], self.camera['scale'])
        downloader.connect('downloaded', self.on_downloaded)
        downloader.start()


def main():
    GObject.threads_init()
    configuration = Configuration()
    cameras = configuration.get('cameras')
    if len(cameras) > 0:
        for acamera in cameras:
            cm = CameraWidget(acamera)
            cm.show()
            cm.start_updater()
        Gtk.main()
    exit(0)

if __name__ == '__main__':
    main()

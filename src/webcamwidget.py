#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# webcamwidget.py
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
from gi.repository import Gst
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf
from gi.repository import Gtk
from gi.repository import GdkX11
from gi.repository import GstVideo
import sys
import os
import comun
from configurator import Configuration


class WebcamWidget(Gtk.Window):
    __gsignals__ = {
        'pinit': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (bool,)),
        'preferences': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        }

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title('Webcam')
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

        '''
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual is not None and screen.is_composited():
            self.set_visual(visual)
        '''
        self.add_events(Gdk.EventMask.ALL_EVENTS_MASK)
        self.connect('button-press-event', self.button_press)
        # self.connect('draw', self.on_expose, None)
        self.connect('configure-event', self.configure_event)
        self.connect('screen-changed', self.screen_changed)
        vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        # overlay = Gtk.Overlay()
        self.add(vbox)
        # self.add(overlay)
        self.movie_window = Gtk.DrawingArea()
        self.movie_window.set_size_request(500, 375)
        vbox.pack_end(self.movie_window, False, False, 1)
        # overlay.add(self.movie_window)
        hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        hbox.set_size_request(40, 40)
        vbox.pack_start(hbox, False, False, 1)
        # overlay.add_overlay(hbox)
        button = Gtk.Button()
        button.set_size_request(40, 40)
        button.connect('clicked', self.on_button_clicked)
        hbox.pack_start(button, False, False, 1)
        self.pin = Gtk.Image()
        button.add(self.pin)
        button.set_name('pin')
        on_button = Gtk.Button()
        on_button.set_size_request(40, 40)
        on_button.connect('clicked', self.on_button_on_clicked)
        hbox.pack_end(on_button, False, False, 1)
        self.on = Gtk.Image()
        on_button.add(self.on)
        on_button.set_name('on')
        #
        # self.image = Gtk.Image()
        # vbox.pack_start(self.image, True, True, 0)
        #
        self.filename = None
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
        self.screen_changed(self)
        self.player = Gst.parse_launch("v4l2src ! autovideosink")
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)
        self.on.set_from_pixbuf(
            GdkPixbuf.Pixbuf.new_from_file_at_scale(
                os.path.join(comun.IMAGESDIR, 'off.svg'), 50, 50, 1))

        self.load_preferences()
        self.show_all()

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.player.set_state(Gst.State.NULL)
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error: %s" % (err, debug))
            self.player.set_state(Gst.State.NULL)

    def on_sync_message(self, bus, message):
        struct = message.get_structure()
        if not struct:
            return
        message_name = struct.get_name()
        print(message_name)
        if message_name == "prepare-window-handle":
            # Assign the viewport
            imagesink = message.src
            imagesink.set_property("force-aspect-ratio", True)
            print(imagesink.get_property("window-width"))
            imagesink.set_window_handle(
                self.movie_window.get_property('window').get_xid())
            print('must be playing')

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
        if self.is_on is True:
            print('stop')
            self.is_on = False
            self.player.set_state(Gst.State.NULL)
            self.on.set_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    os.path.join(comun.IMAGESDIR, 'off.svg'), 50, 50, 1))
        else:
            print('start')
            self.is_on = True
            self.player.set_state(Gst.State.PLAYING)
            self.on.set_from_pixbuf(
                GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    os.path.join(comun.IMAGESDIR, 'on.svg'), 50, 50, 1))

    def on_button_clicked(self, widget):
        self.is_above = not self.is_above
        self.emit('pinit', self.is_above)
        self.is_set_keep_above(self.is_above)

    def load_preferences(self):
        configuration = Configuration()
        x = configuration.get('webcam-x')
        y = configuration.get('webcam-y')
        self.is_above = configuration.get('webcam-onwidgettop')
        self.showintaskbar = configuration.get('webcam-showintaskbar')
        self.onalldesktop = configuration.get('webcam-onalldesktop')
        self.is_on = configuration.get('webcam-on')
        self.set_keep_above(self.is_above)
        self.is_set_keep_above(self.is_above)
        self.set_keep_below(not self.is_above)
        if self.onalldesktop:
            self.stick()
        else:
            self.unstick()
        self.move(x, y)

    def save_preferences(self):
        try:
            configuration = Configuration()
            x, y = self.get_position()
            configuration.set('webcam-x', x)
            configuration.set('webcam-y', y)
            configuration.set('webcam-onwidgettop', self.is_above)
            configuration.set('webcam-showintaskbar', self.showintaskbar)
            configuration.set('webcam-onalldesktop', self.onalldesktop)
            configuration.set('webcam-on', self.is_on)
            configuration.save()
        except Exception as e:
            print(e)

    def stop(self):
        self.stop_updater()
        self.destroy()

    def start_updater(self):
        pass

    def stop_updater(self):
        pass

    def update(self):
        pass


def main():
    GObject.threads_init()
    Gst.init(None)
    wcw = WebcamWidget()
    wcw.show()
    Gtk.main()
    exit(0)

if __name__ == '__main__':
    main()

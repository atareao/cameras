#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# preferences_dialog.py
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
import comun
import os
import shutil
from comun import _
from configurator import Configuration


def create_or_remove_autostart(create):
    if not os.path.exists(comun.AUTOSTART_DIR):
        os.makedirs(comun.AUTOSTART_DIR)
    if create is True:
        if not os.path.exists(comun.AUTOSTARTD):
            shutil.copyfile(comun.AUTOSTARTO, comun.AUTOSTARTD)
    else:
        if os.path.exists(comun.AUTOSTARTD):
            os.remove(comun.AUTOSTARTD)


class PreferencesDialog(Gtk.Dialog):

    def __init__(self):
        #
        Gtk.Dialog.__init__(self,
                            'Cameras | '+_('Preferences'),
                            None,
                            Gtk.DialogFlags.MODAL |
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            (Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT,
                                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_QUIT, Gtk.ResponseType.CLOSE))
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_size_request(600, 200)
        self.connect('close', self.close_ok)
        # self.set_icon_from_file(comun.ICON)
        #
        vbox0 = Gtk.VBox(spacing=5)
        vbox0.set_border_width(5)
        self.get_content_area().add(vbox0)
        # ***************************************************************
        self.notebook = Gtk.Notebook.new()
        vbox0.add(self.notebook)
        # ***************************************************************
        vbox11 = Gtk.VBox(spacing=5)
        vbox11.set_border_width(5)
        self.notebook.append_page(vbox11, Gtk.Label.new(_('General')))
        frame11 = Gtk.Frame()
        vbox11.pack_start(frame11, False, True, 1)
        table11 = Gtk.Table(4, 2, False)
        frame11.add(table11)
        # ***************************************************************
        label11 = Gtk.Label(_('Autostart')+':')
        label11.set_alignment(0, 0.5)
        table11.attach(label11, 0, 1, 0, 1, xpadding=5, ypadding=5)
        self.switch1 = Gtk.Switch()
        table11.attach(self.switch1, 1, 2, 0, 1,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)
        label12 = Gtk.Label(_('Icon light')+':')
        label12.set_alignment(0, 0.5)
        table11.attach(label12, 0, 1, 1, 2, xpadding=5, ypadding=5)
        self.switch2 = Gtk.Switch()
        table11.attach(self.switch2, 1, 2, 1, 2,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)
        new_camera_button = Gtk.Button()
        new_camera_button.set_label(_('Add new camera'))
        new_camera_button.connect('clicked',
                                  self.on_new_camera_button_clicked)
        table11.attach(new_camera_button, 0, 2, 2, 3,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)
        # ***************************************************************
        frame12 = Gtk.Frame.new(_('Webcam'))
        vbox11.pack_start(frame12, False, True, 1)
        table12 = Gtk.Table(4, 2, False)
        frame12.add(table12)
        label13 = Gtk.Label(_('Show')+':')
        label13.set_alignment(0, 0.5)
        table12.attach(label13, 0, 1, 1, 2,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.FILL)
        self.webcam_show = Gtk.Switch()
        self.webcam_show.set_active(False)
        table12.attach(self.webcam_show, 1, 2, 1, 2,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)
        label14 = Gtk.Label(_('Widget on top')+':')
        label14.set_alignment(0, 0.5)
        table12.attach(label14, 0, 1, 2, 3,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.FILL)
        self.webcam_onwidgettop = Gtk.Switch()
        self.webcam_onwidgettop.set_active(False)
        table12.attach(self.webcam_onwidgettop, 1, 2, 2, 3,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)
        label15 = Gtk.Label(_('Show in taskbar')+':')
        label15.set_alignment(0, 0.5)
        table12.attach(label15, 0, 1, 3, 4,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.FILL)
        self.webcam_showintaskbar = Gtk.Switch()
        self.webcam_showintaskbar.set_active(False)
        table12.attach(self.webcam_showintaskbar, 1, 2, 3, 4,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)
        label16 = Gtk.Label(_('Show on all desktop')+':')
        label16.set_alignment(0, 0.5)
        table12.attach(label16, 0, 1, 4, 5,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.FILL)
        self.webcam_onalldesktop = Gtk.Switch()
        self.webcam_onalldesktop.set_active(False)
        table12.attach(self.webcam_onalldesktop, 1, 2, 4, 5,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)

        #
        self.load_preferences()
        #
        self.show_all()

    def on_new_camera_button_clicked(self, widget):
        cameras = str(self.notebook.get_n_pages())
        data = {}
        vbox11 = Gtk.VBox(spacing=5)
        vbox11.set_border_width(5)
        self.notebook.append_page(
            vbox11, Gtk.Label.new(_('Camera') + ' ' + cameras))
        frame11 = Gtk.Frame()
        vbox11.pack_start(frame11, False, True, 1)
        table11 = Gtk.Table(7, 2, False)
        frame11.add(table11)
        label11 = Gtk.Label(_('Url')+':')
        label11.set_alignment(0, 0.5)
        table11.attach(label11, 0, 1, 0, 1,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.FILL)
        data['url'] = Gtk.Entry()
        data['url'].set_width_chars(80)
        table11.attach(data['url'], 1, 2, 0, 1,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.FILL)
        label12 = Gtk.Label(_('Scale')+':')
        label12.set_alignment(0, 0.5)
        table11.attach(label12, 0, 1, 1, 2,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.FILL)
        data['scale'] = Gtk.SpinButton()
        data['scale'].set_adjustment(
            Gtk.Adjustment.new(100,
                               1,
                               101,
                               1,
                               10,
                               1))
        table11.attach(data['scale'], 1, 2, 1, 2,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)
        label14 = Gtk.Label(_('Widget on top')+':')
        label14.set_alignment(0, 0.5)
        table11.attach(label14, 0, 1, 2, 3,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.FILL)
        data['onwidgettop'] = Gtk.Switch()
        data['onwidgettop'].set_active(False)
        table11.attach(data['onwidgettop'], 1, 2, 2, 3,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)
        label15 = Gtk.Label(_('Show in taskbar')+':')
        label15.set_alignment(0, 0.5)
        table11.attach(label15, 0, 1, 3, 4,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.FILL)
        data['showintaskbar'] = Gtk.Switch()
        data['showintaskbar'].set_active(False)
        table11.attach(data['showintaskbar'], 1, 2, 3, 4,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)
        label16 = Gtk.Label(_('Show on all desktop')+':')
        label16.set_alignment(0, 0.5)
        table11.attach(label16, 0, 1, 4, 5,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.FILL)
        data['onalldesktop'] = Gtk.Switch()
        data['onalldesktop'].set_active(False)
        table11.attach(data['onalldesktop'], 1, 2, 4, 5,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)
        label17 = Gtk.Label(_('Refresh time')+':')
        label17.set_alignment(0, 0.5)
        table11.attach(label17, 0, 1, 5, 6,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.FILL)
        data['refresh-time'] = Gtk.SpinButton()
        data['refresh-time'].set_adjustment(
            Gtk.Adjustment.new(10,
                               10,
                               3600,
                               10,
                               50,
                               10))
        table11.attach(data['refresh-time'], 1, 2, 5, 6,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)
        label18 = Gtk.Label(_('On')+':')
        label18.set_alignment(0, 0.5)
        table11.attach(label18, 0, 1, 6, 7,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.FILL)
        data['on'] = Gtk.Switch()
        data['on'].set_active(True)
        table11.attach(data['on'], 1, 2, 6, 7,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)
        remove_button = Gtk.Button()
        remove_button.set_label(_('Remove camera') + ' ' + cameras)
        remove_button.connect('clicked',
                              self.on_remove_button_clicked)
        table11.attach(remove_button, 0, 2, 7, 8,
                       xpadding=5,
                       ypadding=5,
                       xoptions=Gtk.AttachOptions.SHRINK)
        self.widgets.append(data)
        self.show_all()

    def on_change_on_ac(self, widget, on_ac):
        self.value_on_ac.set_sensitive(on_ac)

    def on_change_on_low_power(self, widget, on_low_power):
        self.value_on_low_power.set_sensitive(on_low_power)
        self.low_battery_value.set_sensitive(on_low_power)

    def on_minimum_backlight_changed(self, widget):
        minimum_backlight = self.minimum_backlight.get_value()
        maximum_backlight = self.maximum_backlight.get_value()
        if minimum_backlight >= maximum_backlight:
            self.minimum_backlight.set_value(maximum_backlight-1)

    def on_maximum_backlight_changed(self, widget):
        minimum_backlight = self.minimum_backlight.get_value()
        maximum_backlight = self.maximum_backlight.get_value()
        if maximum_backlight <= minimum_backlight:
            self.maximum_backlight.set_value(maximum_backlight+1)

    def on_backlight_changed(self, widget):
        bm = BacklightManager()
        bm.set_backlight(self.backlight.get_value())

    def messagedialog(self, title, message):
        dialog = Gtk.MessageDialog(None,
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.INFO,
                                   buttons=Gtk.ButtonsType.OK)
        dialog.set_markup("<b>%s</b>" % title)
        dialog.format_secondary_markup(message)
        dialog.run()
        dialog.destroy()

    def close_ok(self):
        self.hide()

    def load_preferences(self):
        configuration = Configuration()
        self.switch1.set_active(os.path.exists(comun.AUTOSTARTD))
        self.switch2.set_active(configuration.get('theme') == 'light')
        self.webcam_show.set_active(configuration.get('webcam-show'))
        self.webcam_onwidgettop.set_active(
            configuration.get('webcam-onwidgettop'))
        self.webcam_showintaskbar.set_active(
            configuration.get('webcam-showintaskbar'))
        self.webcam_onalldesktop.set_active(
            configuration.get('webcam-onalldesktop'))
        self.widgets = []
        cameras = configuration.get('cameras')
        for index, acamera in enumerate(cameras):
            data = {}
            vbox11 = Gtk.VBox(spacing=5)
            vbox11.set_border_width(5)
            ncamera = str(index + 1)
            self.notebook.append_page(
                vbox11, Gtk.Label.new(_('Camera') + ' ' + ncamera))
            frame11 = Gtk.Frame()
            vbox11.pack_start(frame11, False, True, 1)
            table11 = Gtk.Table(7, 2, False)
            frame11.add(table11)
            label11 = Gtk.Label(_('Url')+':')
            label11.set_alignment(0, 0.5)
            table11.attach(label11, 0, 1, 0, 1,
                           xpadding=5,
                           ypadding=5,
                           xoptions=Gtk.AttachOptions.FILL)
            data['url'] = Gtk.Entry()
            data['url'].set_width_chars(80)
            data['url'].set_sensitive(False)
            data['url'].set_text(acamera['url'])
            table11.attach(data['url'], 1, 2, 0, 1,
                           xpadding=5,
                           ypadding=5,
                           xoptions=Gtk.AttachOptions.FILL)
            label12 = Gtk.Label(_('Scale')+':')
            label12.set_alignment(0, 0.5)
            table11.attach(label12, 0, 1, 1, 2,
                           xpadding=5,
                           ypadding=5,
                           xoptions=Gtk.AttachOptions.FILL)
            data['scale'] = Gtk.SpinButton()
            data['scale'].set_adjustment(
                Gtk.Adjustment.new(acamera['scale'],
                                   1,
                                   101,
                                   1,
                                   10,
                                   1))
            table11.attach(data['scale'], 1, 2, 1, 2,
                           xpadding=5,
                           ypadding=5,
                           xoptions=Gtk.AttachOptions.SHRINK)
            label14 = Gtk.Label(_('Widget on top')+':')
            label14.set_alignment(0, 0.5)
            table11.attach(label14, 0, 1, 2, 3,
                           xpadding=5,
                           ypadding=5,
                           xoptions=Gtk.AttachOptions.FILL)
            data['onwidgettop'] = Gtk.Switch()
            data['onwidgettop'].set_active(acamera['onwidgettop'])
            table11.attach(data['onwidgettop'], 1, 2, 2, 3,
                           xpadding=5,
                           ypadding=5,
                           xoptions=Gtk.AttachOptions.SHRINK)
            label15 = Gtk.Label(_('Show in taskbar')+':')
            label15.set_alignment(0, 0.5)
            table11.attach(label15, 0, 1, 3, 4,
                           xpadding=5,
                           ypadding=5,
                           xoptions=Gtk.AttachOptions.FILL)
            data['showintaskbar'] = Gtk.Switch()
            data['showintaskbar'].set_active(acamera['showintaskbar'])
            table11.attach(data['showintaskbar'], 1, 2, 3, 4,
                           xpadding=5,
                           ypadding=5,
                           xoptions=Gtk.AttachOptions.SHRINK)
            label16 = Gtk.Label(_('Show on all desktop')+':')
            label16.set_alignment(0, 0.5)
            table11.attach(label16, 0, 1, 4, 5,
                           xpadding=5,
                           ypadding=5,
                           xoptions=Gtk.AttachOptions.FILL)
            data['onalldesktop'] = Gtk.Switch()
            data['onalldesktop'].set_active(acamera['onalldesktop'])
            table11.attach(data['onalldesktop'], 1, 2, 4, 5,
                           xpadding=5,
                           ypadding=5,
                           xoptions=Gtk.AttachOptions.SHRINK)
            label17 = Gtk.Label(_('Refresh time')+':')
            label17.set_alignment(0, 0.5)
            table11.attach(label17, 0, 1, 5, 6,
                           xpadding=5,
                           ypadding=5,
                           xoptions=Gtk.AttachOptions.FILL)
            data['refresh-time'] = Gtk.SpinButton()
            data['refresh-time'].set_adjustment(
                Gtk.Adjustment.new(acamera['refresh-time'],
                                   10,
                                   3600,
                                   10,
                                   50,
                                   10))
            table11.attach(data['refresh-time'], 1, 2, 5, 6,
                           xpadding=5,
                           ypadding=5,
                           xoptions=Gtk.AttachOptions.SHRINK)
            label17 = Gtk.Label(_('On')+':')
            label17.set_alignment(0, 0.5)
            table11.attach(label17, 0, 1, 6, 7,
                           xpadding=5,
                           ypadding=5,
                           xoptions=Gtk.AttachOptions.FILL)
            data['on'] = Gtk.Switch()
            if 'on' in acamera.keys():
                data['on'].set_active(acamera['on'])
            else:
                data['on'].set_active(True)
            table11.attach(data['on'], 1, 2, 6, 7,
                           xpadding=5,
                           ypadding=5,
                           xoptions=Gtk.AttachOptions.SHRINK)
            remove_button = Gtk.Button()
            remove_button.set_label(_('Remove camera') + ' ' + ncamera)
            remove_button.connect('clicked',
                                  self.on_remove_button_clicked)
            table11.attach(remove_button, 0, 2, 7, 8,
                           xpadding=5,
                           ypadding=5,
                           xoptions=Gtk.AttachOptions.SHRINK)
            self.widgets.append(data)

    def on_remove_button_clicked(self, widget):
        print(self.notebook.get_current_page())
        self.notebook.remove_page(self.notebook.get_current_page())

    def save_preferences(self):
        configuration = Configuration()
        cameras = configuration.get('cameras')
        create_or_remove_autostart(self.switch1.get_active())
        if self.switch2.get_active() is True:
            configuration.set('theme', 'light')
        else:
            configuration.set('theme', 'dark')
        configuration.set('webcam-show', self.webcam_show.get_active())
        configuration.set('webcam-onwidgettop',
                          self.webcam_onwidgettop.get_active())
        configuration.set('webcam-showintaskbar',
                          self.webcam_showintaskbar.get_active())
        configuration.set('webcam-onalldesktop',
                          self.webcam_onalldesktop.get_active())
        new_cameras = []
        for awidget in self.widgets:
            exists = False
            if len(awidget['url'].get_text()) > 0:
                for old_camera in cameras:
                    if old_camera['url'] == awidget['url'].get_text():
                        exists = True
                        old_camera['scale'] = awidget['scale'].get_value()
                        old_camera['onwidgettop'] =\
                            awidget['onwidgettop'].get_active()
                        old_camera['showintaskbar'] =\
                            awidget['showintaskbar'].get_active()
                        old_camera['onalldesktop'] =\
                            awidget['onalldesktop'].get_active()
                        old_camera['refresh-time'] =\
                            awidget['refresh-time'].get_value()
                        old_camera['on'] =\
                            awidget['on'].get_active()
                        new_cameras.append(old_camera)
                if exists is False:
                    new_camera = {}
                    new_camera['url'] = awidget['url'].get_text()
                    if not new_camera['url'].startswith('http://') and\
                            not new_camera['url'].startswith('https://'):
                        new_camera['url'] = 'http://' + new_camera['url']
                    new_camera['scale'] = awidget['scale'].get_value()
                    new_camera['x'] = 100
                    new_camera['y'] = 100
                    new_camera['onwidgettop'] = \
                        awidget['onwidgettop'].get_active()
                    new_camera['showintaskbar'] = \
                        awidget['showintaskbar'].get_active()
                    new_camera['onalldesktop'] = \
                        awidget['onalldesktop'].get_active()
                    new_camera['refresh-time'] = \
                        awidget['refresh-time'].get_value()
                    new_camera['on'] = \
                        awidget['on'].get_active()
                    new_cameras.append(new_camera)
        configuration.set('cameras', new_cameras)
        configuration.save()

if __name__ == "__main__":
    cm = PreferencesDialog()
    if cm.run() == Gtk.ResponseType.ACCEPT:
        print(1)
        cm.close_ok()
    cm.hide()
    cm.destroy()
    exit(0)

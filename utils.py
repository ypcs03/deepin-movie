#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Wang Yong
#
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty
from PyQt5.QtDBus import QDBusInterface, QDBusConnection


def _longest_match(*strs):
    shortest_str = min(strs, key=len)
    if all(x.startswith(shortest_str) for x in strs):
        yield shortest_str
    else:
        for idx, chr in enumerate(shortest_str):
            if all(x[idx] == chr for x in strs):
                yield chr
            else:
                break


def longest_match(*strs):
    return "".join(list(_longest_match(*strs)))


class Utils(QObject):

    """docstring for Utils"""

    def __init__(self):
        super(Utils, self).__init__()

    @pyqtProperty(str, constant=True)
    def homeDir(self):
        return os.path.expanduser("~")

    @pyqtSlot(str, result="QVariant")
    def getAllFilesInDir(self, dir):
        dir = dir[7:] if dir.startswith("file://") else dir
        result = []
        for entry in os.listdir(dir):
            file_abs_path = os.path.join(dir, entry)
            if os.path.isfile(file_abs_path):
                result.append(file_abs_path)
        return result

    # name should has no "file://" prefix
    @pyqtSlot(str, result=str)
    def getSeriesByName(self, name):
        dir = os.path.dirname(name)
        allFiles = self.getAllFilesInDir(dir)
        allFiles.remove(name)
        allFiles = [os.path.basename(x) for x in allFiles]
        nameFilter = min((longest_match(x, os.path.basename(name)) for x in allFiles),
                         key=len)

        result = filter(lambda x: nameFilter in x, allFiles)
        result = [os.path.join(dir, x) for x in result]

        return json.dumps({"name":nameFilter, "items":result})

    @pyqtSlot()
    def enable_zone(self):
        try:
            iface = QDBusInterface(
                "com.deepin.daemon.Zone", "/com/deepin/daemon/Zone", '', QDBusConnection.sessionBus())
            iface.asyncCall("EnableZoneDetected", True)
        except:
            pass

    @pyqtSlot()
    def disable_zone(self):
        try:
            iface = QDBusInterface(
                "com.deepin.daemon.Zone", "/com/deepin/daemon/Zone", '', QDBusConnection.sessionBus())
            iface.asyncCall("EnableZoneDetected", False)
        except:
            pass

    @pyqtSlot(int, int, str, result=bool)
    def checkKeySequenceEqual(self, modifier, key, targetKeySequence):
        return QKeySequence(modifier + key) == QKeySequence(targetKeySequence)

    @pyqtSlot(int, int, result=str)
    def keyEventToQKeySequenceString(self, modifier, key):
        return QKeySequence(modifier + key).toString()

    @pyqtSlot(str)
    def copyToClipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.clear(mode=clipboard.Clipboard)
        clipboard.setText(text, mode=clipboard.Clipboard)

utils = Utils()
if __name__ == '__main__':
    lst = [
        "权力的游戏.Game.of.Thrones.S04E01.中英字幕.HDTVrip.720x400.mp4",
        "权力的游戏.Game.of.Thrones.S04E02.中英字幕.HDTVrip.720x400.mp4",
        "权力的游戏.Game.of.Thrones.S04E03.中英字幕.HDTVrip.720x400.mp4",
        "权力的游戏.Game.of.Thrones.S04E04.中英字幕.HDTVrip.720x400.mp4",
        "权力的游戏.Game.of.Thrones.S04E05.中英字幕.HDTVrip.720x400.mp4",
        "权力的游戏.Game.of.Thrones.S04E06.中英字幕.HDTVrip.720x400.mp4",
        "权力的游戏.Game.of.Thrones.S04E07.中英字幕.HDTVrip.720x400.mp4",
        "权力的游戏.Game.of.Thrones.S04E07.中英字幕.HDTVrip.624x352.mp4",
    ]

    print longest_match(*lst)
    result = utils.getSeriesByName("/home/hualet/Videos/1000种死法第五季/1000种死法第五季-第5集.rmvb")
    print result
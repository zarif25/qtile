#!/bin/bash

feh --bg-scale ~/.config/qtile/wall.jpg &&

setsid org.telegram.desktop -startintray &>/dev/null &
setsid org.qbittorrent.qBittorrent &>/dev/null &
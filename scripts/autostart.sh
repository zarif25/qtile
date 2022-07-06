#!/bin/bash

feh --bg-scale ~/.config/qtile/wall.png &&

setsid org.telegram.desktop -startintray &>/dev/null &
setsid org.qbittorrent.qBittorrent &>/dev/null &
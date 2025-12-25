#!/bin/bash
#Desktop-session xdg build variables

function LOCATIONS {
LOCATION=$1
if [ ! -d "$LOCATION" ]; then
    say "Location does not exist; making"
    mkdir -p $LOCATION;
    chmod 0700 $LOCATION;
fi
}

#Make / Merge / Update xdg base directories

echo_variable XDG_DATA_HOME=${XDG_DATA_HOME:-"$HOME/.local/share"}
LOCATIONS "$HOME/.local/share"

echo_variable XDG_CONFIG_HOME=${XDG_CONFIG_HOME:-"$HOME/.config"}
LOCATIONS "$HOME/.config"

echo_variable XDG_STATE_HOME=${XDG_STATE_HOME:-"$HOME/.local/state"}
LOCATIONS "$HOME/.config"

echo_variable XDG_CACHE_HOME=${XDG_CACHE_HOME:-"$HOME/.cache"}
LOCATIONS "$HOME/.cache"

if [ -d "/run/user/$UID/" ]; then
    echo_variable XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-"/run/user/$UID/"}
else
    warn "Recommended runtime directory not available, attempting to make backup directory under /tmp\nThis should be removed at logout"
    LOCATIONS "/tmp/$UID/.run"
    echo_variable XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-"/tmp/$UID/.run"}
fi

echo_variable XDG_DATA_DIRS=${XDG_DATA_DIRS:-"/usr/local/share/:/usr/share/"}

echo_variable XDG_CONFIG_DIRS=${XDG_CONFIG_DIRS:-"/etc/xdg"}

echo_variable XDG_CURRENT_DESKTOP=$DESKTOP_SESSION_WM

#Make / merge / update xdg user directories
xdg-user-dirs-update

if [ -f ${XDG_CONFIG_HOME:-$HOME/.config}/user-dirs.dirs ]; then
    . ${XDG_CONFIG_HOME:-$HOME/.config}/user-dirs.dirs
    export XDG_DESKTOP_DIR XDG_DOWNLOAD_DIR XDG_TEMPLATES_DIR XDG_PUBLICSHARE_DIR XDG_DOCUMENTS_DIR XDG_MUSIC_DIR XDG_PICTURES_DIR XDG_VIDEOS_DIR
fi

if [ -f $XDG_DATA_HOME/applications/mimeinfo.cache ]; then
    warn "Depreciated mime database left: Recommend removing $XDG_DATA_HOME/applications/mimeinfo.cache as this file should not be used to set defaults";
fi

if [ -f  $XDG_DATA_HOME/applications/defaults.list ]; then
    warn "Depreciated mime database left: Recommend removing $XDG_DATA_HOME/applications/defaults.list";
fi

if [ ! -f $XDG_DATA_HOME/applications/mimeapps.list ]; then
    say "Linking  $XDG_DATA_HOME/applications/mimeapps.list with $XDG_CONFIG_HOME/mimeapps.list";
    ln -s $XDG_CONFIG_HOME/mimeapps.list $XDG_DATA_HOME/applications/mimeapps.list;
elif [ -f  $XDG_DATA_HOME/applications/mimeapps.list ] && [ ! -L $XDG_DATA_HOME/applications/mimeapps.list ]; then
    warn "Depreciated mime database left: Recommend removing $XDG_DATA_HOME/applications/mimeapps.list and replacing it with a symlink to $XDG_CONFIG_HOME/mimeapps.list";
else    
    if [ "$(readlink -f  $XDG_DATA_HOME/applications/mimeapps.list)" != "$XDG_CONFIG_HOME/mimeapps.list" ]; then
        warn "$XDG_DATA_HOME/applications/mimeapps.list not linked with  $XDG_CONFIG_HOME/mimeapps.list. Suggest changing the link to point to $XDG_CONFIG_HOME/mimeapps.list";
    fi
fi

#Xport the gtkrc files
export GTK2_RC_FILES="$HOME/.gtkrc-2.0"

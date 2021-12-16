#!/bin/bash

mv ~/.zprofile ~/.zprofile-old
ln -s ~/dotfiles/.zprofile ~/.zprofile

mv ~/Library/Application\ Support/Code/User/settings.json ~/Library/Application\ Support/Code/User/settings-old.json
ln -s ~/dotfiles/.vscode ~/Library/Application\ Support/Code/User/settings.json

cat ~/dotfiles/.gitalias >> ~/.gitconfig

touch ~/dotfiles/command/_local.sh

if ! [ $SPIN ]; then
    mkdir -p ~/dotfiles/script
    mkdir -p ~/dotfiles/data

    working_dir=$PWD

    for plugin in ~/dotfiles/streamdeck/*; do
        cd $plugin
        ln -s $plugin ~/Library/Application\ Support/com.elgato.StreamDeck/Plugins/
        $plugin/install.sh
    done

    cd $working_dir
fi

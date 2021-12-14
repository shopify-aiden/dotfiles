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
fi

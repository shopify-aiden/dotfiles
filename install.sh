#!/bin/bash

ln -s ~/dotfiles/.zprofile ~/.zprofile
ln -s ~/dotfiles/.vscode ~/Library/Application\ Support/Code/User/settings.json
cat ~/dotfiles/.gitalias >> ~/.gitconfig

if [ "$SPIN" ]; then
else
    mkdir -p ~/dotfiles/script
fi

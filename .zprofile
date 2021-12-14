source ~/dotfiles/variable.sh

source ~/dotfiles/command/_alias.sh
source ~/dotfiles/command/_common.sh

if ! [ $SPIN ]; then
    for script in ~/dotfiles/script/*; do
        alias ${${script##*/}%%.py}="python3 $script"
    done
fi

source ~/dotfiles/command/_local.sh

if ! [ $SPIN ]; then
    source ~/dotfiles/command/_mac.sh
else
    source ~/dotfiles/command/_spin.sh
fi

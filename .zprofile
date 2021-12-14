source ~/dotfiles/variable.sh

source ~/dotfiles/command/_alias.sh
source ~/dotfiles/command/_common.sh

if [ "$SPIN" ]; then
    source ~/dotfiles/command/_spin.sh
else
    source ~/dotfiles/command/_local.sh
    for script in ~/dotfiles/script*; do alias ${${script##*/}%%.py}="$script"
fi

alias slack="open -a 'Slack'"
alias spotify="open -a'Spotify'"


chrome() {
    open -a "Google Chrome" $@
}


dot() {
    code ~/dotfiles
}


start() {
    chrome
    slack
    spotify

    if ! [ -x "$(command -v script_start)" ]; then
        script_start
    fi
}


silent() {
    nohup $@ > /dev/null 2>&1 &iter
}
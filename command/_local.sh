alias slack="open -a 'Slack'"
alias spotify="open -a'Spotify'"


chrome() {
    open -a "Chrome" $@
}


dot() {
    code ~/dotfiles
}


start() {
    chrome
    slack
    spotify
}


silent() {
    nohup $@ > /dev/null 2>&1 &iter
}

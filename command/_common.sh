d64() {
    echo -n $1 | base64 -D
    echo
}

e64() {
    echo -n $1 | base64
}

#!/bin/sh
wget -qO- http://sms2.personal.com.ar/Mensajes/sms.php|awk -v RS="\"" '
    /http.*?tmp/{system("wget \"" $0 "\"")}'

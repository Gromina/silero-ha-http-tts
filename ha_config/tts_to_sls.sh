#!/bin/bash

url=`curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "INPUT_TEXT='$3'" $1/tts | grep -oP '"url":"\K([^"]*)'`
curl -X GET "$2/api/audio?action=play&url=$url"

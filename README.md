# silero-ha-http-tts


## todo

- [x] docker packaging
- [x] make initial server
- [x] silero package working
- [x] TTS code itself
- [x] caching of TTS results in local filesystem
- [x] ML models cached in docker
- [ ] Normalize text
- [x] server implements HA TTS API (MaryTTS)
- [x] make docs how to run it all with HA
- [ ] respect voice, language parameters

## Endpoints

POST /process - MaryTTS format endpoint returning wav file. Used when setup as HA TTS service

POST /tts - just get url to generated wav file

## I took some ideas from

* https://github.com/elia-morrison/silero_docker


## HA config
```
tts:
  - platform: marytts
    host: localhost
    port: 9898
    codec: WAVE_FILE
    voice: xenia
    language: ru
```

## curl test

```
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "INPUT_TEXT=Привет" http://127.1:9898/tts
```

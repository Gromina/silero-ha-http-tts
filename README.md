# silero-ha-http-tts


## todo

- [x] docker packaging
- [x] make initial server
- [x] silero package working
- [x] TTS code itself
- [x] caching of TTS results in local filesystem
- [x] ML models cached in docker
- [ ] Normalize text
- [ ] server implements HA TTS HTTP API https://www.home-assistant.io/integrations/tts/
- [ ] make docs how to run it all with HA



## I took some ideas from

* https://github.com/elia-morrison/silero_docker

## example request for testing

```
curl -X POST -d '{"text":"жопа с ручкой"}'  -H  "accept: application/json" -H  "Content-Type: application/json" http://localhost:9898/api
```

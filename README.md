# silero-ha-http-tts
Этот проект я сделал для себя, чтобы обеспечить свой умный дом синтезом речи, который может работать автономно, без облачных провайдеров.
На текущий момент работает:
- Непосредственно синтез речи при помощи моделей [silero](https://github.com/snakers4/silero-models)
- Силеро не умеет (почему?) норнмализовывать текст, поэтому пришлось сделать свою нормализацию при помощи [Natasha](https://github.com/natasha/natasha) & [pymorphy](https://github.com/kmike/pymorphy2). На текущий момент нормализуется только температура (число в текст)
- докер контейнер выдает два эндпойнта. Один - для встроенного TTS Home Assistant, второй - чтобы получить звуковой файл непосредственно. 
- проигрывание звука в SLS шлюз. Пришлось сделать кривовато, но работает

Что еще предстоит, или чего нет:
- Не разобрался с media-source в Home Assitant - если нужно в итоге в автоматизации получить рабочий URL, не знаю, как это сделать
- Голос говорящего захаркожен
- Эффект эха захаркожен
- качество синтеза захардкожено
- образ контейнера собирается локально, не загружается на DockerHub
- захардкожены паузы в начале и конце (SLS шлюз шипит на старте и финише)
- Синтез работает на x64 архитектуре. На малинке крашится, пока не разбирался (вероятно, силеро не работает)
- синтезированные файлы остаются в контейнере и никак не чистятся (кроме перезапуска контейнера)

## todo

- [x] docker packaging
- [x] make initial server
- [x] silero package working
- [x] TTS code itself
- [x] caching of TTS results in local filesystem
- [x] ML models cached in docker
- [x] Normalize text
- [x] server implements HA TTS API (MaryTTS)
- [x] make docs how to run it all with HA
- [ ] respect voice, language parameters
- [ ] make DockerHub image
- [ ] parse humidity, dates, just numbers in normalization
- [ ] make cache cleanups

## How to run

```hash
git clone https://github.com/Gromina/silero-ha-http-tts.git
cd silero-ha-http-tts.git

make && make run # which is shortcut for 2 following lines
# docker build -t silero .
# docker run -p 9898:80 --rm --name tts_silero silero

## Endpoints

POST /process - MaryTTS format endpoint returning wav file. Used when setup as HA TTS service

POST /tts - just get url to generated wav file

## I took some ideas from

* https://github.com/elia-morrison/silero_docker


## HA config to work as TTS
```
tts:
  - platform: marytts
    host: localhost
    port: 9898
    codec: WAVE_FILE
    voice: xenia
    language: ru
```
## HA config to use with [SLS gateway](https://slsys.github.io/Gateway/README_rus.html)

Put script from ./ha_config to your HA config folder

Make shell command in HA config:

```yaml
shell_command:
        tts_to_sls: './tts_to_sls.sh "{{ tts_address }}" "{{ sls_address }}" "{{ text}}" '
```

Add following automation (write down correct IP addresses for TTS service and SLS)

```yaml
- id: '1667401859473'
  alias: Speak status
  description: ''
  trigger: []
  condition: []
  action:
  - service: shell_command.tts_to_sls
    data_template:
      tts_address: http://192.111.11.111:9898
      sls_address: http://192.111.11.190
      text: Привет, шеф! В комнате 12
        градусов. В то же время на улице -23
        градусов
  mode: single
```


## curl test

```
curl -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "INPUT_TEXT=Привет" http://127.1:9898/tts
```

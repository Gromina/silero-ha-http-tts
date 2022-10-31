build:
	docker build -t silero .
run:
	docker run -p 9898:80 --rm --name tts_silero silero

# README

Website: [https://hub.docker.com/r/voicevox/voicevox_engine](https://hub.docker.com/r/voicevox/voicevox_engine)

```
docker pull voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
```

```
docker run --rm --gpus all -p 50021:50021 voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
```
# Opengl algorithm for hkube
Renders a triangle and returns it as JPG

## build
```console
docker build -t yehiyam/opengl-alg:v0.0.2 -f Dockerfile  .
```
## local run (openGL)
```console
docker run --rm -it  --runtime=nvidia -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY -e XAUTHORITY -e NVIDIA_DRIVER_CAPABILITIES=all -e WORKER_BINARY=true -e WORKER_SOCKET_URL=ws://hkube-myproject.10.42.128.41.nip.io/hkube/debug/ogl yehiyam/opengl-alg:v0.0.3
```

## localrun (egl)
```console
docker run --rm -it  --runtime=nvidia  -e USE_EGL=true -e WORKER_BINARY=true -e WORKER_SOCKET_URL=ws://hkube-myproject.10.42.128.41.nip.io/hkube/debug/ogl yehiyam/opengl-alg:v0.0.3
```
## algorithm definition (OpenGL)
```yaml
{
    "name": "opengl-alg",
    "cpu": 1,
    "gpu": 0.1,
    "mem": "256Mi",
    "minHotWorkers": 0,
    "options": {
        "opengl": true,
        "binary": true
    },
    "algorithmImage": "yehiyam/opengl-alg:v0.0.3",
    "type": "Image"
}
```

## algorithm definition (egl)
```yaml
{
    "name": "opengl-alg",
    "cpu": 1,
    "gpu": 0.1,
    "mem": "256Mi",
    "minHotWorkers": 0,
    "options": {
        "binary": true
    },
    "algorithmImage": "yehiyam/opengl-alg:v0.0.3",
    "type": "Image"
}
```

## flowInput (optional)
```json
{
    "width":512,
    "height":512,
    "sleep":5
}
```

## decode result from bson
```console
pip install pymongo
```

```console
python decode.py path_to_bson_data result.buffer out.jpg
```

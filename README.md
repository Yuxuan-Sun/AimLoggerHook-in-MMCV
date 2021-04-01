# AimLoggerHook-in-MMCV

This is a walkthrough of using aim in mmcv.

aim github repo: [https://github.com/aimhubio/aim#track](https://github.com/aimhubio/aim#track)

# install docker

docker is required to launch aim UI

official tutorial : [https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)  

or you could just copy n paste the followings (should be alright

```bash
# delete old version, it's okay if noth happen (it just means you didn't install any of them
$ sudo apt-get remove docker docker-engine docker.io containerd runc
# set up the repo so that you could install & update docker in the repo in the future
$ sudo apt-get update
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
# add docker's offical GPG key
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
# stable repo
$ echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# install docker engine
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
# test whether you've installed it successfully
$ sudo docker run hello-world
```

run the following python code

```python
import docker
client = docker.from_env()
client.ping()
```

if you see `requests.exceptions.ConnectionError: ('Connection aborted.', PermissionError(13, 'Permission denied'))` it's because docker daemon requires superuser privilege. Following commands will allow non-root users to have access as well.

```bash
$ sudo usermod -aG docker $USER
$ sudo systemctl restart docker
restart your shell
```

Ensure installation is completed by re-running the 3-lines python code. 

# AimLoggerHook

enter`mmcv/runner/hooks/logger/`（depending on where you install mmcv, the following is my path

```bash
$ cd /home/sunyx30/anaconda3/lib/python3.8/site-packages/mmcv/runner/hooks/logger/
$ git clone https://github.com/Yuxuan-Sun/AimLoggerHook-in-MMDet.git
# copy aim.py to /hooks/logger
$ cp AimLoggerHook-in-MMDet/aim.py .
```

**the 'hparam' is self-defined in aim.py, remember to modify it according to your model**


remember to add `AimLoggerHook` in `__init__.py` 

## config

change your `log_config` in config file as sth like the following

```python
log_config = dict(
    interval=50, 
    hooks=[
        dict(type='TextLoggerHook'),
        dict(type='AimLoggerHook')])
```

# run aim

```bash
$ aim init
# train model as usual, the following is my command 
$ CUDA_VISIBLE_DEVICES=1,2,3 PORT=29501 tools/dist_train.sh configs/datatang/retinanet_repvgg_fpn.py 3
$ aim up
# remember to execute `aim init` and `aim up` in the same directory
```

then you should see sth like 

```bash
┌--------------------------------------------------------┐
        Aim UI collects anonymous usage analytics.
                Read how to opt-out here:
   https://github.com/aimhubio/aim#anonymized-telemetry
└--------------------------------------------------------┘
Running Aim UI on repo `/home/sunyx30/datatang_hand_detection/.aim`
Open http://127.0.0.1:43800
Press Ctrl+C to exit
```

# view aim UI locally

```bash
ssh -N -f -L localhost:8888:localhost:43800 remoteUser@remoteIP
```

after entering your server password, just enter  `[localhost:8888](http://localhost:8888)`  in you local browser. (You could change the port as you desire)
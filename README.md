# FileCheckMate
## Setup
```bash
$ git clone https://github.com/patr1ckbat3man/FileCheckMate.git
$ python3 -m venv env
$ source env/bin/activate
$ (env) python3 -m pip install -r requirements.txt 
```
## Redis
You can either run redis through a docker container or download it directly. For the second option:
```editorconfig
port              6379
daemonize         yes
save              60 1
bind              127.0.0.1
tcp-keepalive     300
dbfilename        dump.rdb
dir               ./
rdbcompression    yes
```
Copy this and create a 6379.conf file
```bash
$ mkdir -p /etc/redis/
$ mv 6379.conf /etc/redis
```
Run your redis server and check if everything works
```bash
redis-server /etc/redis/6379.conf
redis-cli
127.0.0.1:6379> PING
```
If you get an output saying PONG, you are ready to start using the monitoring script.
Run your app:
```bash
chmod +x main.py
./main.py
```
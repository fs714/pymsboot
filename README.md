Python Micro Service Example Project

### 1. How to start this demo
1. Start RabbitMQ
    ```
    docker run -d --restart=always --name rabbitmq --hostname rabbitmq -p 4369:4369 -p 5671:5671 -p 5672:5672 -p 25672:25672 -p 15671:15671 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=guest -e RABBITMQ_DEFAULT_PASS=guest rabbitmq:3.7.6-management-alpine
    ```
2. Install this project
```
# cd to this project folder
python setup.py install
```
3. Start API Service
```
pymsboot-api --config-file=pymsboot.conf
```
4. Start Engine Service
```
pymsboot-engine --config-file=pymsboot.conf
```

### 1. Generate conf file
```
oslo-config-generator \
--namespace pymsboot.config \
--namespace oslo.config \
--namespace oslo.log \
--namespace oslo.concurrency \
--namespace oslo.service.service \
--namespace oslo.service.periodic_task \
--namespace oslo.service.sslutils \
--namespace oslo.service.wsgi \
--namespace oslo.messaging
```

Update
```
transport_url = rabbit://guest:guest@127.0.0.1:5672//
```

### 2. Restful API Server

URL | Method | Usage
--- | --- | ---
/v1/movies | GET | Get all movies information
/v1/movies | POST | Add one new movie information
/v1/movies/<UUID> | GET | Get one movie information by UUID
/v1/movies/<UUID> | PUT | Update one movie information by UUID
/v1/movies/<UUID> | DELETE | Delete one movie information by UUID

### 3. RPC Service

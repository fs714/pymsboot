Python Micro Service Example Project

## 1. Architecture
### 1.1 Overview
Pymsboot includes 2 separated services:
- pymsboot-api
  - API Gateway
  - Interact with pymsboot-engine by RPC through RabbitMQ
  - Support multi process in one instance by Eventlet + Multiprocess
  - Support scale out to multi instances
- pymsboot-engine
  - Listening RPC message from RabbitMQ as RPC Server
  - Interact with Database
  - Support multi process in one instance by Eventlet + Multiprocess
  - Support scale out to multi instances

Pymsboot refer to OpenStack architecture which has been proved by thousands of production deployments in past years. Follow
OpenStack projects could be a good reference:
- Magnum
- Ironic
- Zun

### 1.2 Configuration
This project use oslo_config to manage the project configuration.
- Prerequisite
  Install this project by follow command
  ```
  python setup.py install
  ```

  > To clean the installation, use ```python setup.py clean --all```

- Generate original conf file
  ```
  oslo-config-generator \
  --namespace pymsboot.config \
  --namespace oslo.concurrency \
  --namespace oslo.config \
  --namespace oslo.db \
  --namespace oslo.db.concurrency \
  --namespace oslo.log \
  --namespace oslo.messaging \
  --namespace oslo.service.service \
  --namespace oslo.service.periodic_task \
  --namespace oslo.service.sslutils \
  --namespace oslo.service.wsgi \
  ```

- Frequently used configuration
  ```
  [DEFAULT]
  transport_url = rabbit://guest:guest@127.0.0.1:5672//

  [api]
  #host = 0.0.0.0
  #port = 9666
  api_workers = 2

  [database]
  connection = postgresql+psycopg2://user:addr:5432/db_name

  [engine]
  #host = 0.0.0.0
  #topic = pymsboot_engine
  engine_workers = 1
  ```

## 2. Deployment
Currently 2 methods are recommended for pymsboot deployment and testing. Container based deployment should be used for
production.

### 2.1 Start Pymsboot by Script
- Start RabbitMQ
  ```
  docker run -d --restart=always --name rabbitmq --hostname rabbitmq -p 4369:4369 -p 5671:5671 -p 5672:5672 -p 25672:25672 -p 15671:15671 -p 15672:15672 -e RABBITMQ_DEFAULT_USER=guest -e RABBITMQ_DEFAULT_PASS=guest rabbitmq:3.7.6-management-alpine
  ```
- Start Pymsboot Engine Service
  ```
  # cd to project folder
  python start_engine.py --config-file=conf/pymsboot.conf
  ```
- Start Pymsboot API Service
  ```
  # cd to project folder
  python start_api.py --config-file=conf/pymsboot.conf
  ```

### 2.2 Start Pymsboot by Docker
- Start RabbitMQ
  ```
  # cd to project folder
  docker-compose -f compose/rabbitmq.yml up -d
  ```
- Prepare ENV (One-time)
  ```
  # cd to project folder
  mkdir -p /etc/pymsboot
  mkdir -p /var/log/pymsboot
  cp conf/pymsboot.conf /etc/pymsboot
  ```
  - Edit /etc/pymsboot according to your ENV.
  - Edit compose/pymsboot.yml according to yoyr ENV
- Start Pymsboot
  ```
  # cd to project folder
  docker-compose -f compose/pymsboot.yml up -d
  ```

### 2.3 Log Rotation
Linux system logrotate should be used for log rotate for production.
```
# cd to project folder
cp resources/pymsboot_log_rotate /etc/logrotate.d/
```

### 3. Restful API Server

URL | Method | Usage
--- | --- | ---
/v1/movies | GET | Get all movies information
/v1/movies | POST | Add one new movie and download it
/v1/movies/<UUID> | GET | Get one movie information by UUID
/v1/movies/<UUID> | PUT | Update one movie information by UUID
/v1/movies/<UUID> | DELETE | Delete one movie information by UUID

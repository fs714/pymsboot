Python Micro Service Example Project

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

### 2. Restful API Server

URL | Method | Usage
--- | --- | ---
/v1/movies | GET | Get all movies information
/v1/movies | POST | Add one new movie information
/v1/movies/<UUID> | GET | Get one movie information by UUID
/v1/movies/<UUID> | PUT | Update one movie information by UUID
/v1/movies/<UUID> | DELETE | Delete one movie information by UUID

### 3. RPC Service

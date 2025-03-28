# Лабораторная работа №5

# Цель лабораторной работы
Освоить запуск полноценного веб-приложения из разных репозиториев. Приложение должно содержать фронтенд и бэкэнд части из соответствующих репозиториев. Компоуз-файл должен запускать базу данных для приложения, и обратный прокси nginx.

# Реализация

1. Образы должены быть легковесными

Выполним команду `docker ps -a --filter "name=devops_labs_2" --size`, чтобы оценить занимаемый ими объём:
```
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS          PORTS                  NAMES                         SIZE
e8ed5556e08b   nginx:1.25-alpine        "/docker-entrypoint.…"   10 minutes ago   Up 24 seconds   0.0.0.0:3000->80/tcp   devops_labs_2-nginx-proxy-1   2B (virtual 49.7MB)
27fdadb5c4ca   devops_labs_2-frontend   "docker-entrypoint.s…"   10 minutes ago   Up 24 seconds                          devops_labs_2-frontend-1      13MB (virtual 611MB)
9dde45f0d920   devops_labs_2-backend    "/__cacert_entrypoin…"   10 minutes ago   Up 25 seconds                          devops_labs_2-backend-1       32.8kB (virtual 425MB)
3f9d1d82c2d4   postgres:16-alpine       "docker-entrypoint.s…"   10 minutes ago   Up 25 seconds   5432/tcp               devops_labs_2-db-1            63B (virtual 267MB)
```

Вес фронтенд-образа объясним тем, что он основан на Node.js и включает в себя весь проект с исходниками, установленными зависимостями и собранным билдом. Большую часть веса занимают `node_modules`, где хранятся библиотеки, нужные для сборки и работы приложения.

2. Использовать базовые легковестные образы - alpine

Исипользуем для:
- `nginx-proxy` — `nginx:1.25-alpine`
- `db` — `postgres:16-alpine`
- `backend` — `eclipse-temurin:21-jdk-alpine`
- `frontend` — `node:20-alpine`

3. Учесть запуск `backend`, `frontend`, `db` и `nginx-proxy`

В docker-compose.yml описаны четыре сервиса - backend, frontend, db и nginx-proxy. Каждый контейнер работает в своей среде и нет лишнего проброса портов:
```
ports:
  - "80:80"  # только у nginx-proxy

```

Остальные сервисы взаимодействуют только внутри Docker-сети:
- `frontend` -> `backend` по `http://backend:8080`
- `nginx` -> `frontend` по `http://frontend:3000`
- `nginx` -> `backend` по `http://backend:8080`
- `backend` -> `db` по `postgres://db:5432`

4. Вся конфигурация выполняется через переменные окружения, передающиеся через `env_file` и `environment`

Все переменные вынесены в `.env`:
```
APP_DOMAIN=localhost
FRONTEND_PORT=3000
BACKEND_PORT=5000
DB_USER=appuser
DB_PASSWORD=secret
DB_NAME=appdb
MYSQL_PORT=5432
```
В docker-compose.yml используется: `env_file: .env`.

6. Точкой входа является только `nginx-proxy`, остальные сервисы не имеют открытых наружу портов

Только nginx-proxy публикует порт наружу:
```
ports:
  - "80:80"
```
Остальные сервисы не имеют открытых портов.

8. Должна быть возможность конфигурирования через файлы настроек в виде `volume`

Примонтированы конфигурационные файлы и директории:
- nginx-proxy:
```
volumes:
  - ./nginx/default.conf:/etc/nginx/conf.d/default.conf:ro
  - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
  - ./nginx/cache:/var/cache/nginx
```
- frontend:
```
volumes:
  - ./frontend:/app
  - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
  - ./nginx/cache:/var/cache/nginx
```
9. Контейнеры должены запускатьсь от непривилегированного пользователя
В Dockerfile:
```
RUN adduser -D appuser
USER appuser
```

В docker-compose.yml: `user: "1000:1000"`

11. После установки всех нужных утилит, должен очищаться кеш

В frontend/Dockerfile:
```
RUN npm install && npm run build && npm cache clean --force
```

# Запуск контейнеров
Все сервисы успешно стартовали, и они взаимодействуют друг с другом через Docker-сеть. Контейнер nginx-proxy работает как точка входа и проксирует трафик к остальным сервисам:
```
Container devops_labs_2-db-1           Created                                                                                                                                           0.0s 
 ✔ Container devops_labs_2-backend-1      Created                                                                                                                                           0.0s 
 ✔ Container devops_labs_2-frontend-1     Created                                                                                                                                           0.0s 
 ✔ Container devops_labs_2-nginx-proxy-1  Created                                                                                                                                           0.0s 
Attaching to devops_labs_2-backend-1, devops_labs_2-db-1, devops_labs_2-frontend-1, devops_labs_2-nginx-proxy-1
devops_labs_2-db-1           | 
devops_labs_2-db-1           | PostgreSQL Database directory appears to contain a database; Skipping initialization
devops_labs_2-db-1           | 
devops_labs_2-db-1           | 2025-03-28 21:10:57.851 UTC [1] LOG:  starting PostgreSQL 16.8 on aarch64-unknown-linux-musl, compiled by gcc (Alpine 14.2.0) 14.2.0, 64-bit
devops_labs_2-db-1           | 2025-03-28 21:10:57.851 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
devops_labs_2-db-1           | 2025-03-28 21:10:57.851 UTC [1] LOG:  listening on IPv6 address "::", port 5432
devops_labs_2-db-1           | 2025-03-28 21:10:57.858 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
devops_labs_2-db-1           | 2025-03-28 21:10:57.860 UTC [29] LOG:  database system was shut down at 2025-03-28 21:10:54 UTC
devops_labs_2-db-1           | 2025-03-28 21:10:57.863 UTC [1] LOG:  database system is ready to accept connections
devops_labs_2-nginx-proxy-1  | /docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
devops_labs_2-nginx-proxy-1  | /docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
devops_labs_2-nginx-proxy-1  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
devops_labs_2-nginx-proxy-1  | 10-listen-on-ipv6-by-default.sh: info: can not modify /etc/nginx/conf.d/default.conf (read-only file system?)
devops_labs_2-nginx-proxy-1  | /docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
devops_labs_2-nginx-proxy-1  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
devops_labs_2-nginx-proxy-1  | /docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
devops_labs_2-nginx-proxy-1  | /docker-entrypoint.sh: Configuration complete; ready for start up
devops_labs_2-nginx-proxy-1  | 2025/03/28 21:10:58 [warn] 1#1: the "user" directive makes sense only if the master process runs with super-user privileges, ignored in /etc/nginx/nginx.conf:1
devops_labs_2-nginx-proxy-1  | nginx: [warn] the "user" directive makes sense only if the master process runs with super-user privileges, ignored in /etc/nginx/nginx.conf:1
devops_labs_2-backend-1      | 
devops_labs_2-backend-1      |   .   ____          _            __ _ _
devops_labs_2-backend-1      |  /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
devops_labs_2-backend-1      | ( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
devops_labs_2-backend-1      |  \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
devops_labs_2-backend-1      |   '  |____| .__|_| |_|_| |_\__, | / / / /
devops_labs_2-backend-1      |  =========|_|==============|___/=/_/_/_/
devops_labs_2-backend-1      |  :: Spring Boot ::                (v2.4.2)
devops_labs_2-backend-1      | 
devops_labs_2-backend-1      | 2025-03-28 21:10:58.811  INFO 1 --- [           main] b.h.HobbieBackendApplication             : Starting HobbieBackendApplication v0.0.1-SNAPSHOT using Java 21.0.6 on 9dde45f0d920 with PID 1 (/app/app.jar started by appuser in /app)
devops_labs_2-backend-1      | 2025-03-28 21:10:58.812  INFO 1 --- [           main] b.h.HobbieBackendApplication             : No active profile set, falling back to default profiles: default
devops_labs_2-frontend-1     |  INFO  Accepting connections at http://localhost:3000
devops_labs_2-backend-1      | 2025-03-28 21:10:59.751  INFO 1 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Bootstrapping Spring Data JPA repositories in DEFAULT mode.
devops_labs_2-backend-1      | 2025-03-28 21:10:59.828  INFO 1 --- [           main] .s.d.r.c.RepositoryConfigurationDelegate : Finished Spring Data repository scanning in 69 ms. Found 8 JPA repository interfaces.
devops_labs_2-backend-1      | 2025-03-28 21:11:00.449  INFO 1 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat initialized with port(s): 5000 (http)
devops_labs_2-backend-1      | 2025-03-28 21:11:00.456  INFO 1 --- [           main] o.apache.catalina.core.StandardService   : Starting service [Tomcat]
devops_labs_2-backend-1      | 2025-03-28 21:11:00.456  INFO 1 --- [           main] org.apache.catalina.core.StandardEngine  : Starting Servlet engine: [Apache Tomcat/9.0.41]
devops_labs_2-backend-1      | 2025-03-28 21:11:00.487  INFO 1 --- [           main] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
devops_labs_2-backend-1      | 2025-03-28 21:11:00.487  INFO 1 --- [           main] w.s.c.ServletWebServerApplicationContext : Root WebApplicationContext: initialization completed in 1640 ms
devops_labs_2-backend-1      | 2025-03-28 21:11:00.704  INFO 1 --- [           main] o.hibernate.jpa.internal.util.LogHelper  : HHH000204: Processing PersistenceUnitInfo [name: default]
devops_labs_2-backend-1      | 2025-03-28 21:11:00.743  INFO 1 --- [           main] org.hibernate.Version                    : HHH000412: Hibernate ORM core version 5.4.27.Final
devops_labs_2-backend-1      | 2025-03-28 21:11:00.842  INFO 1 --- [           main] o.hibernate.annotations.common.Version   : HCANN000001: Hibernate Commons Annotations {5.1.2.Final}
devops_labs_2-backend-1      | 2025-03-28 21:11:00.906  INFO 1 --- [           main] com.zaxxer.hikari.HikariDataSource       : HikariPool-1 - Starting...
```

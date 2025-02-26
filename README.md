# Лабораторная №2

## Цель лабораторной
Собрать из исходного когда и запустить в докере рабочее приложение с базой данных (любое опенсорс - Java, python/django/flask, golang).

## Реализация
1. Образ должен быть легковесным
   
Используем вместо стандартного python:3.11 (~900MB) используем python:3.11-alpine (~30MB) <img width="209" alt="Снимок экрана 2025-02-27 в 00 35 25" src="https://github.com/user-attachments/assets/2a65d4fb-fa44-4bbe-a6a4-9d6d53123cf8" />

2. Использовать базовые легковестные образы - alpine

`Alpine Linux` — это легковесный дистрибутив Linux (~5MB), который минимизирует размер образов и уменьшает уязвимости.

При этом он совместим со стандартными инструментами, такими как `apt`, `apk`, `pip`, `npm` и т. д.

3. Вся конфигурация приложения должна быть через переменные окружения
   
Конфигурация приложения (логин, пароли, пути) передаются через переменные окружения:
<img width="794" alt="Снимок экрана 2025-02-27 в 00 39 36" src="https://github.com/user-attachments/assets/3e8314b6-5396-421b-9dc9-963cd3898293" />

И используются в `docker-compose.yml`:

<img width="325" alt="Снимок экрана 2025-02-27 в 00 44 03" src="https://github.com/user-attachments/assets/bd71edaf-ebdc-4e8e-a4aa-be115be2140b" />

4. Статика (зависимости) должна быть внешним томом `volume`

В `docker-compose.yml` подключаем volume для хранения базы данных:

<img width="331" alt="Снимок экрана 2025-02-27 в 00 47 38" src="https://github.com/user-attachments/assets/4f921d57-0c30-403b-8737-66d4a19b8a15" />

Теперь даже при перезапуске контейнера база не исчезнет.

5. Создать файл `docker-compose` для старта и сборки

Создан файл `docker-compose` в корне проекта:

<img width="613" alt="Снимок экрана 2025-02-27 в 00 49 12" src="https://github.com/user-attachments/assets/fc836dc4-aafb-43d3-8256-70eb1f7005b2" />

Для запуска можно использовать команду: `docker-compose up -d`

6. В `docker-compose` нужно использовать базу данных (postgresql,mysql,mongodb etc.)

Используем базу данных PostgreSQL:

<img width="360" alt="Снимок экрана 2025-02-27 в 00 50 30" src="https://github.com/user-attachments/assets/f95a015f-9a7b-4de9-be92-1a793fe45648" />
  
7. При старте приложения должно быть учтено выполнение автоматических миграций

<img width="402" alt="Снимок экрана 2025-02-27 в 00 53 11" src="https://github.com/user-attachments/assets/38ec1410-abc9-4286-8eb3-b206ec5a3085" />


  
8. Контейнер должен запускаться от непривилегированного пользователя

Создаем непривилегированного пользователя:

<img width="427" alt="Снимок экрана 2025-02-27 в 01 14 31" src="https://github.com/user-attachments/assets/30bb8379-13d1-4b3f-b2c7-f0da348f392c" />

9. После установки всех нужных утилит, должен очищаться кеш

Удаляем кэш после установки зависимостей:

<img width="235" alt="Снимок экрана 2025-02-27 в 01 15 58" src="https://github.com/user-attachments/assets/5ec50a92-9fe1-4d6c-b48f-faaa4229f06f" />

Выполняем команду `docker-compose build`:

<img width="1096" alt="Снимок экрана 2025-02-27 в 01 00 35" src="https://github.com/user-attachments/assets/8dedf56c-f01c-43fa-914f-7317b52ec65c" />

Выполняем команду `docker-compose up -d`:

<img width="613" alt="Снимок экрана 2025-02-27 в 01 01 06" src="https://github.com/user-attachments/assets/de3abfff-d4a6-4ea6-9e25-be405f92412b" />





# Лабораторная №1

## Цель
Запустить в докере рабочий веб-сервер nginx

## Реализация

1. Создать образ mynginx, который будет запускать nginx внутри контейнера

<img width="333" alt="Снимок экрана 2025-02-27 в 01 38 00" src="https://github.com/user-attachments/assets/49443e66-282e-4f9b-9bd9-1d75b9cd6400" />

2. Получить ответ вашего nginx из контейнера по адресу http://localhost:8080

<img width="653" alt="Снимок экрана 2025-02-27 в 01 38 44" src="https://github.com/user-attachments/assets/157463ce-b8c9-4fde-978b-7411c4b2e295" />

3. Использовать базовые легковесные образы – alpine

<img width="160" alt="Снимок экрана 2025-02-27 в 01 39 05" src="https://github.com/user-attachments/assets/d904fb42-6bd4-4ea4-ba51-946ad972ed3e" />

4. Добавить возможность конфигурирования nginx через внешний файл

<img width="315" alt="Снимок экрана 2025-02-27 в 01 39 32" src="https://github.com/user-attachments/assets/54797784-6720-4592-b74e-c46098587bdc" />

5. Статические страницы (сайты) должны быть внешним томом volume

<img width="315" alt="Снимок экрана 2025-02-27 в 01 39 32" src="https://github.com/user-attachments/assets/54797784-6720-4592-b74e-c46098587bdc" />

6. Контейнер должен запускаться от непривилегированного пользователя

<img width="99" alt="Снимок экрана 2025-02-27 в 01 40 09" src="https://github.com/user-attachments/assets/595d3ac7-ee86-4466-a2e2-ce37b1237aab" />

7. Создать файл docker-compose для старта и сборки
В корне проекта есть файл `docker-compose.yml`:

<img width="612" alt="Снимок экрана 2025-02-27 в 01 40 41" src="https://github.com/user-attachments/assets/9e6fe751-75c4-465a-885f-ed39e70860c5" />

Запуск `docker-compose build`:

<img width="1136" alt="Снимок экрана 2025-02-27 в 01 31 26" src="https://github.com/user-attachments/assets/d0f3784f-c897-492b-a746-dcb400f966d6" />

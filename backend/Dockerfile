FROM bellsoft/liberica-openjdk-alpine:17 AS build

# Устанавливаем Maven
RUN apk add --no-cache maven

# Указываем рабочую директорию
WORKDIR /app

# Копируем pom.xml отдельно для кэширования зависимостей
COPY pom.xml ./
RUN mvn dependency:go-offline

# Копируем остальные исходники
COPY src ./src
RUN mvn clean package -DskipTests

# Финальный образ
FROM bellsoft/liberica-openjdk-alpine:17

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app
COPY --from=build /app/target/*.jar app.jar

USER appuser

ENTRYPOINT ["java", "-jar", "app.jar"]


# MediaTrack

MediaTrack - REST API сервис для управления базой данных видео. Сервис предоставляет полный CRUD-функционал для работы с метаданными видео с поддержкой фильтрации, валидации и Docker-развертывания.

# 🚀 Запуск проекта
+ Клонируйте репозиторий и перейдите в папку проекта
```
git clone https://github.com/GGGamzat/MediaTrack.git
cd MediaTrack
```

+ Соберите и запустите с помощью Docker
```
docker-compose up --build
```

+ Api будет доступно по адресу http://localhost:8000/docs

# 📡 API Эндпоинты

1. Создание видео
```
curl -X POST "http://localhost:8000/videos" \
  -H "Content-Type: application/json" \
  -d '{
    "video_path": "/storage/camera1/video.mp4",
    "start_time": "2024-01-15T10:30:00",
    "duration": "PT1H30M",
    "camera_number": 1,
    "location": "Entrance"
  }'
```

2. Получение списка видео
```
curl "http://localhost:8000/videos"
```

3. Получение списка видео (с фильтрацией)
```
curl "http://localhost:8000/videos?camera_number=1&camera_number=2&status=new&status=transcoded&location=Entrance&location=Exit"
```

4. Получение конкретного видео
```
curl "http://localhost:8000/videos/1"
```

5. Обновление статуса видео
```
curl -X PATCH "http://localhost:8000/videos/1/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "transcoded"}'
```
# Книжный клуб

## Запуск 

1. docker compose -f docker-compose.yml -f docker-compose.local.yml up -d --build
2. docker compose exec backend python manage.py loaddata users.json clubs.json

## Скриншоты

![Авторизация](assets/auth.png)
![Список клубов](assets/clubs.png)
![Карточка клуба](assets/club.png)
![Рецензии](assets/review.png)
![404](assets/404.png)

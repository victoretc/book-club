# Книжный клуб

## Запуск 

1. docker compose -f docker-compose.yml -f docker-compose.local.yml up -d backend
2. Открыть http://localhost:8100
3. docker compose exec backend python manage.py loaddata users.json clubs.json

Для страницы карточек сделай loader и спрячь пагинацию до момента пока не загрузились карточки 


Текущие проблемы дизайна:


9. Отзывы прям сильно перелапатить нужно. 
12. Ебучий адаптив


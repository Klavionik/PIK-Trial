# "Прораб v0.1"

### Описание

Сервис для ведения учета положенных в доме кирпичей. Тестовое задание.

### Запуск

`$ git clone https://github.com/Klavionik/construction-trial-case.git`  
`$ cd construction_trial_case`  
`$ ./manage.py migrate`  
`$ ./manage.py loaddata construction.json`  
`$ ./manage.py runserver`

### Использование

* Тесты  
`$ ./manage.py test`

* Добавление нового дома  
`/api/construction/building`

* Добавление кирпичей в дом  
`/api/construction/building/{building_id}/add_bricks`

* Статистика по всем домам (`/` редиректит сюда же)  
`/api/construction/stats`

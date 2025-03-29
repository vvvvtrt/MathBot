# MathBot

## Fo start working with DB:

1. Push vars to `.env` (example in `.env.example`)

2. Up PosgreSQL with Docker

```bash
make docker-db-up
```

3. Create all tables

```py
python -m database.create_all
```

4. Use services in directory `services`

    For test, you can run code to add new teacher and work with him:

```py
python -m services.tests
```

### Отправка задания студенту
- Студент может узнать свой Telegram ID из бота (@getmyid_bot) и сказать его учителю. Учитель же зная этот ID сможет отправить ему задание. Для реализации этого нужно вызвать метод assign_pattern_to_student() сервиса StudentService.



### Docker commands
In Makefile (for Linux)

```bash
make <command>
```

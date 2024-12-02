# database migrations

[migration tools](https://github.com/golang-migrate/migrate/tree/master/cmd/migrate)
Для создания миграции с помощью migrate CLI, вы можете выполнить следующие шаги, учитывая ваш текущий проект и структуру миграций.

1. Установите migrate CLI
   Если вы еще не установили migrate, сделайте это в соответствии с документацией, например:

bash
Копировать код

# Для MacOS через Homebrew

brew install golang-migrate
Или для других операционных систем следуйте инструкциям из документации.

2. Создание миграции для таблицы users
   Для создания миграции с помощью migrate CLI выполните команду:

bash
Копировать код
migrate create -ext sql -dir migrations create_users_table
Это создаст два файла миграции в папке migrations:

000003_create_users_table.up.sql
000003_create_users_table.down.sql 3. Редактирование миграционных файлов
Файл 000003_create_users_table.up.sql
В этом файле пропишите SQL-запрос для создания таблицы users:

sql
Копировать код
-- 000003_create_users_table.up.sql

CREATE TABLE users (
id SERIAL PRIMARY KEY,
username VARCHAR(255) UNIQUE NOT NULL,
email VARCHAR(255) UNIQUE NOT NULL,
password VARCHAR(255) NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Добавление триггера для автоматического обновления поля updated_at
CREATE OR REPLACE FUNCTION update_user_timestamp()
RETURNS TRIGGER AS $$
BEGIN
NEW.updated_at = CURRENT_TIMESTAMP;
RETURN NEW;
END;

$$
LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_user_timestamp
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_user_timestamp();
Файл 000003_create_users_table.down.sql
В этом файле пропишите SQL-запрос для отката миграции (удаление таблицы):

sql
Копировать код
-- 000003_create_users_table.down.sql

DROP TABLE IF EXISTS users;
4. Применение миграции
Чтобы применить миграцию, выполните команду:

bash
Копировать код
migrate -source file://migrations -database "postgres://username:password@localhost:5432/your_database_name" up
Для применения конкретной миграции (например, 2), используйте:

bash
Копировать код
migrate -source file://migrations -database "postgres://username:password@localhost:5432/your_database_name" up 2
5. Откат миграции
Если нужно откатить миграцию, выполните команду:

bash
Копировать код
migrate -source file://migrations -database "postgres://username:password@localhost:5432/your_database_name" down 1
Заключение
С помощью migrate CLI вы можете легко создавать и применять миграции. В вашем случае, чтобы добавить таблицу users, вы создаете миграцию через migrate create, редактируете сгенерированные файлы с SQL-кодом и применяете их к базе данных.
$$
'''
migrate -path migrations -database "postgres://ivan:8798@localhost:9876/users?sslmode=disable" down
'''

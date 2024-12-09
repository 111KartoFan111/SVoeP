# ИСпользуется PosgreSQL
При переноси  базы данных изменить пути пользователя хост и пароль

Таблицы
CREATE TABLE applications (
    id SERIAL PRIMARY KEY, -- уникальный идентификатор новости
    name VARCHAR(255) NOT NULL, --Имя клиента
    phone VARCHAR(20) NOT NULL, -- номер телефона
    comment TEXT, -- комментарий клиента
    processed BOOLEAN DEFAULT FALSE, -- 
    admin_comment TEXT -- комментарий администратора
);

CREATE TABLE news (
    id SERIAL PRIMARY KEY,  -- уникальный идентификатор новости
    title TEXT NOT NULL,     -- заголовок новости
    content TEXT NOT NULL,   -- содержание новости
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- дата и время создания новости (по умолчанию текущее время)
);


-- парольь администратора 2222 при желании можно изменить
 @svoeadmin_bot -- телеграмм бот

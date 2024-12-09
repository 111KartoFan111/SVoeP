from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import psycopg2

# Установите подключение к базе данных
def get_db_connection():
    conn = psycopg2.connect(dbname="svoe_db", user="postgres", password="0000", host="127.0.0.1", port=5433)
    return conn

# Пароль для администратора
ADMIN_PASSWORD = "2222"  # Замените на реальный пароль администратора

# Глобальная переменная для отслеживания статуса авторизации пользователя
authorized_users = {}

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Здравствуйте! Пожалуйста, введите пароль для авторизации.")

# Обработчик пароля
async def password_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    password = update.message.text.strip()

    # Проверка пароля
    if password == ADMIN_PASSWORD:
        authorized_users[user_id] = True
        await update.message.reply_text("Вы авторизованы как администратор. Теперь используйте команды /applications или /news.")
    else:
        await update.message.reply_text("Неверный пароль. Попробуйте снова.")

# Обработчик команды /applications — показывает все заявки
async def applications(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Проверка, авторизован ли пользователь
    if user_id not in authorized_users or not authorized_users[user_id]:
        await update.message.reply_text("Для доступа к этой команде вам нужно ввести пароль администратора.")
        return

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, phone, comment, processed FROM applications")
    applications = cur.fetchall()
    conn.close()

    # Формирование списка заявок
    message = "Заявки:\n\n"
    for app in applications:
        message += f"ID: {app[0]}, Имя: {app[1]}, Телефон: {app[2]}, Комментарий: {app[3]}, Обработано: {app[4]}\n"

    await update.message.reply_text(message)

# Обработчик команды /news — показывает все новости
async def news(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Проверка, авторизован ли пользователь
    if user_id not in authorized_users or not authorized_users[user_id]:
        await update.message.reply_text("Для доступа к этой команде вам нужно ввести пароль администратора.")
        return

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, content, date FROM news ORDER BY date DESC")
    news_items = cur.fetchall()
    conn.close()

    # Формирование списка новостей
    message = "Новости:\n\n"
    for news_item in news_items:
        message += f"ID: {news_item[0]}, Заголовок: {news_item[1]}, Дата: {news_item[3]}\n{news_item[2]}\n\n"

    await update.message.reply_text(message)

# Обработчик команды /add_news — добавление новости с автоматической датой
async def add_news(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Проверка, авторизован ли пользователь
    if user_id not in authorized_users or not authorized_users[user_id]:
        await update.message.reply_text("Для доступа к этой команде вам нужно ввести пароль администратора.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Использование: /add_news <Заголовок> <Контент>")
        return

    title = context.args[0]
    content = ' '.join(context.args[1:])

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO news (title, content, date)
        VALUES (%s, %s, NOW())
        """,
        (title, content)
    )
    conn.commit()
    conn.close()

    await update.message.reply_text(f"Новость '{title}' добавлена с текущей датой!")


# Обработчик команды /update_news — обновление новости
async def update_news(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Проверка, авторизован ли пользователь
    if user_id not in authorized_users or not authorized_users[user_id]:
        await update.message.reply_text("Для доступа к этой команде вам нужно ввести пароль администратора.")
        return

    if len(context.args) < 3:
        await update.message.reply_text("Использование: /update_news <ID новости> <Заголовок> <Контент>")
        return

    news_id = int(context.args[0])
    title = context.args[1]
    content = ' '.join(context.args[2:])

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE news
        SET title = %s, content = %s
        WHERE id = %s
    """, (title, content, news_id))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"Новость ID {news_id} обновлена!")

# Обработчик команды /delete_news — удаление новости
async def delete_news(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # Проверка, авторизован ли пользователь
    if user_id not in authorized_users or not authorized_users[user_id]:
        await update.message.reply_text("Для доступа к этой команде вам нужно ввести пароль администратора.")
        return

    if len(context.args) < 1:
        await update.message.reply_text("Использование: /delete_news <ID новости>")
        return

    news_id = int(context.args[0])

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM news WHERE id = %s", (news_id,))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"Новость ID {news_id} удалена!")

# Главная функция
def main():
    application = Application.builder().token("7705461504:AAHNbj_cY44V10LQS9LXWdNgw3wLBQ1qr2U").build()
    sss = application
    sss.add_handler(CommandHandler("start", start))
    sss.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, password_handler))


    sss.add_handler(CommandHandler("applications", applications))
    sss.add_handler(CommandHandler("news", news))
    sss.add_handler(CommandHandler("add_news", add_news))
    sss.add_handler(CommandHandler("update_news", update_news))
    sss.add_handler(CommandHandler("delete_news", delete_news))

    application.run_polling()

if __name__ == '__main__':
    main()

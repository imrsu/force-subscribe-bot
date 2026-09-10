import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
CHANNEL = "@Kick_Feed"

def subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        print(f"User {user_id} status: {member.status}")
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Error checking status for {user_id}: {e}")
        return False

@bot.message_handler(func=lambda m: True)
def check_user(message):
    if not subscribed(message.from_user.id):
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception as e:
            print(f"Error deleting message: {e}")

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                "🚀 Join KickFeed",
                url="https://t.me/Kick_Feed"
            )
        )

        bot.send_message(
            message.chat.id,
            "⚠️ You must join @Kick_Feed before chatting.",
            reply_markup=markup
        )

bot.infinity_polling()

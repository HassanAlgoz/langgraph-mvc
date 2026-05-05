from telegram.ext import Application, MessageHandler, filters

from mvc.frontends.telegram.bot import Bot
from mvc.config import MODEL_NAME, OPENROUTER_API_KEY
from mvc.services.llm import new_llm

def main():
    llm = new_llm(
        model=MODEL_NAME,
        openrouter_api_key=OPENROUTER_API_KEY,
        streaming=True,
    )
    bot = Bot(llm=llm)

    application = Application.builder().token(bot.get_bot_token()).build()

    application.add_handler(MessageHandler(filters.ALL, bot.on_update_received))

    application.run_polling()


if __name__ == "__main__":
    main()

import asyncio
import logging
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from .models import Contact

logger = logging.getLogger(__name__)

token = os.getenv("BOT_TOKEN")

app = ApplicationBuilder().token(token).build()


async def start(update: Update, context) -> None:
    if not await Contact.objects.filter(chat_id=update.message.chat_id, user_id=update.message.from_user.id).aexists():
        await Contact.objects.acreate(
            user_id=update.message.from_user.id,
            chat_id=update.message.chat_id,
        )

    await update.message.reply_text(f'سلام ☺️. لطفا لینک آهنگ مورد نظرتو بفرست تا دانلودش کنم.')


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("خب حالا صبر کن تا ببینم چی فرستادی.")
    if not update.message.text.startswith("https://open.spotify"):
        await update.message.reply_text(
            "❌ لینکت ایراد داره. دانلود نمیشه."
            "\nنمونه لینک صحیح: \n\n https://open.spotify.com/track/6sPpUfwcYBgW3kTXStNsVM?si=COAFhsEpRgWYvUlCRBQ4Jg"
        )
        return

    loop = asyncio.get_event_loop()
    await update.message.reply_text("🔁 در حال دانلود ....")
    exit_code = await loop.run_in_executor(
        None,
        os.system,
        f"./spotdl-4.2.8-linux download {update.message.text}"
    )
    logger.debug(f'\n\nexit_code of download ==> {exit_code}\n\n')
    if exit_code != 0:
        await update.message.reply_text(
            "❌ لینکت ایراد داره. دانلود نمیشه."
            "\nنمونه لینک صحیح: \n\n https://open.spotify.com/track/6sPpUfwcYBgW3kTXStNsVM?si=COAFhsEpRgWYvUlCRBQ4Jg"
        )
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            os.system,
            f"rm /code/musics/*"
        )
        return

    file_name = os.listdir("/code/musics/")[0]

    with open(f"/code/musics/{file_name}", "rb") as file:
        await update.message.reply_audio(audio=file.read(), connect_timeout=30, pool_timeout=30)
        await update.message.reply_text("✅ دانلود موفق")
        await update.message.reply_text("باز هم میتونی لینک جدید بفرستی.🙂")

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        os.system,
        f"rm /code/musics/*"
    )


app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, download))

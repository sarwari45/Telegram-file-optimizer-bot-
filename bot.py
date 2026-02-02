import os
import ffmpeg
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv"8185938078:AAFLkF103Xh_Vj5jS5VLN3fc3WdlX6yxyzY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "📸 Send an image or 🎥 a video\n"
        "🔧 I will reduce the file size\n"
        "✅ No visible quality loss\n\n"
        "🚀 Powered by shakib Sarwari"
    )

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if msg.photo:
        photo = msg.photo[-1]
        file = await photo.get_file()
        input_path = "input.jpg"
        output_path = "output.jpg"

        await file.download_to_drive(input_path)

        img = Image.open(input_path)
        img.save(output_path, optimize=True, quality=85)

        await msg.reply_photo(
            photo=open(output_path, "rb"),
            caption="✅ Image optimized successfully"
        )

    elif msg.video:
        video = msg.video
        file = await video.get_file()
        input_path = "input.mp4"
        output_path = "output.mp4"

        await file.download_to_drive(input_path)

        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                vcodec="libx264",
                crf=23,
                preset="slow",
                movflags="faststart"
            )
            .run(overwrite_output=True)
        )

        await msg.reply_video(
            video=open(output_path, "rb"),
            caption="✅ Video optimized with smart compression"
        )

    for f in ["input.jpg", "output.jpg", "input.mp4", "output.mp4"]:
        if os.path.exists(f):
            os.remove(f)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, handle_media))
app.run_polling()

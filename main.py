import os
import subprocess
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("8185938078:AAFLkF103Xh_Vj5jS5VLN3fc3WdlX6yxyzY")

# -------- Commands --------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "📷 Send a photo to compress\n"
        "🎥 Send a video to compress"
    )

# -------- PHOTO HANDLER --------

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()

    input_path = "input.jpg"
    output_path = "output.jpg"

    await file.download_to_drive(input_path)

    # Compress photo using PIL
    from PIL import Image
    image = Image.open(input_path)
    image.save(output_path, optimize=True, quality=60)

    await update.message.reply_photo(photo=open(output_path, "rb"))

# -------- VIDEO HANDLER --------

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video
    file = await video.get_file()

    input_path = "input.mp4"
    output_path = "output.mp4"

    await file.download_to_drive(input_path)

    # Compress video using FFmpeg
    subprocess.run([
        "ffmpeg",
        "-i", input_path,
        "-vcodec", "libx264",
        "-crf", "28",
        output_path
    ])

    await update.message.reply_video(video=open(output_path, "rb"))

# -------- BOT START --------

app = ApplicationBuilder().token(8185938078:"AAFLkF103Xh_Vj5jS5VLN3fc3WdlX6yxyzY").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.VIDEO, handle_video))

app.run_polling()

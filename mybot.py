import io
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- SETTINGS ---
TELEGRAM_TOKEN = '9002713207:AAErUNY68DCJ-BiCftxnYUHojVOcxosx8ow'

async def handle_audio_cleaning(update: Update, context: ContextTypes.T):
    # Ye bot audio ya document dono ko accept karega
    file = update.message.audio or update.message.document
    
    if file:
        # User ko feel dilao ki processing ho rahi hai
        await update.message.reply_text("Cleaning audio and removing tags... 🧹")
        
        try:
            # Step 1: File ko memory (RAM) mein download karo
            # Isse hard drive ki permission error nahi aayegi
            audio_file = await file.get_file()
            audio_bytes = await audio_file.download_as_bytearray()
            
            # Step 2: Bytearray ko voice buffer mein badlo
            voice_buffer = io.BytesIO(audio_bytes)
            
            # IMPORTANT: Telegram ko batana ki ye .ogg (voice note) hai
            # Taki metadata aur 'Unknown Artist' gayab ho jaye
            voice_buffer.name = "clean_voice.ogg" 
            
            # Step 3: Voice Note ke roop mein bhejo
            await update.message.reply_voice(voice=voice_buffer)
            
            # Optional: Cleanup message (aap ise hata bhi sakte hain)
            # await update.message.reply_text("Done! ✅")
            
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    else:
        await update.message.reply_text("Bhai, pehle Reel wala MP3 file bhejo!")

async def start(update: Update, context: ContextTypes.T):
    await update.message.reply_text(
        "Welcome! 🎙️\n\nMujhe koi bhi MP3 file bhejo, "
        "main use clean Voice Note (Bubble) mein convert kar dunga "
        "taaki koi 'Unknown Artist' ya file name na dikhe."
    )

if __name__ == '__main__':
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    # filters.AUDIO aur filters.Document dono ko handle karega
    app.add_handler(MessageHandler(filters.AUDIO | filters.Document.ALL, handle_audio_cleaning))
    
    print("Bot is running... Ready to clean audio! 🚀")
    app.run_polling()
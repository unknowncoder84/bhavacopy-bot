import requests
import zipfile
import io
import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8137518523:AAFmeYkuQO7EBZlySh7MCVAD5YySkdjz_6A"

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    parts = text.split()

    if len(parts) != 2:
        await update.message.reply_text("Send like: TCS 16-01-2026")
        return

    symbol = parts[0].upper()
    date = parts[1]

    d, m, y = date.split("-")

    url = f"https://www.nseindia.com/content/historical/DERIVATIVES/{y}/{m}/fo{d}{m}{y}.zip"

    session = requests.Session()
    session.get("https://www.nseindia.com")

    response = session.get(url)

    if response.status_code != 200:
        await update.message.reply_text("Bhavcopy not found for this date")
        return

    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    csv_name = zip_file.namelist()[0]

    df = pd.read_csv(zip_file.open(csv_name))
    df = df[df["SYMBOL"] == symbol]

    file_name = f"{symbol}.xlsx"
    df.to_excel(file_name, index=False)

    await update.message.reply_document(open(file_name, "rb"))

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))
app.run_polling()
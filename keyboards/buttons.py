from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
main_menu = ReplyKeyboardMarkup(
keyboard=[
    [
           KeyboardButton(text="🎬 فیلم"),
            KeyboardButton(text="📺 سریال")
    ],
    [
           KeyboardButton(text="⭐ علاقه مندی های من")
    ],
    [
            KeyboardButton(text="ℹ️ درباره ما"),
            KeyboardButton(text="❓ راهنما")
            
    ]
],
resize_keyboard=True
)
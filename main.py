import asyncio
import os
import aiohttp

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards.buttons import main_menu
from database import create_db, add_favorite, get_favorites


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")


# ---------------- STATES ----------------

class MovieState(StatesGroup):
    waiting_for_movie = State()


class SeriesState(StatesGroup):
    waiting_for_series = State()



# ---------------- API ----------------

async def search_movie(movie_name):

    url = "https://www.omdbapi.com/"

    params = {
        "apikey": os.getenv("OMDB_API_KEY"),
        "t": movie_name,
        "type": "movie"
    }


    async with aiohttp.ClientSession() as session:

        async with session.get(url, params=params) as response:

            return await response.json()



async def search_series(series_name):

    url = "https://www.omdbapi.com/"

    params = {
        "apikey": os.getenv("OMDB_API_KEY"),
        "t": series_name,
        "type": "series"
    }


    async with aiohttp.ClientSession() as session:

        async with session.get(url, params=params) as response:

            return await response.json()



# ---------------- MAIN ----------------

async def main():

    bot = Bot(token=TOKEN)

    dp = Dispatcher()

    create_db()



    # START

    @dp.message(Command("start"))
    async def start_handler(message: Message):

        await message.answer(
            "🎬 خوش آمدید\n\nیک گزینه را انتخاب کنید:",
            reply_markup=main_menu
        )



    # ---------------- MOVIE ----------------


    @dp.message(F.text.contains("فیلم"))
    async def movie_handler(message: Message, state: FSMContext):

        await message.answer(
            "🎬 نام فیلم را وارد کنید:"
        )

        await state.set_state(
            MovieState.waiting_for_movie
        )



    @dp.message(MovieState.waiting_for_movie)
    async def get_movie_name(message: Message, state: FSMContext):

        movie_name = message.text


        await message.answer(
            f"🔍 در حال جستجوی فیلم: {movie_name}"
        )


        data = await search_movie(movie_name)



        if data.get("Response") == "True":


            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="❤️ ذخیره فیلم",
                            callback_data=f"save_{data['Title']}"
                        )
                    ]
                ]
            )



            await message.answer_photo(

                photo=data.get("Poster"),

                caption=f"""
🎬 {data.get('Title')}

📅 سال انتشار:
{data.get('Year')}

🎭 ژانر:
{data.get('Genre')}

⭐ امتیاز IMDb:
{data.get('imdbRating')}

🎬 کارگردان:
{data.get('Director')}

👥 بازیگران:
{data.get('Actors')}

📝 خلاصه:
{data.get('Plot')}
🌍 کشور:
{data.get('Country')}

🗣 زبان:
{data.get('Language')}

⏱ مدت زمان:
{data.get('Runtime')}

🏆 جوایز:
{data.get('Awards')}
""",

                reply_markup=keyboard
            )


        else:

            await message.answer(
                "❌ فیلم پیدا نشد"
            )


        await state.clear()



    # ذخیره فیلم

    # @dp.callback_query(F.data.startswith("save_"))
    # async def save_movie(callback: CallbackQuery):

    #     movie_name = callback.data.replace(
    #         "save_",
    #         ""
    #     )


    #     add_favorite(
    #         callback.from_user.id,
    #         movie_name
    #     )


    #     await callback.answer(
    #         "❤️ فیلم ذخیره شد"
    #     ) 
    @dp.callback_query(F.data.startswith("save_") & ~F.data.startswith("save_series_"))
    async def save_movie(callback: CallbackQuery):

     print("MOVIE CALLBACK:", callback.data)

     movie_name = callback.data.replace(
        "save_",
        ""
    )

     add_favorite(
        callback.from_user.id,
        movie_name
    )

     await callback.answer("❤️ فیلم ذخیره شد")


    #SERIES


    @dp.message(F.text.contains("سریال"))
    async def series_handler(message: Message, state: FSMContext):

        await message.answer(
            "📺 نام سریال را وارد کنید:"
        )


        await state.set_state(
            SeriesState.waiting_for_series
        )



    @dp.message(SeriesState.waiting_for_series)
    async def get_series_name(message: Message, state: FSMContext):

        series_name = message.text


        await message.answer(
            f"🔍 در حال جستجوی سریال: {series_name}"
        )


        data = await search_series(series_name)



        if data.get("Response") == "True":
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="❤️ ذخیره سریال",
                            callback_data=f"save_series_{data['Title']}"
                        )
                    ]
                ]
            )
            extera=""
            try:
                if float(data.get("imdbRating,0")) >= 8.5:
                    extra += "\n🔥 این اثر امتیاز بسیار بالایی در IMDb دارد."
            except:
                pass
            if "oscar" in data.get("Awards",""):
                extra += "\n🏆 برنده جایزه اسکار"

            await message.answer_photo(

                photo=data.get("Poster"),

                caption=f"""
📺 {data.get('Title')}

📅 سال انتشار:
{data.get('Year')}

🎭 ژانر:
{data.get('Genre')}

⭐ امتیاز IMDb:
{data.get('imdbRating')}

👥 بازیگران:
{data.get('Actors')}

📝 خلاصه:
{data.get('Plot')}
🌍 کشور:
{data.get('Country')}

🗣 زبان:
{data.get('Language')}

⏱ مدت زمان:
{data.get('Runtime')}

🏆 جوایز:
{data.get('Awards')}
{extera}
""",
    reply_markup=keyboard
            )


        else:

            await message.answer(
                "❌ سریال پیدا نشد"
            )


        await state.clear()

    # @dp.callback_query(F.data.startswith("save_") & ~F.data.startswith("save_series_"))
    # async def save_series(callback: CallbackQuery):
    #     get_series_name = callback.data.replace(
    #         "save_series_",
    #         ""
    #     )
    #     add_favorite(
    #         callback.from_user.id,
    #         get_series_name
    #     )
    #     await callback.answer("❤️ سریال ذخیره شد")
    @dp.callback_query(F.data.startswith("save_series_"))
    async def save_series(callback: CallbackQuery):

     print("SERIES CALLBACK:", callback.data)

     series_name = callback.data.replace(
        "save_series_",
        ""
    )

     add_favorite(
        callback.from_user.id,
        series_name
    )

     await callback.answer("❤️ سریال ذخیره شد")

    #FAVORITES


    @dp.message(F.text.contains("⭐ علاقه مندی های من"))
    async def favorites_handler(message: Message):

        movies = get_favorites(
            message.from_user.id
        )


        if not movies:

            await message.answer(
                "⭐ هنوز فیلمی ذخیره نکردید."
            )

            return



        text = "⭐ فیلم‌های ذخیره شده:\n\n"


        for movie in movies:

            text += f"🎬 {movie[0]}\n"



        await message.answer(text)

    @dp.message(F.text == "❓ راهنما")
    async def help_handler(message: Message):
        await message.answer(
              """
📚 راهنمای استفاده از ربات

🎬 جستجوی فیلم
روی دکمه «فیلم» بزنید و نام فیلم را به انگلیسی وارد کنید.
مثال:
Inception

📺 جستجوی سریال
روی دکمه «سریال» بزنید و نام سریال را به انگلیسی وارد کنید.
مثال:
Breaking Bad

❤️ ذخیره علاقه‌مندی
بعد از نمایش اطلاعات، روی دکمه «ذخیره» بزنید.

⭐ علاقه‌مندی‌های من
تمام فیلم‌ها و سریال‌های ذخیره‌شده را مشاهده کنید.

🤖 اطلاعات این ربات از سایت OMDb دریافت می‌شود.
"""
        )

#ABOUT


    @dp.message(F.text.contains("درباره"))
    async def about_handler(message: Message):

        await message.answer(
            "🤖 این بات برای جستجوی فیلم و سریال ساخته شده."
        )



    print("Bot started!")

    await dp.start_polling(bot)




if __name__ == "__main__":

    asyncio.run(main())
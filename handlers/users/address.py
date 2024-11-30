from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default.user import user_address_keyboard, my_address_keyboards, categories_keyboards
from loader import _
from loader import dp
from logging_settings import logger
from states.user import RegisterState
from utils.db_commands.address import get_user_address, add_address, get_address_by_name
from utils.db_commands.products import get_categories
from utils.get_location import get_full_address
from . import menu



def create_map_link(latitude, longitude):
    return f"https://www.google.com/maps/?q={latitude},{longitude}"


@dp.message_handler(lambda message: message.text in ["🍴 Menu", "🍴 Menyu"])
async def get_address_menu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    await message.answer(text=_("Submit your geolocation 📍 or select a delivery address", locale=language),
                         reply_markup=await user_address_keyboard(language=language))

    map_link = "https://www.google.com/maps"  # Link to Google Maps
    await message.answer(f"You can also choose your location on the map: {map_link}")


@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def get_full_location(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    address = await get_full_address(latitude=latitude, longitude=longitude)

    try:
        if address:
            await message.answer(text=address)  # This should work if 'address' is valid
            map_link = create_map_link(latitude, longitude)
            await add_address(message=message, name=address, latitude=latitude, longitude=longitude)
            await message.answer(f"Your address: {address}\nYou can view your location on the map: {map_link}")
        else:
            await message.answer("Address could not be found. Please try again.")
    except Exception as e:
        logger.error(f"Error sending message: {e}")



@dp.message_handler(lambda message: message.text in ["🗺 My addresses", "🗺 Mening manzillarim"])
async def get_my_address(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    addresses = await get_user_address(message.chat.id)
    if addresses:
        await message.answer(text=_("Your address:", locale=language),
                             reply_markup=await my_address_keyboards(addresses, language=language))

    else:
        await message.answer(text=_("You don't have any addresses yet", locale=language),
                             reply_markup=await user_address_keyboard(language=language))
    await RegisterState.address.set()


@dp.message_handler(state=RegisterState.address)
async def get_address_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get('language')
    address_name = message.text
    address = await get_address_by_name(address_name)
    if address:
        menu.categories = await get_categories()

        await message.answer("Choose a product category:",
                             reply_markup=await categories_keyboards(menu.categories, language=language))
    else:
        await message.answer("You do not have such an address.")
    await state.finish()

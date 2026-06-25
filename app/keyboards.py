from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text="[ 🚀 ] Запуск жалоб", callback_data="startReportStep1")
		],
		[
			InlineKeyboardButton(text="[ ℹ ] Информация", callback_data="startInfo"),
			InlineKeyboardButton(text="[ 🗞 ] Наш канал", url="https://t.me/durov")
		]
	]
)

cancel = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text="[ ✖️ ] Отмена", callback_data="cancelAction")
		]
	]
)

reasons = InlineKeyboardMarkup(
	inline_keyboard=[
		[
			InlineKeyboardButton(text="[ 📇 ] Доксинг", callback_data="reason_doxing"),
			InlineKeyboardButton(text="[ 🔞 ] Порнография", callback_data="reason_porn"),
			InlineKeyboardButton(text="[ 🎣 ] Фишинг", callback_data="reason_phishing")
		],
		[
			InlineKeyboardButton(text="[ 🛑 ] Мошенничество", callback_data="reason_scam"),
			InlineKeyboardButton(text="[ 🔫 ] Терроризм", callback_data="reason_terror")
		],
		[
			InlineKeyboardButton(text="[ ✖️ ] Отмена", callback_data="cancelAction")
		]		
	]
)
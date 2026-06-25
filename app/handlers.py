from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import asyncio

import app.keyboards as kb
from scripts.reporter import report

rt = Router()

class Report(StatesGroup):
	msg_id = State()
	username = State()
	reason = State()

@rt.callback_query(F.data == "cancelAction")
async def actionCancel(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	
	await state.clear()
	
	msg = (
		"[ 👋 ] <b>Добро пожаловать!</b>\n"
		"\n"
		"[ 💻 ] Данный бот отправляет жалобы на ботов, что нарушают <b>Terms of Service</b> платформы <b>Telegram</b>\n"
		"\n"
		"[ 👇 ] Ниже предоставлено меню управления ботом."
	)
	
	await callback.message.edit_text(
		text=msg,
		parse_mode="HTML",
		reply_markup=kb.start
	)

@rt.message(CommandStart())
async def startMessage(message: Message):
	
	msg = (
		"[ 👋 ] <b>Добро пожаловать!</b>\n"
		"\n"
		"[ 💻 ] Данный бот отправляет жалобы на ботов, что нарушают <b>Terms of Service</b> платформы <b>Telegram</b>\n"
		"\n"
		"[ 👇 ] Ниже предоставлено меню управления ботом."
	)
	
	await message.answer(
		msg,
		parse_mode="HTML",
		reply_markup=kb.start
	)
	
@rt.callback_query(F.data == "startReportStep1")
async def reportingStep1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    
    msg = "<pre>[ 🔗 ] Введите @username бота, что нарушает <b>Terms of Service Telegram</b></pre>"
    
    await state.set_state(Report.username)
    
    edited_msg = await callback.message.edit_text(
        text=msg, 
        parse_mode="HTML",
        reply_markup=kb.cancel
    )
    
    await state.update_data(msg_id=edited_msg)

@rt.message(Report.username)
async def reportingStep2(message: Message, state: FSMContext):
    username = message.text
    data = await state.get_data()
    bot_message = data.get("msg_id")
    
    if username.startswith('@') and username.lower().endswith('bot'):
        await state.update_data(username=username)
        await state.set_state(Report.reason)
        
        msg = f"<pre>[ 🎈 ] Выбери причину для отправки жалоб на бота <i>{username}</i></pre>"
        
        await message.delete()
        
        await bot_message.edit_text(
            text=msg,
            parse_mode="HTML",
            reply_markup=kb.reasons
        )
        
    else:
        msg = (
            "<pre>[ 🔗 ] Введите корректный @username бота, что нарушает <b>Terms of Service Telegram</b>\n"
            "<i>💡 Например: @TestingBot</i></pre>"
        )
                
        await message.delete()
        
        await bot_message.edit_text(
            text=msg,
            parse_mode="HTML",
            reply_markup=kb.cancel
        )
        
@rt.callback_query(F.data.startswith("reason_"))
async def reportingStepStart(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	
	reason = callback.data.split("_")[1]
	
	data = await state.get_data()
	
	if reason == "doxing":
		
		good, fail = await report(
			target_username=data.get("username"),
			comment="Здравствуйте уважаемый агент! Данный бот специализируется на распространении персональных данных, что нарушает правила телеграм, а также законодательство Российской Федерации. Прошу удалить данный бот.",
			option=b"63:c"
		)
		
	elif reason == "porn":
		
		good, fail = await report(
			target_username=data.get("username"),
			comment="Здравствуйте уважаемый агент! Данный бот специализируется на распространении порнографического контента грубого характера. Прошу проверить данный бот и удалить, спасибо.",
			option=b"57:c"
		)
		
	elif reason == "phishing":
		
		good, fail = await report(
			target_username=data.get("username"),
			comment="Здравствуйте уважаемый агент! Данный бот требует номер телефона для дальнейшего создания попытки входа в аккаунт, что является грубым нарушением Terms of Service, прошу удалить бота.",
			option=b"73:c"
		)
		
	elif reason == "scam":
		
		good, fail = await report(
			target_username=data.get("username"),
			comment="Здравствуйте уважаемый агент! Данный бот является мошенническим, примите меры.",
			option=b"71:c"
		)
		
	elif reason == "terror":
		
		good, fail = await report(
			target_username=data.get("username"),
			comment="Здравствуйте уважаемый агент! Данный бот специализируется на распространении контента для привлечения к терроризму. Это нарушает Terms of Service Telegram а также множественные статьи из законодательства Российской  Федерации, удалите бота.",
			option=b"92:c"
		)
		
	else:
		pass
		
	msg = (
   	 f"<blockquote>🎉 Отправка завершена</blockquote>\n"
   	 f"\n"
   	 f"[ ✅ ] <i>Успешные</i> » <i>{good}</i>\n"
  	  f"[ ❎ ] <i>Неуспешные</i> » <i>{fail}</i>\n"
  	  f"\n"
  	  f"[ ⚡️ ] <i>Цель</i>: <code>{data.get('username')}</code>"
	)

	await callback.message.edit_text(
  	  text=msg,
   	 parse_mode="HTML"
	)

	await state.clear()
	
@rt.callback_query(F.data == "startInfo")
async def startInfo(callback: CallbackQuery):
	await callback.answer()
	
	msg = (
		"[ ℹ️ ] Информационный блок\n"
		"\n"
		" ┌ Бот работает на основе внутренних жалоб\n"
		" ├ Скорость удаления нарушителя не зависит от\n"
		" ├ количества сессий, все зависит от ИИ-модерации\n"
		" ├ а также фильтров (триггеров) Telegram\n"
		" └ Если не снесло 1 раз, второй раз тоже не снесет.\n"
		"\n"
		" ┌ Разработчик бота: <a href='https://github.com/userHideCode'>Hide (ссылка на Git)</a>\n"
		" └ Канал разработчика: <a href='https://t.me/hiderepos'>кликабельная ссылка</a>"		
	)
	
	await callback.message.edit_text(
		text=msg,
		parse_mode="HTML",
		reply_markup=kb.cancel
	)
import asyncio
import os
import random
from telethon import TelegramClient, functions, errors
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")

async def check_session_valid(client):
    try:
        if not await client.is_user_authorized():
            return False, "Не авторизован"
        
        me = await client.get_me()
        if not me:
            return False, "Не удалось получить информацию"
        
        if me.restricted:
            return False, "Аккаунт ограничен"
        
        return True, "OK"
    except errors.rpcerrorlist.AuthKeyUnregisteredError:
        return False, "Ключ не зарегистрирован"
    except errors.rpcerrorlist.SessionPasswordNeededError:
        return False, "Требуется пароль"
    except errors.rpcerrorlist.UserDeactivatedError:
        return False, "Пользователь деактивирован"
    except errors.rpcerrorlist.FloodWaitError as e:
        return False, f"Ожидание {e.seconds}с"
    except Exception as e:
        return False, f"Ошибка: {str(e)}"

async def report(target_username, comment, option=None, sessions_dir="sessions"):
    if not API_ID or not API_HASH:
        return {"error": "API_ID и API_HASH не установлены в файле .env", "success": 0, "total": 0}
    
    if not os.path.exists(sessions_dir):
        os.makedirs(sessions_dir)
        return {"error": "Отсутсвует папка с сессиями", "success": 0, "total": 0}
    
    sessions = [f for f in os.listdir(sessions_dir) if f.endswith('.session')]
    if not sessions:
        return {"error": "Нету сессий.", "success": 0, "total": 0}
    
    options = [option] if option else [b"100:c"]
    semaphore = asyncio.Semaphore(len(sessions))
    
    async def _report(session_file):
        async with semaphore:
            session_path = os.path.join(sessions_dir, os.path.splitext(session_file)[0])
            client = TelegramClient(session_path, API_ID, API_HASH)
            try:
                await client.start()
                
                is_valid, msg = await check_session_valid(client)
                if not is_valid:
                    print(f"❌ {session_file}: {msg}")
                    return False
                
                entity = await client.get_entity(target_username)
                success = 0
                for opt in options:
                    try:
                        result = await client(functions.messages.ReportRequest(
                            peer=entity, id=[], option=opt,
                            message=comment.format(target=target_username)
                        ))
                        if "Reported" in str(result):
                            success += 1
                        await asyncio.sleep(1)
                    except:
                        pass
                return success == len(options)
            except errors.rpcerrorlist.AuthKeyUnregisteredError:
                print(f"❌ {session_file}: Сессия недействительна, удалите файл")
                return False
            except Exception as e:
                print(f"❌ {session_file}: {str(e)[:100]}")
                return False
            finally:
                await client.disconnect()
    
    results = await asyncio.gather(*[_report(s) for s in sessions])
    
    failed = len(sessions) - sum(results)
    success = sum(results)
    
    return success, failed
import re
import logging
import asyncio
import random

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import ButtonDataInvalid, FloodWait

from bot.database import Database # pylint: disable=import-error
from bot.bot import Bot # pylint: disable=import-error

RESULT_IMG = [
"https://telegra.ph/file/9a3985f596048be356c7d.jpg",
"https://telegra.ph/file/f2739aef09df96b6829e7.jpg",
"https://telegra.ph/file/d583d4b9b8c3b7db38a91.jpg",
"https://telegra.ph/file/b74fd995ef41efea3beea.jpg",
"https://telegra.ph/file/20ca0bb17099e867110ca.jpg",
"https://telegra.ph/file/160fed87725326fc56e92.jpg",
"https://telegra.ph/file/0cdcc20578ed81cc1e15e.jpg",
"https://telegra.ph/file/67a23ada76a26a7ca9591.jpg",
"https://telegra.ph/file/e42ed01c03e3a6347c7c2.jpg",
"https://telegra.ph/file/5e1118ab987a1a93b18ca.jpg",
"https://telegra.ph/file/41f4aecff3334530a1fb8.jpg",
"https://telegra.ph/file/3ef3f4b3b9d2d7baf78c5.jpg",
"https://telegra.ph/file/9f0e2bb3c9a1845546171.jpg",
"https://telegra.ph/file/3461dd13f8421d5218768.jpg",
"https://telegra.ph/file/4f6b5ec07aa095131f70b.jpg",
"https://telegra.ph/file/f3cfd6585348dd25e5e11.jpg",
"https://telegra.ph/file/bd0e95fe5e583f91afd8f.jpg",
"https://telegra.ph/file/d6f191da98cd97f560f68.jpg",
"https://telegra.ph/file/f989f751e8cf9fcc09cbf.jpg",
"https://telegra.ph/file/9126c1fb70c77c996d9b1.jpg",
"https://telegra.ph/file/8c0b9e24da2ead70504fb.jpg",
"https://telegra.ph/file/cf8c22f59da051eda3093.jpg",
"https://telegra.ph/file/ac6638789003a25a78492.jpg",
"https://telegra.ph/file/d625294d467b3e9b0dd13.jpg",
"https://telegra.ph/file/1c4035c1abc4847d6c2f4.jpg",
"https://telegra.ph/file/3ebd39b9b6ca30986eb26.jpg",
"https://telegra.ph/file/375c51ea166256927b968.jpg",
"https://telegra.ph/file/5e0d3c0df2c27ca29b700.jpg",
"https://telegra.ph/file/4769799b5eac3a36af05e.jpg",
"https://telegra.ph/file/ecef05bd32c6591578cc1.jpg",
"https://telegra.ph/file/b05096e2fe39ed4881684.jpg",
"https://telegra.ph/file/78e87346630b3b4c38d09.jpg",
"https://telegra.ph/file/40fe04dbd68ab922187b5.jpg",
"https://telegra.ph/file/4e71a817d539a3c9ed9f2.jpg",
"https://telegra.ph/file/40ae8131462f4fe11558b.jpg",
"https://telegra.ph/file/45082e244a74859861940.jpg",
"https://telegra.ph/file/3589c633f2dd80eb84445.jpg",
"https://telegra.ph/file/dacb4b5a755e34dff4870.jpg",
"https://telegra.ph/file/d9ef838995b8b93f3d8e1.jpg",
"https://telegra.ph/file/aa1e94a3ec6897f29fa2e.jpg",
"https://telegra.ph/file/443d6ba72661e30032766.jpg",
"https://telegra.ph/file/dadffd2e4db1f07ebe40c.jpg"
]

FIND = {}
INVITE_LINK = {}
ACTIVE_CHATS = {}
db = Database()

@Bot.on_message(filters.text & filters.group & ~filters.bot, group=0)
async def auto_filter(bot, update):
    """
    A Funtion To Handle Incoming Text And Reply With Appropriate Results
    """
    group_id = update.chat.id

    if re.findall(r"((^\/|^,|^\.|^[\U0001F600-\U000E007F]).*)", update.text):
        return
    
    if ("https://" or "http://") in update.text:
        return
    
    query = re.sub(r"[1-2]\d{3}", "", update.text) # Targetting Only 1000 - 2999 😁
    
    if len(query) < 2:
        return
    
    results = []
    
    global ACTIVE_CHATS
    global FIND
    
    configs = await db.find_chat(group_id)
    achats = ACTIVE_CHATS[str(group_id)] if ACTIVE_CHATS.get(str(group_id)) else await db.find_active(group_id)
    ACTIVE_CHATS[str(group_id)] = achats
    
    if not configs:
        return
    
    allow_video = configs["types"]["video"]
    allow_audio = configs["types"]["audio"] 
    allow_document = configs["types"]["document"]
    
    max_pages = configs["configs"]["max_pages"] # maximum page result of a query
    pm_file_chat = configs["configs"]["pm_fchat"] # should file to be send from bot pm to user
    max_results = configs["configs"]["max_results"] # maximum total result of a query
    max_per_page = configs["configs"]["max_per_page"] # maximum buttom per page 
    show_invite = configs["configs"]["show_invite_link"] # should or not show active chat invite link
    
    show_invite = (False if pm_file_chat == True else show_invite) # turn show_invite to False if pm_file_chat is True
    
    filters = await db.get_filters(group_id, query)
    
    if filters:
        for filter in filters: # iterating through each files
            file_name = filter.get("file_name")
            file_type = filter.get("file_type")
            file_link = filter.get("file_link")
            file_size = int(filter.get("file_size", "0"))
            
            # from B to MiB
            
            if file_size < 1024:
                file_size = f"[{file_size} B]"
            elif file_size < (1024**2):
                file_size = f"[{str(round(file_size/1024, 2))} KB] "
            elif file_size < (1024**3):
                file_size = f"[{str(round(file_size/(1024**2), 2))} MB] "
            elif file_size < (1024**4):
                file_size = f"[{str(round(file_size/(1024**3), 2))} GB] "
            
            
            file_size = "" if file_size == ("[0 B]") else file_size
            
            # add emoji down below inside " " if you want..
            button_text = f"🔖{file_size} ● {file_name}"
            

            if file_type == "video":
                if allow_video: 
                    pass
                else:
                    continue
                
            elif file_type == "audio":
                if allow_audio:
                    pass
                else:
                    continue
                
            elif file_type == "document":
                if allow_document:
                    pass
                else:
                    continue
            
            if len(results) >= max_results:
                break
            
            if pm_file_chat: 
                unique_id = filter.get("unique_id")
                if not FIND.get("bot_details"):
                    try:
                        bot_= await bot.get_me()
                        FIND["bot_details"] = bot_
                    except FloodWait as e:
                        asyncio.sleep(e.x)
                        bot_= await bot.get_me()
                        FIND["bot_details"] = bot_
                
                bot_ = FIND.get("bot_details")
                file_link = f"https://t.me/{bot_.username}?start={unique_id}"
            
            results.append(
                [
                    InlineKeyboardButton(button_text, url=file_link)
                ]
            )
        
    else:
        Send_message = await bot.send_photo( chat_id=update.chat.id,
            photo="https://telegra.ph/file/5a77812dcd24c8cf44572.jpg",
            caption="<b>Couldn't Find This Movie.Try Again..! ഈ സിനിമയുടെ ഒറിജിനൽ പേര് ഗൂഗിളിൽ പോയി കണ്ടെത്തി അതുപോലെ ഇവിടെ കൊടുക്കുക 🥺 \n \n<a href=https://google.com>🔍 SEARCH IN GOOGLE</a> \n \n<a href=https://t.me/joinchat/6WZ0z0AQ0E8yMDdl>ഒന്നും മനസിലായില്ല OGGY SER</a> </b>",
            buttons = [[
        InlineKeyboardButton('💘  𝗪𝗢𝗥𝗞𝗜𝗡𝗚 𝗚𝗥𝗢𝗨𝗣  💘', url='https://t.me/moviehubgroupp'),
    ]]
            reply_to_message_id=update.message_id )
        
        await asyncio.sleep(20)
        await Send_message.delete()
        return # return if no files found for that query
    

    if len(results) == 0: # double check
        return
    
    else:
    
        result = []
        # seperating total files into chunks to make as seperate pages
        result += [results[i * max_per_page :(i + 1) * max_per_page ] for i in range((len(results) + max_per_page - 1) // max_per_page )]
        len_result = len(result)
        len_results = len(results)
        results = None # Free Up Memory
        
        FIND[query] = {"results": result, "total_len": len_results, "max_pages": max_pages} # TrojanzHex's Idea Of Dicts😅

        # Add next buttin if page count is not equal to 1
        if len_result != 1:
            result[0].append(
                [
                    InlineKeyboardButton("🚀 𝗚𝗢 𝗧𝗢 𝗡𝗘𝗫𝗧 𝗣𝗔𝗚𝗘 🚀", callback_data=f"navigate(0|next|{query})")
                ]
            )
        
        # Just A Decaration
        result[0].append([
            InlineKeyboardButton(f"📘 Page 1/{len_result if len_result < max_pages else max_pages} 📘", callback_data="ignore")
        ])
        
        
        # if show_invite is True Append invite link buttons
        if show_invite:
            
            ibuttons = []
            achatId = []
            await gen_invite_links(configs, group_id, bot, update)
            
            for x in achats["chats"] if isinstance(achats, dict) else achats:
                achatId.append(int(x["chat_id"])) if isinstance(x, dict) else achatId.append(x)

            ACTIVE_CHATS[str(group_id)] = achatId
            
            for y in INVITE_LINK.get(str(group_id)):
                
                chat_id = int(y["chat_id"])
                
                if chat_id not in achatId:
                    continue
                
                chat_name = y["chat_name"]
                invite_link = y["invite_link"]
                
                if ((len(ibuttons)%2) == 0):
                    ibuttons.append(
                        [
                            InlineKeyboardButton(f"⚜ {chat_name} ⚜", url=invite_link)
                        ]
                    )

                else:
                    ibuttons[-1].append(
                        InlineKeyboardButton(f"⚜ {chat_name} ⚜", url=invite_link)
                    )
                
            for x in ibuttons:
                result[0].insert(0, x) #Insert invite link buttons at first of page
                
            ibuttons = None # Free Up Memory...
            achatId = None
            
            
        reply_markup = InlineKeyboardMarkup(result[0])

        try:
            await bot.send_photo(
                chat_id = update.chat.id,
                photo=f"{random.choice(RESULT_IMG)}", caption=f"𝗛𝗘𝗬 𝗗𝗨𝗗𝗘 {update.from_user.mention} 🙋‍♂️ \n \n Found Result-: {(len_results)} \n \n 😚 𝗖𝗟𝗜𝗖𝗞 𝗬𝗢𝗨𝗥 𝗙𝗜𝗟𝗘 📂 𝗔𝗡𝗗 𝗦𝗧𝗔𝗥𝗧 𝗧𝗛𝗘 𝗕𝗢𝗧😌 \n \n 🎬𝗠𝗢𝗩𝗜𝗘 𝗡𝗔𝗠𝗘: <code>{query}</code>",
                reply_markup=reply_markup,
                parse_mode="html",
                reply_to_message_id=update.message_id
            )

        except ButtonDataInvalid:
            print(result[0])
        
        except Exception as e:
            print(e)


async def gen_invite_links(db, group_id, bot, update):
    """
    A Funtion To Generate Invite Links For All Active 
    Connected Chats In A Group
    """
    chats = db.get("chat_ids")
    global INVITE_LINK
    
    if INVITE_LINK.get(str(group_id)):
        return
    
    Links = []
    if chats:
        for x in chats:
            Name = x["chat_name"]
            
            if Name == None:
                continue
            
            chatId=int(x["chat_id"])
            
            Link = await bot.export_chat_invite_link(chatId)
            Links.append({"chat_id": chatId, "chat_name": Name, "invite_link": Link})

        INVITE_LINK[str(group_id)] = Links
    return 


async def recacher(group_id, ReCacheInvite=True, ReCacheActive=False, bot=Bot, update=Message):
    """
    A Funtion To rechase invite links and active chats of a specific chat
    """
    global INVITE_LINK, ACTIVE_CHATS

    if ReCacheInvite:
        if INVITE_LINK.get(str(group_id)):
            INVITE_LINK.pop(str(group_id))
        
        Links = []
        chats = await db.find_chat(group_id)
        chats = chats["chat_ids"]
        
        if chats:
            for x in chats:
                Name = x["chat_name"]
                chat_id = x["chat_id"]
                if (Name == None or chat_id == None):
                    continue
                
                chat_id = int(chat_id)
                
                Link = await bot.export_chat_invite_link(chat_id)
                Links.append({"chat_id": chat_id, "chat_name": Name, "invite_link": Link})

            INVITE_LINK[str(group_id)] = Links
    
    if ReCacheActive:
        
        if ACTIVE_CHATS.get(str(group_id)):
            ACTIVE_CHATS.pop(str(group_id))
        
        achats = await db.find_active(group_id)
        achatId = []
        if achats:
            for x in achats["chats"]:
                achatId.append(int(x["chat_id"]))
            
            ACTIVE_CHATS[str(group_id)] = achatId
    return 


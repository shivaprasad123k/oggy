#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG
import random
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from bot import Translation, LOGGER # pylint: disable=import-error
from bot.database import Database # pylint: disable=import-error
PHOTO = [ 
"https://telegra.ph/file/b6987b454ef1d84a5576b.jpg",
 "https://telegra.ph/file/ae46485308f11a3859e00.jpg",
 "https://telegra.ph/file/8996147181e7a921b7093.jpg",
 "https://telegra.ph/file/89fcdb26325e083a3e3a8.jpg",
 "https://telegra.ph/file/801e574e56d7caefd2ec4.jpg",
 "https://telegra.ph/file/5764ff0c275e9ea7d83c9.jpg",
 "https://telegra.ph/file/c096c45d8c24d80d15e7f.jpg",
 "https://telegra.ph/file/12a64264e010822585a62.jpg",
 "https://telegra.ph/file/67ba89184b79372dbe103.jpg",
 "https://telegra.ph/file/9eddbb8d6a2d7282ce908.jpg",
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
db = Database()

@Client.on_message(filters.command(["start"]) & filters.private, group=1)
async def start(bot, update):
    
    try:
        file_uid = update.command[1]
    except IndexError:
        file_uid = False
    
    if file_uid:
        file_id, file_name, file_caption, file_type = await db.get_file(file_uid)
        
        if (file_id or file_type) == None:
            return
        
        caption = file_caption if file_caption != ("" or None) else ("<code>" + file_name + "</code>")
        try:
            await update.reply_cached_media(
                file_id,
                quote=True,
                caption = f"{file_name}",
                parse_mode="html",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton
                                (
                                    '♻️ 𝗝𝗢𝗜𝗡 𝗖𝗛𝗔𝗡𝗘𝗟 ♻️', url="https://t.me/mallumovies30"
                                )
                        ]
                    ]
                )
            )
        except Exception as e:
            await update.reply_text(f"<b>Error:</b>\n<code>{e}</code>", True, parse_mode="html")
            LOGGER(__name__).error(e)
        return

    buttons = [[
        InlineKeyboardButton('💘  𝗪𝗢𝗥𝗞𝗜𝗡𝗚 𝗚𝗥𝗢𝗨𝗣  💘', url='https://t.me/moviehubgroupp'),
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_photo(
        chat_id=update.chat.id,
        photo=f"{random.choice(PHOTO)}",
        caption=Translation.START_TEXT.format(
                update.from_user.first_name),
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["help"]) & filters.private, group=1)
async def help(bot, update):
    buttons = [[
        InlineKeyboardButton('Home ⚡', callback_data='start'),
        InlineKeyboardButton('About 🚩', callback_data='about')
    ],[
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_TEXT,
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )


@Client.on_message(filters.command(["about"]) & filters.private, group=1)
async def about(bot, update):
    
    buttons = [[
        InlineKeyboardButton('Home ⚡', callback_data='start'),
        InlineKeyboardButton('Close 🔐', callback_data='close')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ABOUT_TEXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
        parse_mode="html",
        reply_to_message_id=update.message_id
    )

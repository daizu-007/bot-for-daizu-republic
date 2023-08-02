#このdiscord botは、大豆共和国の管理をするbotです。botの名前は、大豆共和国警察庁長官です。
import discord
import asyncio
import requests
import os
import json
from os import path
from discord.ext import commands

#初期設定
#botの権限 .allで全ての権限を与える。
intents = discord.Intents.all()
#botを定義する
bot = commands.Bot(intents=intents, command_prefix="/")
#jsonファイルから情報を取得する
with open(path.join(path.dirname(__file__), "data.json"), "r") as f:
    data = json.load(f) #dataにjsonファイルの内容を代入
#discordのトークン
dcToken = data["keys"]["dcToken"]
#discordのwebhookのURL
dcURL = data["keys"]["dcURL"]

#実行
bot.run(dcToken) #botを実行

#botが起動したときの処理
@bot.event
async def on_ready():
    print("bot is ready")   #botが起動したことを表示

#新しいユーザーが参加したときの処理
@bot.event
async def on_member_join(member):
    print("new member joined")
    #welcomeメッセージを作成
    message = f"{member.mention}さん、大豆共和国へようこそ！\n<#1124242129783377961>を確認してください。\nその後、<#1124235224641982516>で自己紹介をしてください。"
    #welcomeメッセージを送信
    await bot.get_channel(1124235204375085108).send(message)

#ユーザーがサーバーから退出したときの処理
@bot.event
async def on_member_remove(member):
    print("member left")
    #退出メッセージを作成
    message = f"{member.name}さんが、大豆共和国を去りました。"
    #退出メッセージを送信
    await bot.get_channel(1124235204375085108).send(message)

#メッセージが送信されたときの処理
@bot.event
async def on_message(message):
    #メッセージの送信者がbotなら
    if message.author.bot:
        return #何もしない
    #メッセージが送信されたチャンネルが自己紹介チャンネルなら
    if message.channel.id == 1124235224641982516:
        #メッセージが自己紹介かどうかを判定
        if isSelfIntroduction(message.content,message.author.name):
            #メッセージを送信
            await message.channel.send("自己紹介ありがとうございます。")
        else:
            #メッセージを送信
            await message.channel.send("自己紹介をお願いします。")

#文章が自己紹介かどうかを判定する関数
def isSelfIntroduction(text,user):
    if user in text:
        return True
    else:
        return False




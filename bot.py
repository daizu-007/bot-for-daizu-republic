#このdiscord botは、大豆共和国の管理をするbotです。botの名前は、大豆共和国警察庁長官です。
import discord
import asyncio
import requests
import os

#初期設定
#botの権限 .allで全ての権限を与える。
intents = discord.Intents.default()
#botを定義する
bot = discord.Client(intents=intents)
#discordのトークン
dcToken = os.environ["DP-dcToken"]
#discordのwebhookのURL
dcURL = os.environ["DcURL"]

#新しいユーザーが参加したときの処理
@bot.event
async def on_member_join(member):
    print("new member joined")
    #welcomeメッセージを作成
    message = f"{member.mention}さん、大豆共和国へようこそ！\n<#1124242129783377961>を確認してください。\nその後、<#1124235224641982516>で自己紹介をしてください。"
    #welcomeメッセージを送信
    await bot.get_channel(1124235204375085108).send(message)

#botが起動したときの処理
@bot.event
async def on_ready():
    print("bot is ready")   #botが起動したことを表示

#実行
bot.run(dcToken) #botを実行
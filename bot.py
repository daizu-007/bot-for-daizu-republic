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
    message = f"{member.display_name}さんが、大豆共和国を去りました。"
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
        if isSelfIntroduction(message.content,message.author.display_name):
            #国民ロールを付与
            await message.author.add_roles(message.guild.get_role(1124582468918452225))
            await message.channel.send(f"{message.author.mention}さん、おめでとうございます。あなたは今から大豆共和国民です！")
        else:
            #メッセージを送信
            await message.channel.send(f"<@1034077539938881577>、{message.author.mention}さんが自己紹介をしました。確認してください。")
    #メッセージが送信されたチャンネルが自己紹介チャンネルでないなら
    else:
        await bot.process_commands(message) #コマンドを処理する

#文章が自己紹介かどうかを判定する関数
def isSelfIntroduction(text,user):
    if user in text:
        return True
    else:
        return False

#コマンド
#pingコマンド
@bot.command(name="ping", description="pingを返します。", guild_ids=["1109024847432007771"])
async def ping(ctx): 
    await ctx.send("pong")

#helpコマンド
@bot.command(name="list", description="コマンド一覧を表示します。", guild_ids=["1109024847432007771"])
async def help(ctx):
    #helpメッセージを作成
    message = """

コマンド一覧
    /ping:pingを返します。
    /help:コマンド一覧を表示します。

"""
    #helpメッセージを送信
    await ctx.send(message)

#実行
bot.run(dcToken) #botを実行

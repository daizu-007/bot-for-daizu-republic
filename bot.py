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
dcURLs = data["keys"]["webhookURL"]
#jsonファイルから絵文字の情報を取得する
with open(path.join(path.dirname(__file__), "emojis.json"), "r") as f:
    emojis = json.load(f) #emojisにjsonファイルの内容を代入
#headerの設定
headers = {'Content-Type': 'application/json'}


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
        if message.content.startswith("$"):
            emoji_name = message.content[1:] #メッセージの先頭の"$"を削除
            emoji_URL = emojis.get(emoji_name) #絵文字のURLを取得
            if emoji_URL == None: #絵文字のURLが存在しないなら
                await message.channel.send("その絵文字は存在しません。") #TODO 今後送信したユーザーにのみ表示されるようにする
            else: #絵文字のURLが存在するなら
                username = message.author.display_name #ユーザー名を取得
                avatar_of_user= message.author.display_avatar #ユーザーのアバターを取得
                #スタンプの内容を作成
                stamp_content = {
                    "username": username,
                    "avatar_url": str(avatar_of_user), #アバターのURLを文字列に変換 っていうかasset型ってなんだよ
                    "content": emoji_URL #TODO 今後embedを使うようにする
                }
                #スタンプを送信
                requests.post(dcURLs["emojis"]["hiroba"], json.dumps(stamp_content), headers=headers)
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

#HELPコマンド
@bot.command(name="HELP", description="コマンド一覧を表示します。", guild_ids=["1109024847432007771"])
async def HELP(ctx):
    #helpメッセージを作成
    message = """
## コマンド一覧
 - /ping: pingを返します。
 - /HELP: コマンド一覧を表示します。
## スタンプ
 - "$"で始まるメッセージを送信すると、対応するスタンプを送信できます。
"""
    #helpメッセージを送信
    await ctx.send(message)

#実行
bot.run(dcToken) #botを実行

#このdiscord botは、大豆共和国の管理をするbotです。botの名前は、大豆共和国警察庁長官です。



###必要なライブラリをインポート###

import discord #pycord discord関連のライブラリ
import asyncio #非同期処理のライブラリ
import requests #HTTPリクエストを送信するライブラリ
import os #os関連の処理をするライブラリ
import json #jsonファイルを扱うライブラリ
from os import path #pathを扱うライブラリ 
from discord.ext import commands #discord botのコマンドを扱うライブラリ



###デバックモード###

#デバックモードを有効にする
debug = True



###初期設定###


#bot関連

#botの権限 .allで全ての権限を与える。
intents = discord.Intents.all()
#botを定義する
bot = commands.Bot(intents=intents, command_prefix="/")


#ファイルの読み込み

#jsonファイルからconfig情報を取得する
with open(path.join(path.dirname(__file__), "config.json"), "r") as f:
    config = json.load(f) #configにjsonファイルの内容を代入
#jsonファイルから絵文字の情報を取得する
with open(path.join(path.dirname(__file__), "emojis.json"), "r") as f:
    emojis = json.load(f) #emojisにjsonファイルの内容を代入


#定数

#discordのトークン
dcToken = config["keys"]["dcToken"]
#discordのwebhookのURL
dcURLs = config["webhookURLs"]
#headerの設定
headers = {'Content-Type': 'application/json'}


###discordイベント###

#botが起動したときの処理
@bot.event
async def on_ready():
    print("bot is ready")   #botが起動したことを表示
    global announcementChannel #アナウンスチャンネルをグローバル変数として定義
    announcementChannel = bot.get_channel(1124899720872067122) #アナウンスチャンネルを取得


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
        return #関数を終了する
    
    #メッセージが送信されたチャンネルが自己紹介チャンネルでないなら
    if message.content.startswith("$"): #メッセージが"$"で始まるなら
        #絵文字関連の処理をする
        await emoji(message)
        return #関数を終了する
    
    await bot.process_commands(message) #コマンドを処理する



###コマンド###

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
 - /create-stamp: スタンプを作成します。引数のnameにはスタンプの名前、image_urlにはスタンプの画像のURLを入力してください。
## スタンプ
 - "$"で始まるメッセージを送信すると、対応するスタンプを送信できます。
"""
    #helpメッセージを送信
    await ctx.send(message)


#スタンプを作成するコマンド
@bot.command(name="create-stamp", description="スタンプを作成します。", guild_ids=["1109024847432007771"])
async def create_stamp(ctx, name: str, image_url: str):
    #すでに同じ名前のスタンプがあるかどうかを判定
    if name in emojis:
        await ctx.send("すでに同じ名前のスタンプがあります。")
        return #関数を終了する
    #スタンプの情報を追加
    emojis[name] = image_url
    #スタンプの情報をjsonファイルに保存
    with open(path.join(path.dirname(__file__), "emojis.json"), "w") as f:
        json.dump(emojis, f, indent=4)
    #スタンプを作成したことを送信
    await announcementChannel.send(f"{ctx.author.mention}さんが、{name}という名前のスタンプを作成しました。")


@bot.command()
async def add(ctx: commands.Context, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(str(left + right))

                       


###関数###

#文章が自己紹介かどうかを判定する関数

def isSelfIntroduction(text,user):
    if user in text:
        return True
    else:
        return False


#絵文字関連の処理をする関数

async def emoji(message):
    #必要な情報を取得
    emoji_name = message.content[1:] #メッセージの先頭の"$"を削除
    emoji_URL = emojis.get(emoji_name) #絵文字のURLを取得
    username = message.author.display_name #ユーザー名を取得
    avatar_of_user= message.author.display_avatar #ユーザーのアバターを取得

    if emoji_URL == None: #絵文字のURLが存在しないなら
        await message.reply("その絵文字は存在しません。") #メッセージを送信 絵文字の新規追加を可能にする またこのメッセージは送信者のみ見られるようにする
    
    else: #絵文字のURLが存在するなら
        #スタンプの内容を作成
        stamp_content = {
            "username": username,
            "avatar_url": str(avatar_of_user), #アバターのURLを文字列に変換 っていうかasset型ってなんだよ
            "content": emoji_URL
        }
        #スタンプを送信
        requests.post(dcURLs["emojis"]["hiroba"], json.dumps(stamp_content), headers=headers)
        #元のメッセージを削除
        await message.delete()



###実行###

bot.run(dcToken) #botを実行

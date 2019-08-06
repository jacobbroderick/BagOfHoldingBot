# Work with Python 3.6
import configparser
import discord
from discord.ext import commands
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from tabulate import tabulate

from models import Base,  Member, Bag, BagItem 


config = configparser.ConfigParser()

config.read('config.ini')

TOKEN = config['DEFAULT']['BotToken']

print(TOKEN)

connectionString = 'mysql+pymysql://{}:{}@{}:3306/bag'.format(config['DEFAULT']['DBUser'], config['DEFAULT']['DBPass'], config['DEFAULT']['DBHost'])

engine = create_engine(connectionString , echo=False)
Session = sessionmaker(bind=engine)
session = Session()

if not engine.dialect.has_table(engine, 'event'):
    Base.metadata.create_all(engine)


description = 'bag of holding bot'
bot = commands.Bot(command_prefix='!', description=description)

@bot.command()
async def dump(ctx):
    server = ctx.guild.name
    try:
        bagItem = session.query(BagItem,Bag).filter(BagItem.bag_id == Bag.id).filter(Bag.server == server).all()
        if len(bagItem) > 1:
            for b in bagItem:
                session.query(BagItem).filter(BagItem.id == b.BagItem.id).delete()
                session.commit()
                await ctx.send('{} dropped'.format(b.BagItem.item))
    except Exception as e:
        await ctx.send('Could not complete your command')
        print(e)

@bot.command()
async def ping(ctx):
    author = ctx.message.author.name
    server = ctx.message.guild.name
    await ctx.send('Pong for {} from {}!'.format(author,server))

@bot.command()
async def hold(ctx, item:str):
    server = ctx.message.guild.name
    try:
        count = session.query(Bag).filter(Bag.server == server).count()
        if count < 1:
            bag = Bag(server = server)
            session.add(bag)
            session.commit()
        ServerBag = session.query(Bag).filter(Bag.server == server).one()
        bagItem = BagItem(bag_id = ServerBag.id, item = item)
        session.add(bagItem)
        session.commit()
        await ctx.send('{} Saved'.format(item))
    except Exception as e:
        await ctx.send('Could not complete your command')
        print(e)


@bot.command()
async def stop(ctx):
    await bot.logout()

@bot.command()
async def member(ctx):
    '''testing creating a member'''
    author = ctx.message.author.name
    avatar = ctx.message.author.avatar_url
    id = ctx.message.author.id
    try:
        count = session.query(Member).filter(Member.id == id).count()
        if count < 1:
            member = Member(id = id, name = author, avatar = str(avatar))
            session.add(member)
            session.commit()
            await ctx.send('Member created')
    except Exception as e:
        await ctx.send('Could not complete your command')
        print(e)
        


@bot.command()
async def list(ctx):
    '''Displays the current list of current events
        example: !list
    '''
    server = ctx.guild.name
    try:
        bagitems = session.query(BagItem,Bag).filter(Bag.server == server).filter(Bag.id == BagItem.bag_id).order_by(BagItem.id).all()
        headers = ['Item']
        rows = [[b.BagItem.item] for b in bagitems]
        table = tabulate(rows, headers)
        await ctx.send('```\n' + table + '```')
    except Exception as e:
        await ctx.send('Could not complete your command')
        print(e)

@bot.command()
async def drop(ctx, item: str):
    '''
        Removes an item from a bag of holding
    '''
    server = ctx.guild.name
    try:
        bagItem = session.query(BagItem,Bag).filter(BagItem.bag_id == Bag.id).filter(Bag.server == server).filter(BagItem.item == item).first()
        if len(bagItem) > 1:
            session.query(BagItem).filter(BagItem.id == bagItem.BagItem.id).delete()
            session.commit()
            await ctx.send('{} dropped'.format(item))
        else:
            await ctx.send('{} not in bag'.format(item))
    except Exception as e:
        await ctx.send('Could not complete your command')
        print(e)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(TOKEN)
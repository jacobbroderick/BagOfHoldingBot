# Work with Python 3.6
from os import getenv
import discord
from discord.ext import commands
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from tabulate import tabulate

from models import Base, Event, Member, Attendance

TOKEN = 'NTg0MTU5NjY4NzE3MzU1MDEz.XRGYQA.SRZLllwr-VfCC961d5594_mM3es'

engine = create_engine('mysql+pymysql://jacob:password@localhost:3306/bag', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

if not engine.dialect.has_table(engine, 'event'):
    Base.metadata.create_all(engine)


description = 'bag of holding bot'
bot = commands.Bot(command_prefix='!', description=description)


@bot.command(pass_context=True)
async def ping(ctx):
    author = ctx.message.author.name
    server = ctx.message.guild.name
    await ctx.send('Pong for {} from {}!'.format(author,server))

@bot.command(pass_context=True)
async def create(ctx, name: str, date: str, time: str='0:00am'):
    '''Creates an event with the specified name and date example
        !create party 12/22/2017 1:40pm
    '''
    server = ctx.message.guild.name
    date_time = '{} {}'.format(date, time)
    try:
        event_date = datetime.strptime(date_time, '%m/%d/%Y %I:%M%p')
        event = Event(name=name, server=server,date=event_date)
        session.add(event)
        session.commit()
        await ctx.send('Event {} created successfully for {}'.format(name,event.date))
    except Exception as e:
        await ctx.send('Could not complete your command')
        print(e)

@bot.command()
async def member(ctx):
    '''testing creating a member'''
    author = ctx.message.author.name
    avatar = ctx.message.author.avatar_url
    id = ctx.message.author.id
    print(type(id))
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
    try:
        events = session.query(Event).order_by(Event.id).all()
        headers = ['Name','Date','Server']
        rows = [[e.name, e.date, e.server] for e in events]
        table = tabulate(rows, headers)
        await ctx.send('```\n' + table + '```')
    except Exception as e:
        await ctx.send('Could not complete your command')
        print(e)

@bot.command()
async def attend(ctx, name: str):
    '''Allows a user to attend an upcoming event
    example: !attend party
    '''
    author = ctx.message.author.name
    avatar = ctx.message.author.avatar_url
    id = ctx.message.author.id
    print(type(id))
    try:
        count = session.query(Member).filter(Member.id == id).count()
        event = session.query(Event).filter(Event.name == name).first()

        if not event:
            await ctx.send('This event does not exist')
            return
        
        if count < 1:
            member = Member(id = id, name = author, avatar = str(avatar))
            session.add(member)
        
        attending = Attendance(member_id = id, event_id = event.id)
        session.add(attending)
        session.commit()
        await ctx.send('Member {} is now attending event {}'.format(author, name))
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
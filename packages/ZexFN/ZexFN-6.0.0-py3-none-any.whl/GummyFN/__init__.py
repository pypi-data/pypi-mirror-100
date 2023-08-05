"""This example showcases how to use fortnitepy. If captcha is enforced for
the account, you will only have to enter the authorization code the first time
you run this script.
NOTE: This example uses AdvancedAuth and stores the details in a file.
It is important that this file is moved whenever the script itself is moved
because it relies on the stored details. However, if the file is nowhere to

be found, it will simply use email and password or prompt you to enter a
new authorization code to generate a new file.
"""
 
import fortnitepy
import sanic
import json
import os
import sanic
from flask import Flask, render_template, redirect, url_for, request
import traceback
import json
import time
from termcolor import colored
import os
import discord
from discord.ext import commands as discord_commands


from threading import Thread
import logging
from fortnitepy.ext import commands as fortnite_commands
import aioconsole
from typing import Optional

from fortnitepy.ext import commands
import BenBotAsync

from functools import partial

import asyncio
# Third party imports.

import requests
import sys

import crayons




with open('Settings.json') as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(colored("There was an error in one of the bot's files! (Settings.json). If you have problems trying to fix it, join the discord support server for help - https://discord.gg/ugUTsaz", "red"))
        print(colored(f'\n {e}', 'red'))
        exit(1)



server = None


filename = 'device_auths.json'
description = 'My discord + fortnite bot!'



def getNewSkins():
    r = requests.get('https://benbotfn.tk/api/v1/files/added')

    response = r.json()

    cids = []

    for cid in [item for item in response if item.split('/')[-1].upper().startswith('CID_')]:
        cids.append(cid.split('/')[-1].split('.')[0])
    
    return cids

def getNewEmotes():
    r = requests.get('https://benbotfn.tk/api/v1/files/added')

    response = r.json()

    eids = []

    for cid in [item for item in response if item.split('/')[-1].upper().startswith('EID_')]:
        eids.append(cid.split('/')[-1].split('.')[0])
    
    return eids

def get_device_auth_details():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(Email, details):
    existing = get_device_auth_details()
    existing[Email] = details


    with open(filename, 'w') as fp:
        json.dump(existing, fp)



def is_admin():
    async def predicate(ctx):
        return ctx.author.id in data['Control']['Give full access to']
    return commands.check(predicate)

async def get_authorization_code():
    while True:
        response = await aioconsole.ainput("Go to https://rebrand.ly/authcode and sign in as "  + data['Account']['Email'] + " and enter the response: ")
        if "redirectUrl" in response:
            response = json.loads(response)
            if "?code" not in response["redirectUrl"]:
                print(colored("Invalid response.", "red"))
                continue
            code = response["redirectUrl"].split("?code=")[1]
            return code
        else:
            if "https://accounts.epicgames.com/fnauth" in response:
                if "?code" not in response:
                    print(colored("invalid response.", "red"))
                    continue
                code = response.split("?code=")[1]
                return code
            else:
                code = response
                return code

device_auth_details = get_device_auth_details().get(data['Account']['Email'], {})
fortnite_bot  = fortnite_commands.Bot(
    command_prefix=data['Account']['Prefix'],case_insensitive=True,
    auth=fortnitepy.AdvancedAuth(
        Email=data['Account']['Email'],
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        authorization_code=get_authorization_code,
         **device_auth_details
    ),
    status=data['Party']['Status'],
    platform=fortnitepy.Platform(data['Party']['Platform']),
)
sanic_app = sanic.Sanic(__name__)
server = None
discord_bot = discord_commands.Bot(
        command_prefix=data['Account']['Prefix'],
        description=description,
        case_insensitive=True
    )
discord_bot.remove_command('help')
T = data['Account']['Prefix']

@fortnite_bot.event
async def event_device_auth_generate(details, Email):
    store_device_auth_details(data['Account']['Email'], details)

@fortnite_bot.event
async def event_ready():
    global server
    
    member = fortnite_bot.party.me
    await member.edit_and_keep(
        partial(
            fortnitepy.ClientPartyMember.set_outfit,
            asset=data['Party']['Cosmetics']['Skin']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_backpack,
            asset=data['Party']['Cosmetics']['Backpack']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_pickaxe,
            asset=data['Party']['Cosmetics']['Pickaxe']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_emote,
            asset=data['Party']['Cosmetics']['Emote']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_banner,
            icon=data['Party']['Cosmetics']['Banner']['Banner Name'],
            color=data['Party']['Cosmetics']['Banner']['Banner Color'],
            season_level=data['Party']['Cosmetics']['Banner']['Season Level']
        ),
        partial(
            fortnitepy.ClientPartyMember.set_battlepass_info,
            has_purchased=True,
            level=data['Party']['Cosmetics']['Banner']['battle pass tier']
        )
    )

    fortnite_bot.set_avatar(fortnitepy.Avatar(asset='cid_757_8b3428d3e5cb239d78e21d7c9f560351929cff957ea3638f74910e9321e4e71b', background_colors=['#ffffff', '#ee1064', '#ff0000']))
    log = logging.getLogger('werkzeug')
    log.disabled = True
    Thread(target=app.run,args=("0.0.0.0",8080)).start()
    time.sleep(1)
    print(colored('----------------', 'green'))
    print(colored('Bot started.', 'green'))

    print(colored(f'Bots UserName : {fortnite_bot.user.display_name}', 'green'))

    print(colored(f'Bots UserID : {fortnite_bot.user.id}', 'green'))

    print(colored(f'Platform : {(str((fortnite_bot.platform))[9:]).lower().capitalize()}', 'green'))
    print(colored('UseCode zfn ', 'green')) 
    print(colored('----------------', 'green'))

    
    if data['Discord']['Token'] == '':
        print("no token")
    else:
        await discord_bot.start(data['Discord']['Token'])

    
    
    

    


@fortnite_bot.event
async def event_before_close():
    await discord_bot.close()


@discord_bot.event
async def on_ready():

    await discord_bot.change_presence(status=discord.Status.idle, activity=discord.Game(f'{T}help'))
    
    print(f'bot: {discord_bot.user.name}#{discord_bot.user.discriminator}')




	    
@discord_bot.event
async def on_message(message):
    if message.author.bot:
        return

    await discord_bot.process_commands(message)

@fortnite_bot.event
async def event_friend_add(Friend):
    if not data['Friends']['Accept all friend requestst']:
        if not Friend.id in data['Control']['Give full access to']:
            return
    
    try:
        await Friend.invite()
        

    except:
        pass




@fortnite_bot.event
async def event_party_member_join(member: fortnitepy.PartyMember) -> None:
        try:
           await fortnite_bot.party.me.set_emote(f"{fortnite_bot.party.me.emote}")
           await fortnite_bot.party.send(data['Party']['Join Message'])
        except Exception:
            pass
    

@fortnite_bot.event
async def event_party_invite(invite):
    if data['Party']['Join party on invitation'].lower() == 'true':
        try:
            await invite.accept()
            print(colored(f'Accepted party invite from {invite.sender.display_name}', 'blue'))
        except Exception:
            pass
    elif data['Party']['Join party on invitation'].lower() == 'false':
        if invite.sender.id in data['Control']['Give full access to']:
            await invite.accept()
            print(colored(f'Accepted party invite from {invite.sender.display_name}', 'blue'))
        else:
            print(colored(f'Never accepted party invite from {invite.sender.display_name}', 'red'))

def lenFriends():
    friends = fortnite_bot.friends
    return len(friends)

def lenPartyMembers():
    members = fortnite_bot.party.members
    return len(members)
    
@fortnite_bot.event
async def event_party_member_promote(old_leader, new_leader):
    if new_leader.id == fortnite_bot.user.id:
        await fortnite_bot.party.send(f"Thanks {old_leader.display_name} for promoting me ♥")
        await fortnite_bot.party.me.set_emote("EID_TrueLove")


@fortnite_bot.event
async def event_friend_request(request):
    if data['Friends']['Accept all friend requests'].lower() == 'true':
        try:
            await request.accept()
            print(colored(f'Accepted friend request from {request.display_name}' + f' ({lenFriends()})', 'blue'))
        
        except Exception:
            pass
    elif data['Friends']['Accept all friend requests'].lower() == 'false':
        if request.id in data['Control']['Give full access to']:
            try:
                await request.accept()
                print(colored('Accepted friend request from '  + f'{request.display_name}' + f' ({lenFriends()})', 'blue'))
                
            except Exception:
                pass
        else:
            print(colored(f'Never accepted friend request from {request.display_name}', 'red'))
@fortnite_bot.event
async def event_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('That is not a command. Try !help')
    elif isinstance(error, IndexError):
        pass
    elif isinstance(error, fortnitepy.HTTPException):
        pass
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have access to that command.")
    elif isinstance(error, TimeoutError):
        await ctx.send("You took too long to respond!")
    else:
        print(error)

@fortnite_bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

async def set_and_update_party_prop(schema_key: str, new_value: str):
    prop = {schema_key: fortnite_bot.party.me.meta.set_prop(schema_key, new_value)}
    await fortnite_bot.party.patch(updated=prop)

@fortnite_bot.command()
@is_admin()
async def unhide(ctx, *, epic_username: Optional[str] = None) -> None:
    if epic_username is None:
        user = await fortnite_bot.fetch_user(ctx.author.display_name)
        member = fortnite_bot.party.get_member(user.id)
    else:
        user = await fortnite_bot.fetch_user(epic_username)
        member = fortnite_bot.party.get_member(user.id)

    if member is None:
        await ctx.send("Failed to find that user, are you sure they're in the party?")
    else:
        try:
            await member.promote()
            await ctx.send("unhid everyone")
        except fortnitepy.errors.Forbidden:
            await ctx.send("i found unhide report in server.")
            print(crayons.red("Failed to unhide members as I don't have the required permissions."))


@fortnite_bot.command()
async def emote(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No emote was given, try: {T}emote (emote name)')
    elif content.lower() == 'floss':
        await fortnite_bot.party.me.clear_emote()
        await fortnite_bot.party.me.set_emote(asset='EID_Floss')
        await ctx.send('Emote set to: Floss')
    elif content.lower() == 'none':
        await fortnite_bot.party.me.clear_emote()
        await ctx.send('Emote set to: None')
    elif content.upper().startswith('EID_'):
        await fortnite_bot.party.me.clear_emote()
        await fortnite_bot.party.me.set_emote(asset=content.upper())
        await ctx.send(f'Emote set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await fortnite_bot.party.me.clear_emote()
            await fortnite_bot.party.me.set_emote(asset=cosmetic.id)
            await ctx.send(f'Emote set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find an emote named: {content}')


@fortnite_bot.command()
@is_admin()
async def promote(ctx, *, epic_username: Optional[str] = None) -> None:
    if epic_username is None:
        user = await fortnite_bot.fetch_user(ctx.author.display_name)
        member = fortnite_bot.party.get_member(user.id)
    else:
        user = await fortnite_bot.fetch_user(epic_username)
        member = fortnite_bot.party.get_member(user.id)

    if member is None:
        await ctx.send("Failed to find that user, are you sure they're in the party?")
    else:
        try:
            await member.promote()
            await ctx.send(f"Promoted user: {member.display_name}.")
            print(colored(f"Promoted user: {member.display_name}", "blue"))
        except fortnitepy.errors.Forbidden:
            await ctx.send(f"Failed topromote {member.display_name}, as I'm not party leader.")
            print(crayons.red("Failed to promote member as I don't have the required permissions."))


@fortnite_bot.command()
@is_admin()
async def hide(ctx, *, user = None):
    if fortnite_bot.party.me.leader:
        if user != None:
            try:
                if user is None:
                    user = await fortnite_bot.fetch_profile(ctx.message.author.id)
                    member = fortnite_bot.party.members.get(user.id)
                else:
                    user = await fortnite_bot.fetch_profile(user)
                    member = fortnite_bot.party.members.get(user.id)

                raw_squad_assignments = fortnite_bot.party.meta.get_prop('Default:RawSquadAssignments_j')["RawSquadAssignments"]

                for m in raw_squad_assignments:
                    if m['memberId'] == member.id:
                        raw_squad_assignments.remove(m)

                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j',
                    {
                        'RawSquadAssignments': raw_squad_assignments
                    }
                )

                await ctx.send(f"Hid {member.display_name}")
            except AttributeError:
                await ctx.send("I could not find that user.")
            except fortnitepy.HTTPException:
                await ctx.send("I am not party leader.")
        else:
            try:
                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j',
                    {
                        'RawSquadAssignments': [
                            {
                                'memberId': fortnite_bot.user.id,
                                'absoluteMemberIdx': 1
                            }
                        ]
                    }
                )

                await ctx.send("Hid everyone in the party.")
            except fortnitepy.HTTPException:
                await ctx.send("I am not party leader.")
    else:
        await ctx.send("I need party leader to do this!")


@fortnite_bot.command()
@is_admin()
async def add(ctx, *, member = None):
    if member is not None:
        try:
            user = await fortnite_bot.fetch_profile(member)
            friends = fortnite_bot.friends

            if user.id in friends:
                await ctx.send(f"I already have {user.display_name} as a friend")
            else:
                await fortnite_bot.add_friend(user.id)
                await ctx.send(f'Sent a friend request to {user.display_name}')
                print('Sent a friend request to: ' f'{user.display_name}')

        except fortnitepy.HTTPException:
            await ctx.send("There was a problem trying to add this friend.")
        except AttributeError:
            await ctx.send("I can't find a player with that name.")
    else:
        await ctx.send(f"No user was given. Try: {T}add (user)")

@fortnite_bot.command()
async def pickaxe(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No pickaxe was given, try: {T}pickaxe (pickaxe name)')
    elif content.upper().startswith('Pickaxe_'):
        await fortnite_bot.party.me.set_pickaxe(asset=content.upper())
        await ctx.send(f'Pickaxe set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )
            await fortnite_bot.party.me.set_pickaxe(asset=cosmetic.id)
            await ctx.send(f'Pickaxe set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pickaxe named: {content}')


@fortnite_bot.command()
async def pet(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No pet was given, try: {T}pet (pet name)')
    elif content.lower() == 'none':
        await fortnite_bot.party.me.clear_pet()
        await ctx.send('Pet set to: None')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPet"
            )
            await fortnite_bot.party.me.set_pet(asset=cosmetic.id)
            await ctx.send(f'Pet set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a pet named: {content}')

@fortnite_bot.command()
async def season(ctx):
    await ctx.send("Level 1")
    await fortnite_bot.party.me.set_banner(season_level="1")
    await fortnite_bot.party.me.set_outfit(asset="cid_989_athena_commando_m_progressivejonesy")
    await asyncio.sleep(1.25)

    await fortnite_bot.party.me.set_emote(asset="EID_Custodial")
    await asyncio.sleep(1.25)

    await ctx.send("Level 15")
    await fortnite_bot.party.me.set_banner(season_level="15")
    await fortnite_bot.party.me.set_outfit(asset="cid_a_040_athena_commando_f_temple")
    await asyncio.sleep(1.25)
    
    await fortnite_bot.party.me.set_emote(asset="EID_Temple")
    await asyncio.sleep(1.25)

    await ctx.send("Level 29")
    await fortnite_bot.party.me.set_banner(season_level="29")
    await fortnite_bot.party.me.set_outfit(asset="cid_a_037_athena_commando_f_dinohunter")
    await asyncio.sleep(1.25)
    
    await fortnite_bot.party.me.set_emote(asset="EID_Suits")
    await asyncio.sleep(1.25)

    await ctx.send("Level 50")
    await fortnite_bot.party.me.set_banner(season_level="50")
    await fortnite_bot.party.me.set_outfit(asset="cid_a_041_athena_commando_m_cubeninja")
    await asyncio.sleep(1.25)

    await fortnite_bot.party.me.set_emote(asset="EID_CloudFloat")
    await asyncio.sleep(1.25)

    await ctx.send("Level 61")
    await fortnite_bot.party.me.set_banner(season_level="61")
    await fortnite_bot.party.me.set_outfit(asset="cid_a_039_athena_commando_m_chickenwarrior")
    await asyncio.sleep(1.25)

    await fortnite_bot.party.me.set_emote(asset="EID_BootsAndCats")
    await asyncio.sleep(1.25)

    await ctx.send("Level 77")
    await fortnite_bot.party.me.set_banner(season_level="77")
    await fortnite_bot.party.me.set_outfit(asset="cid_a_036_athena_commando_f_obsidian")
    await asyncio.sleep(1.25)

    await fortnite_bot.party.me.set_emote(asset="EID_Obsidian")
    await asyncio.sleep(1.25)

    await ctx.send("Level 100")
    await fortnite_bot.party.me.set_banner(season_level="100")
    await fortnite_bot.party.me.set_outfit(asset="cid_a_038_athena_commando_f_towersentinel")
    await asyncio.sleep(1.25)
    
    await fortnite_bot.party.me.set_emote(asset="EID_TowerSentinel")
    await asyncio.sleep(1.25)

    await ctx.send(
        "done"
    )

@fortnite_bot.command()
async def backpack(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No backpack was given, try: {T}backpack (backpack name)')
    elif content.lower() == 'none':
        await fortnite_bot.party.me.clear_backpack()
        await ctx.send('Backpack set to: None')
    elif content.upper().startswith('BID_'):
        await fortnite_bot.party.me.set_backpack(asset=content.upper())
        await ctx.send(f'Backpack set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )
            await fortnite_bot.party.me.set_backpack(asset=cosmetic.id)
            await ctx.send(f'Backpack set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a backpack named: {content}')

@fortnite_bot.command()
async def pinkghoul(ctx):
    variants = fortnite_bot.party.me.create_variants(material=3)

    await fortnite_bot.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=variants
    )

    await ctx.send('Skin set to: Pink Ghoul Trooper')


@fortnite_bot.command()
async def purpleskull(ctx):
    variants = fortnite_bot.party.me.create_variants(clothing_color=1)

    await fortnite_bot.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants = variants
    )

    await ctx.send('Skin set to: Purple Skull Trooper')




@fortnite_bot.command()
async def hatlessrecon(ctx):
    variants = fortnite_bot.party.me.create_variants(parts=2)

    await fortnite_bot.party.me.set_outfit(
        asset='CID_022_Athena_Commando_F',
        variants=variants
    )

    await ctx.send('Skin set to: Hatless Recon Expert')



@fortnite_bot.command()
async def hologram(ctx):
    await fortnite_bot.party.me.set_outfit(
        asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
    )
    
    await ctx.send("Skin set to: Hologram")




@fortnite_bot.command()
async def new(ctx, content = None):
    newSkins = getNewSkins()
    newEmotes = getNewEmotes()

    previous_skin = fortnite_bot.party.me.outfit

    if content is None:
        await ctx.send(f'There are {len(newSkins) + len(newEmotes)} new skins + emotes')

        for cosmetic in newSkins + newEmotes:
            if cosmetic.startswith('CID_'):
                await fortnite_bot.party.me.set_outfit(asset=cosmetic)
                await asyncio.sleep(4)
            elif cosmetic.startswith('EID_'):
                await fortnite_bot.party.me.clear_emote()
                await fortnite_bot.party.me.set_emote(asset=cosmetic)
                await asyncio.sleep(4)

    elif 'skin' in content.lower():
        await ctx.send(f'There are {len(newSkins)} new skins')

        for skin in newSkins:
            await fortnite_bot.party.me.set_outfit(asset=skin)
            await asyncio.sleep(4)

    elif 'emote' in content.lower():
        await ctx.send(f'There are {len(newEmotes)} new emotes')

        for emote in newEmotes:
            await fortnite_bot.party.me.clear_emote()
            await fortnite_bot.party.me.set_emote(asset=emote)
            await asyncio.sleep(4)

    await fortnite_bot.party.me.clear_emote()
    
    await ctx.send('Done!')

    await asyncio.sleep(1.5)

    await fortnite_bot.party.me.set_outfit(asset=previous_skin)

    if (content is not None) and ('skin' or 'emote' not in content.lower()):
        ctx.send(f"Not a valid option. Try: {T}new (skins, emotes)")



@fortnite_bot.command()
async def style(ctx: fortnitepy.ext.commands.Context, cosmetic_name: str, variant_type: str, variant_int: str) -> None:
        # cosmetic_types = {
        #     "AthenaCharacter": self.bot.party.me.set_outfit,
        #     "AthenaBackpack": self.bot.party.me.set_backpack,
        #     "AthenaPickaxe": self.bot.party.me.set_pickaxe
        # }

    cosmetic = await fortnite_bot.fortnite_api.cosmetics.get_cosmetic(
        lang="en",
        searchLang="en",
        matchMethod="contains",
        name=cosmetic_name,
        backendType="AthenaCharacter"
    )

    cosmetic_variants =fortnite_bot.party.me.create_variants(
            # item=cosmetic.backend_type.value,
        **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
    )

        # await cosmetic_types[cosmetic.backend_type.value](
    await fortnite_bot.party.me.set_outfit(
        asset=cosmetic.id,
        variants=cosmetic_variants
    )

    await ctx.send(f'Set variants of {cosmetic.id} to {variant_type} {variant_int}.')

@fortnite_bot.command()
async def ready(ctx):
    await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.READY)
    await ctx.send('Ready!')



@fortnite_bot.command()
async def unready(ctx):
    await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('Unready!')



@fortnite_bot.command()
async def skin(ctx, *, content = None):
    if content is None:
        await ctx.send(f'No skin was given, try: {T}!skin (skin name)')
    elif content.upper().startswith('CID_'):
        await fortnite_bot.party.me.set_outfit(asset=content.upper())
        await ctx.send(f'Skin set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                name=content,
                backendType="AthenaCharacter"
            )
            await fortnite_bot.party.me.set_outfit(asset=cosmetic.id)
            await ctx.send(f'Skin set to: {cosmetic.name}')
        except BenBotAsync.exceptions.NotFound:
            await ctx.send(f'Could not find a skin named: {content}')


@fortnite_bot.command()
async def sitin(ctx):
    await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    await ctx.send('Sitting in')


@fortnite_bot.command()
async def sitout(ctx):
    await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    await ctx.send('Sitting out')


@fortnite_bot.command()
async def tier(ctx, tier = None):
    if tier is None:
        await ctx.send(f'No tier was given. Try: {T}tier (tier number)') 
    else:
        await fortnite_bot.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier
        )

        await ctx.send(f'Battle Pass tier set to: {tier}')


@fortnite_bot.command()
async def level(ctx, level = None):
    if level is None:
        await ctx.send(f'No level was given. Try: {T}level (number)')
    else:
        await fortnite_bot.party.me.set_banner(season_level=level)
        await ctx.send(f'Level set to: {level}')




copied_player = ""




@fortnite_bot.command()
async def copy(ctx, *, username = None):
    global copied_player

    if username is None:
        member = [m for m in fortnite_bot.party.members if m.id == ctx.author.id][0]

    else:
        user = await fortnite_bot.fetch_user(username)
        member = [m for m in fortnite_bot.party.members if m.id == user.id][0]

    await fortnite_bot.party.me.edit_and_keep(
            partial(
                fortnitepy.ClientPartyMember.set_outfit,
                asset=member.outfit,
                variants=member.outfit_variants
            ),
            partial(
                fortnitepy.ClientPartyMember.set_backpack,
                asset=member.backpack,
                variants=member.backpack_variants
            ),
            partial(
                fortnitepy.ClientPartyMember.set_pickaxe,
                asset=member.pickaxe,
                variants=member.pickaxe_variants
            ),
            partial(
                fortnitepy.ClientPartyMember.set_banner,
                icon=member.banner[0],
                color=member.banner[1],
                season_level=member.banner[2]
            ),
            partial(
                fortnitepy.ClientPartyMember.set_battlepass_info,
                has_purchased=member.battlepass_info[0],
                level=member.battlepass_info[1]
            ),
            partial(
                fortnitepy.ClientPartyMember.set_emote,
                asset=member.emote
            )
        )

    await ctx.send(f"Now copying: {member.display_name}")

@fortnite_bot.command()
async def yankee(ctx):

    await fortnite_bot.party.me.set_outfit(
        asset='CID_A_044_Athena_Commando_F_NeonCatFashion_64JW3'
		)
    await ctx.send('Skin set to: yankee')


@fortnite_bot.command()
async def goldpeely(ctx):
    variants = fortnite_bot.party.me.create_variants(progressive=4)

    await fortnite_bot.party.me.set_outfit(
        asset='CID_701_Athena_Commando_M_BananaAgent',
        variants=variants,
        enlightenment=(2, 350)
    )
    await ctx.send('Skin set to: Golden Peely')

#discord command ##################################################################

@discord_bot.command()
async def skin(ctx, *, content = None):
    if content is None:
        embed = discord.Embed(title='', color=0xfc4267)
        embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```No skin was given, try: {T}skin (skin name)```', inline=False)
        await ctx.send(embed=embed)
    elif content.upper().startswith('CID_'):
        await fortnite_bot.party.me.set_outfit(asset=content.upper())
        embed = discord.Embed(title='', color=0xfc4267)
        embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```The cid: {content} was successfully equipped```', inline=False)
        embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{content}/icon.png")
        await ctx.send(embed=embed)
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                name=content,
                backendType="AthenaCharacter"
            )
            await fortnite_bot.party.me.set_outfit(asset=cosmetic.id)
            embed = discord.Embed(title='', color=0xfc4267)
            embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```The skin {cosmetic.name} was successfully equipped```', inline=False)
            embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{cosmetic.id}/icon.png")
            await ctx.send(embed=embed)
        except BenBotAsync.exceptions.NotFound:
            embed = discord.Embed(title='', color=0xfc4267)
            embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```The skin {content} wasn\'t found```', inline=False)
            
            await ctx.send(embed=embed)

@discord_bot.command()
async def yankee(ctx):

    await fortnite_bot.party.me.set_outfit(
        asset='CID_A_044_Athena_Commando_F_NeonCatFashion_64JW3'
		)
    embed = discord.Embed(title='', color=0xfc4267)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```Skin set to: yankee``', inline=False)
    await ctx.send(embed=embed)
		
@discord_bot.command()
async def goldpeely(ctx):
    variants = fortnite_bot.party.me.create_variants(progressive=4)

    await fortnite_bot.party.me.set_outfit(
        asset='CID_701_Athena_Commando_M_BananaAgent',
        variants=variants,
        enlightenment=(2, 350)
    )
    embed = discord.Embed(title='', color=0xfc4267)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```Skin set to: Golden Peely```', inline=False)
    embed.set_thumbnail(url="https://benbotfn.tk/cdn/images/CID_701_Athena_Commando_M_BananaAgent/variant/Progressive/Stage4.png")
    await ctx.send(embed=embed)

@discord_bot.command()
async def level(ctx, level = None):
    if level is None:
        embed = discord.Embed(title='', color=0xfc4267)
        embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```No level was given. Try: {T}level (number)```', inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='', color=0xfc4267)
        embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```The bots party level was successfully set to {level}```', inline=False)
        await fortnite_bot.party.me.set_banner(season_level=level)
        await ctx.send(embed=embed)

@discord_bot.command()
async def pinkghoul(ctx):
    variants = fortnite_bot.party.me.create_variants(material=3)

    await fortnite_bot.party.me.set_outfit(
        asset='CID_029_Athena_Commando_F_Halloween',
        variants=variants
    )
    embed = discord.Embed(title='', color=0xfc4267)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```Skin set to: Pink Ghoul Trooper```', inline=False)
    embed.set_thumbnail(url="https://benbotfn.tk/cdn/images/CID_029_Athena_Commando_F_Halloween/variant/Material/Mat3.png")
    await ctx.send(embed=embed)


@discord_bot.command()
async def style(ctx: fortnitepy.ext.commands.Context, cosmetic_name: str, variant_type: str, variant_int: str) -> None:
        # cosmetic_types = {
        #     "AthenaCharacter": self.bot.party.me.set_outfit,
        #     "AthenaBackpack": self.bot.party.me.set_backpack,
        #     "AthenaPickaxe": self.bot.party.me.set_pickaxe
        # }

    cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                name=cosmetic_name,
                backendType="AthenaCharacter"
            )

    cosmetic_variants =fortnite_bot.party.me.create_variants(
            # item=cosmetic.backend_type.value,
        **{variant_type: int(variant_int) if variant_int.isdigit() else variant_int}
    )

        # await cosmetic_types[cosmetic.backend_type.value](
    await fortnite_bot.party.me.set_outfit(
        asset=cosmetic.id,
        variants=cosmetic_variants
    )
    
    embed = discord.Embed(title='', color=0xfc4267)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```Set variants of {cosmetic.id} to {variant_type} {variant_int}.```', inline=False)
    await ctx.send(embed=embed)

@discord_bot.command()
async def emote(ctx, *, content = None):
    if content is None:
        embed = discord.Embed(title='', color=0xfc4267)
        embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```No emote was given, try: {T}emote (emote name)```', inline=False)
        await ctx.send(embed=embed)
    elif content.lower() == 'floss':
        await fortnite_bot.party.me.clear_emote()
        await fortnite_bot.party.me.set_emote(asset='EID_Floss')
        await ctx.send('Emote set to: Floss')
    elif content.lower() == 'none':
        await fortnite_bot.party.me.clear_emote()
        await ctx.send('Emote set to: None')
    elif content.upper().startswith('EID_'):
        await fortnite_bot.party.me.clear_emote()
        await fortnite_bot.party.me.set_emote(asset=content.upper())
        await ctx.send(f'Emote set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaDance"
            )
            await fortnite_bot.party.me.clear_emote()
            await fortnite_bot.party.me.set_emote(asset=cosmetic.id)
            embed = discord.Embed(title='', color=0xfc4267)
            embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```The emote {cosmetic.name} was successfully equipped```', inline=False)
            embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{cosmetic.id}/icon.png")
            await ctx.send(embed=embed)
        except BenBotAsync.exceptions.NotFound:
            embed = discord.Embed(title='', color=0xfc4267)
            embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```The emote {content} wasn\'t found```', inline=False)
            await ctx.send(embed=embed)

async def set_and_update_party_prop(schema_key: str, new_value: str):
    prop = {schema_key: fortnite_bot.party.me.meta.set_prop(schema_key, new_value)}
    await fortnite_bot.party.patch(updated=prop)

@discord_bot.command()
async def unhide(ctx, *, epic_username: Optional[str] = None) -> None:
    if epic_username is None:
        user = await fortnite_bot.fetch_user(ctx.author.display_name)
        member = fortnite_bot.party.get_member(user.id)
    else:
        user = await fortnite_bot.fetch_user(epic_username)
        member = fortnite_bot.party.get_member(user.id)

    if member is None:
        embed = discord.Embed(title='', color=0xfc4267)
        embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```Failed to find that user, are you sure they\'re in the party?```', inline=False)
        await ctx.send(embed=embed)
    else:
        try:
            await member.promote()
            embed = discord.Embed(title='', color=0xfc4267)
            embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```unhid everyone```', inline=False)
            await ctx.send(embed=embed)
        except fortnitepy.errors.Forbidden:
            embed = discord.Embed(title='', color=0xfc4267)
            embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```i found unhide report in server.```', inline=False)
            await ctx.send(embed=embed)
            print(crayons.red("Failed to unhide members as I don't have the required permissions."))
@discord_bot.command()
async def pickaxe(ctx, *, content = None):
    if content is None:
        embed = discord.Embed(title='', color=0xfc4267)
        embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```No pickaxe was given, try: {T}pickaxe (pickaxe name)```', inline=False)
        await ctx.send(embed=embed)
    elif content.upper().startswith('Pickaxe_'):
        await fortnite_bot.party.me.set_pickaxe(asset=content.upper())
        embed = discord.Embed(title='', color=0xfc4267)
        embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```Pickaxe set to: {content}```', inline=False)
        await ctx.send(embed=embed)
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPickaxe"
            )
            await fortnite_bot.party.me.set_pickaxe(asset=cosmetic.id)  
            embed = discord.Embed(title='', color=0xfc4267)
            embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```The Pickaxe {cosmetic.name} was successfully equipped```', inline=False)
            embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{cosmetic.id}/icon.png")
            await ctx.send(embed=embed)
        except BenBotAsync.exceptions.NotFound:
            embed = discord.Embed(title='', color=0xfc4267)
            embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```The pickaxe {content} wasn\'t found```', inline=False)
            await ctx.send(embed=embed)

@discord_bot.command()
async def pet(ctx, *, content = None):
    if content is None:
        embed = discord.Embed(title='', color=0xfc4267)
        embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```No pet was given, try: {T}pet (pet name)```', inline=False)
        await ctx.send(embed=embed)
    elif content.lower() == 'none':
        await fortnite_bot.party.me.clear_pet()
        embed = discord.Embed(title='', color=0xfc4267)
        embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```Pet set to: None```', inline=False)
        await ctx.send(embed=embed)
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaPet"
            )
            await fortnite_bot.party.me.set_pet(asset=cosmetic.id)
            embed = discord.Embed(title='', color=0xfc4267)
            embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```The Pet {cosmetic.name} was successfully equipped```', inline=False)
            embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{cosmetic.id}/icon.png")
            await ctx.send(embed=embed)
        except BenBotAsync.exceptions.NotFound:
            embed = discord.Embed(title='', color=0xfc4267)
            embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```The pet {content} wasn\'t found```', inline=False)
            await ctx.send(embed=embed)
@discord_bot.command()
async def purpleskull(ctx):
    variants = fortnite_bot.party.me.create_variants(clothing_color=1)

    await fortnite_bot.party.me.set_outfit(
        asset='CID_030_Athena_Commando_M_Halloween',
        variants = variants
    )

    embed = discord.Embed(title='', color=0xfc4267)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```Skin set to: Purple Skull Trooper```', inline=False)
    embed.set_thumbnail(url="https://benbotfn.tk/cdn/images/CID_030_Athena_Commando_M_Halloween/variant/ClothingColor/Mat1.png")
    await ctx.send(embed=embed)

@discord_bot.command()
async def hatlessrecon(ctx):
    variants = fortnite_bot.party.me.create_variants(parts=2)

    await fortnite_bot.party.me.set_outfit(
        asset='CID_022_Athena_Commando_F',
        variants=variants
    )
    
    embed = discord.Embed(title='', color=0xfc4267)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```Skin set to: Hatless Recon Expert```', inline=False)
    embed.set_thumbnail(url="https://benbotfn.tk/cdn/images/CID_022_Athena_Commando_F/variant/Parts/Stage2.png")
    await ctx.send(embed=embed)

@discord_bot.command()
async def hologram(ctx):
    await fortnite_bot.party.me.set_outfit(
        asset='CID_VIP_Athena_Commando_M_GalileoGondola_SG'
    )
    
    embed = discord.Embed(title='', color=0xfc4267)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```Skin set to: Hologram```', inline=False)
    embed.set_thumbnail(url="https://benbotfn.tk/cdn/images/CID_VIP_Athena_Commando_M_GalileoGondola_SG/icon.png")
    await ctx.send(embed=embed)


@discord_bot.command()
async def new(ctx, content = None):
    newSkins = getNewSkins()
    newEmotes = getNewEmotes()

    previous_skin = fortnite_bot.party.me.outfit

    if content is None:
        await ctx.send(f'There are {len(newSkins) + len(newEmotes)} new skins + emotes')

        for cosmetic in newSkins + newEmotes:
            if cosmetic.startswith('CID_'):
                await fortnite_bot.party.me.set_outfit(asset=cosmetic)
                await asyncio.sleep(4)
            elif cosmetic.startswith('EID_'):
                await fortnite_bot.party.me.clear_emote()
                await fortnite_bot.party.me.set_emote(asset=cosmetic)
                await asyncio.sleep(4)

    elif 'skin' in content.lower():
        await ctx.send(f'There are {len(newSkins)} new skins')

        for skin in newSkins:
            await fortnite_bot.party.me.set_outfit(asset=skin)
            await asyncio.sleep(4)

    elif 'emote' in content.lower():
        await ctx.send(f'There are {len(newEmotes)} new emotes')

        for emote in newEmotes:
            await fortnite_bot.party.me.clear_emote()
            await fortnite_bot.party.me.set_emote(asset=emote)
            await asyncio.sleep(4)

    await fortnite_bot.party.me.clear_emote()
    
    embed = discord.Embed(title='', color=0xfc4267)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```Done!```', inline=False)
    await ctx.send(embed=embed)

    await asyncio.sleep(1.5)

    await fortnite_bot.party.me.set_outfit(asset=previous_skin)

    if (content is not None) and ('skin' or 'emote' not in content.lower()):
        embed = discord.Embed(title='', color=0xfc4267)
        embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```Not a valid option. Try: {T}new (skins, emotes)```', inline=False)
        ctx.send(embed=embed)

@discord_bot.command()
async def ready(ctx):
    await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.READY)
    embed = discord.Embed(title='', color=0xfc4267)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```Ready```', inline=False)
    await ctx.send(embed=embed)

@discord_bot.command()
async def unready(ctx):
    await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    embed = discord.Embed(title='', color=0xfc4267)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```Unready```', inline=False)
    await ctx.send(embed=embed)

@discord_bot.command()
async def sitin(ctx):
    await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.NOT_READY)
    embed = discord.Embed(title='', color=0xfc4267)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```Sitting in```', inline=False)
    await ctx.send(embed=embed)


@discord_bot.command()
async def sitout(ctx):
    await fortnite_bot.party.me.set_ready(fortnitepy.ReadyState.SITTING_OUT)
    embed = discord.Embed(title='', color=0xfc4267)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```Sitting out```', inline=False)
    await ctx.send(embed=embed)

@discord_bot.command()
async def tier(ctx, tier = None):
    if tier is None:
        embed = discord.Embed(title='', color=0xfc4267)
        embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```No tier was given. Try: {T}tier (tier number)```', inline=False)
        await ctx.send(embed=embed)
    else:
        await fortnite_bot.party.me.set_battlepass_info(
            has_purchased=True,
            level=tier
        )
        
        embed = discord.Embed(title='', color=0xfc4267)
        embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```Battle Pass tier set to: {tier}```', inline=False)
        await ctx.send(embed=embed)

@discord_bot.command()
async def backpack(ctx, *, content = None):
    if content is None:
        embed = discord.Embed(title='', color=0xfc4267)
        embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```No backpack was given, try: {T}emote (emote name)```', inline=False)
        await ctx.send(embed=embed)
    elif content.lower() == 'none':
        await fortnite_bot.party.me.clear_backpack()
        await ctx.send('Backpack set to: None')
    elif content.upper().startswith('BID_'):
        await fortnite_bot.party.me.set_backpack(asset=content.upper())
        await ctx.send(f'Backpack set to: {content}')
    else:
        try:
            cosmetic = await BenBotAsync.get_cosmetic(
                lang="en",
                searchLang="en",
                matchMethod="contains",
                name=content,
                backendType="AthenaBackpack"
            )
            await fortnite_bot.party.me.set_backpack(asset=cosmetic.id)
            embed = discord.Embed(title='', color=0xfc4267)
            embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```The Backpack {cosmetic.name} was successfully equipped```', inline=False)
            embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{cosmetic.id}/icon.png")
            await ctx.send(embed=embed)
        except BenBotAsync.exceptions.NotFound:
            embed = discord.Embed(title='', color=0xfc4267)
            embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```The backpack {content} wasn\'t found```', inline=False)
            await ctx.send(embed=embed)

@discord_bot.command()
async def hide(ctx, *, user = None):
    if fortnite_bot.party.me.leader:
        if user != None:
            try:
                if user is None:
                    user = await fortnite_bot.fetch_profile(ctx.message.author.id)
                    member = fortnite_bot.party.members.get(user.id)
                else:
                    user = await fortnite_bot.fetch_profile(user)
                    member = fortnite_bot.party.members.get(user.id)

                raw_squad_assignments = fortnite_bot.party.meta.get_prop('Default:RawSquadAssignments_j')["RawSquadAssignments"]

                for m in raw_squad_assignments:
                    if m['memberId'] == member.id:
                        raw_squad_assignments.remove(m)

                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j',
                    {
                        'RawSquadAssignments': raw_squad_assignments
                    }
                )

                embed = discord.Embed(title='', color=0xfc4267)
                embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'```Hid {member.display_name}```', inline=False)
                await ctx.send(embed=embed)

            except AttributeError:

                embed = discord.Embed(title='', color=0xfc4267)
                embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```I could not find that user.```', inline=False)
                await ctx.send(embed=embed)

            except fortnitepy.HTTPException:

                embed = discord.Embed(title='', color=0x36deff)
                embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```I am not party leader.```', inline=False)
                await ctx.send(embed=embed)
        else:
            try:
                await set_and_update_party_prop(
                    'Default:RawSquadAssignments_j',
                    {
                        'RawSquadAssignments': [
                            {
                                'memberId': fortnite_bot.user.id,
                                'absoluteMemberIdx': 1
                            }
                        ]
                    }
                )
                
                embed = discord.Embed(title='', color=0x36deff)
                embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```Hid everyone in the party.```', inline=False)
                await ctx.send(embed=embed)

            except fortnitepy.HTTPException:

                embed = discord.Embed(title='', color=0x36deff)
                embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```I am not party leader.```', inline=False)
                await ctx.send(embed=embed)

    else:

        embed = discord.Embed(title='', color=0x36deff)
        embed.add_field(name=f'{fortnite_bot.user.display_name}', value='```I need party leader to do this!```', inline=False)
        await ctx.send(embed=embed)



@discord_bot.command()
async def promote(ctx, *, epic_username: Optional[str] = None) -> None:
    if epic_username is None:
        user = await fortnite_bot.fetch_user(ctx.author.display_name)
        member = fortnite_bot.party.get_member(user.id)
    else:
        user = await fortnite_bot.fetch_user(epic_username)
        member = fortnite_bot.party.get_member(user.id)

    if member is None:
        await ctx.send("Failed to find that user, are you sure they're in the party?")
    else:
        try:
            await member.promote()
            embed = discord.Embed(title=f'{fortnite_bot.user.display_name}', url="https://discord.gg/ugUTsaz",description=f"Promoted user: {member.display_name}.", color=0x36deff)
            embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png")
            await ctx.send(embed=embed)
        except fortnitepy.errors.Forbidden:
            await ctx.send(f"Failed topromote {member.display_name}, as I'm not party leader.")
            print(crayons.red("Failed to promote member as I don't have the required permissions."))

@discord_bot.command()
async def help(ctx):
    
    embed = discord.Embed(title=f'{fortnite_bot.user.display_name}', url="https://discord.gg/ugUTsaz",description="Follow me on OrinFN in youtube to support me", color=0x36deff)
    embed.add_field(name=f'{T}pickaxe', value='```Puts on the selected pickaxe.```', inline=False)
		embed.add_field(name=f'{T}yankee', value='```Puts on the yankee skin.```', inline=False)
		embed.add_field(name=f'{T}skin', value='```Puts on the selected skin.```', inline=False)
    embed.add_field(name=f'{T}emote', value='```Does the selected emote.```', inline=False)
    embed.add_field(name=f'{T}skin', value='```Puts on the selected skin.```', inline=False)
    embed.add_field(name=f'{T}goldpeely', value='```Puts on the golden peely skin.```', inline=False)
    embed.add_field(name=f'{T}level', value='```Changes the bot\'s seasonal level.```', inline=False)
		embed.add_field(name=f'{T}new ', value='```Puts on all new skins + emotes during the current update.```', inline=False)
		embed.add_field(name=f'{T}hologram ', value='```Puts on a holographic skin.```', inline=False)
		embed.add_field(name=f'{T}hatlessrecon ', value='```Puts on the Recon Expert variant with no hat.```', inline=False)
		embed.add_field(name=f'{T}purpleskull ', value='```Puts on the pink variant of the Ghoul Trooper.```', inline=False)
    embed.add_field(name=f'{T}pinkghoul', value='```Puts on the pink variant of the Ghoul Trooper.```', inline=False)
		embed.add_field(name=f'{T}hide', value='```Unhides all users in the party```', inline=False)
    embed.add_field(name=f'{T}hide', value='```Hides users in the bot\'s party (Bot has to be party leader)```', inline=False)
    embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png")
    await ctx.send(embed=embed)

@discord_bot.command()
async def info(ctx):
    embed = discord.Embed(title=f'{fortnite_bot.user.display_name}', url="https://discord.gg/ugUTsaz",description="sub to my in orin on youtube to support me", color=0x36deff)
    embed.add_field(name='party info', value=f'There are {fortnite_bot.party.member_count} in The Bots Lobby')
    embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png")
    await ctx.send(embed=embed) 


@discord_bot.command()
async def add(ctx, *, member = None):
    if member is not None:
        try:
            user = await fortnite_bot.fetch_profile(member)
            friends = fortnite_bot.friends

            if user.id in friends:
                embed = discord.Embed(title=f'{fortnite_bot.user.display_name}', url="https://discord.gg/ugUTsaz",description=f"I already have {user.display_name} as a friend", color=0x36deff)
                await ctx.send(embed=embed)
            else:
                await fortnite_bot.add_friend(user.id)
                embed = discord.Embed(title=f'{fortnite_bot.user.display_name}', url="https://discord.gg/ugUTsaz",description=f"Sent a friend request to {user.display_name}", color=0x36deff)
                await ctx.send(embed=embed)
                print('Sent a friend request to: ' f'{user.display_name}')

        except fortnitepy.HTTPException:
            embed = discord.Embed(title=f'{fortnite_bot.user.display_name}', url="https://discord.gg/ugUTsaz",description="There was a problem trying to add this friend.", color=0x36deff)
            await ctx.send(embed=embed)
        except AttributeError:
            embed = discord.Embed(title=f'{fortnite_bot.user.display_name}', url="https://discord.gg/ugUTsaz",description="I can't find a player with that name.", color=0x36deff)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f'{fortnite_bot.user.display_name}', url="https://discord.gg/ugUTsaz",description=f"No user was given. Try: {T}add (user)", color=0x36deff)
        await ctx.send(embed=embed)

@discord_bot.command()
async def season(ctx):
    
    await fortnite_bot.party.me.set_banner(season_level="1")
    await fortnite_bot.party.me.set_outfit(asset="cid_989_athena_commando_m_progressivejonesy")
    embed = discord.Embed(title='', color=0x36deff)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='Level 1')
    embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png")
    await ctx.send(embed=embed)
    await asyncio.sleep(0.25)
    await asyncio.sleep(1.25)

    
    await fortnite_bot.party.me.set_emote(asset="EID_Custodial")
    await asyncio.sleep(5.00)

    
    await fortnite_bot.party.me.set_banner(season_level="15")
    await fortnite_bot.party.me.set_outfit(asset="cid_a_040_athena_commando_f_temple")
    embed = discord.Embed(title='', color=0x36deff)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='Level 15')
    embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png")
    await ctx.send(embed=embed)
    await asyncio.sleep(0.25)
    await asyncio.sleep(1.25)
    
    await fortnite_bot.party.me.set_emote(asset="EID_Temple")
    await asyncio.sleep(5.00)

    
    await fortnite_bot.party.me.set_banner(season_level="29")
    await fortnite_bot.party.me.set_outfit(asset="cid_a_037_athena_commando_f_dinohunter")
    embed = discord.Embed(title='', color=0x36deff)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='Level 29')
    embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png")
    await ctx.send(embed=embed)
    await asyncio.sleep(0.25)
    await asyncio.sleep(1.25)
    
    await fortnite_bot.party.me.set_emote(asset="EID_Suits")
    await asyncio.sleep(5.00)

    
    await fortnite_bot.party.me.set_banner(season_level="50")
    await fortnite_bot.party.me.set_outfit(asset="cid_a_041_athena_commando_m_cubeninja")
    embed = discord.Embed(title='', color=0x36deff)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='Level 50')
    embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png")
    await ctx.send(embed=embed)
    await asyncio.sleep(0.25)
    await asyncio.sleep(1.25)

    await fortnite_bot.party.me.set_emote(asset="EID_CloudFloat")
    await asyncio.sleep(5.00)

    
    await fortnite_bot.party.me.set_banner(season_level="61")
    await fortnite_bot.party.me.set_outfit(asset="cid_a_039_athena_commando_m_chickenwarrior")
    embed = discord.Embed(title='', color=0x36deff)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='Level 61')
    embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png")
    await ctx.send(embed=embed)
    await asyncio.sleep(0.25)
    await asyncio.sleep(1.25)

    await fortnite_bot.party.me.set_emote(asset="EID_BootsAndCats")
    await asyncio.sleep(5.00)

    
    await fortnite_bot.party.me.set_banner(season_level="77")
    await fortnite_bot.party.me.set_outfit(asset="cid_a_036_athena_commando_f_obsidian")
    embed = discord.Embed(title='', color=0x36deff)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='Level 77')
    embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png")
    await ctx.send(embed=embed)
    await asyncio.sleep(0.25)
    await asyncio.sleep(1.25)

    await fortnite_bot.party.me.set_emote(asset="EID_Obsidian")
    await asyncio.sleep(5.00)

    
    await fortnite_bot.party.me.set_banner(season_level="100")
    await fortnite_bot.party.me.set_outfit(asset="cid_a_038_athena_commando_f_towersentinel")
    embed = discord.Embed(title='', color=0x36deff)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value='Level 100')
    embed.set_thumbnail(url=f"https://benbotfn.tk/cdn/images/{fortnite_bot.party.me.outfit}/icon.png")
    await ctx.send(embed=embed)
    await asyncio.sleep(0.25)
    await asyncio.sleep(1.25)
    
    await fortnite_bot.party.me.set_emote(asset="EID_TowerSentinel")
    await asyncio.sleep(5.00)
    
    embed = discord.Embed(title='', color=0x36deff)
    embed.add_field(name=f'{fortnite_bot.user.display_name}', value=f'Thx for Using Primal what is Primal use {T}Primal')
    embed.set_thumbnail(url="https://api.gummyfn.xyz/images/Primal_en.png")
    await ctx.send(embed=embed)

def exc_str(exc):
    if isinstance(exc, Exception):
        exc = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        return exc
    return None

@discord_bot.event
async def on_command_error(ctx, error):
    exc = exc_str(error)
    if ctx.message.channel.type is discord.ChannelType.private:
        print(crayons.red(str(ctx.message.author) + ": " + exc), file=sys.stderr)
    else:
        print(crayons.red(ctx.message.guild.name + " (" + ctx.message.channel.name + "): " + exc), file=sys.stderr)
    embed = discord.Embed(title='', color=0xfc4267)
    embed.add_field(name='Error', value=f'```{error}```', inline=False)
    await ctx.send(embed=embed)
###### web
app=Flask("")

@app.route('/')
def home():
  return f'"UserName": "{fortnite_bot.user.display_name}",\n"UserID": "{fortnite_bot.user.id}",\n"Platform":"{(str((fortnite_bot.platform))[9:]).lower().capitalize()}",\n"Status": "{fortnite_bot.status}",\n"Skin": "{fortnite_bot.party.me.outfit}",\n"Emote": "{fortnite_bot.party.me.emote}"'


@app.route("/discord")
def support():
    return redirect("https://discord.gg/ugUTsaz")



####### web
fortnite_bot.run()

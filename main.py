from keep_alive import keep_alive
import discord
from discord.ext import commands, tasks
import random
import asyncio
import time

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Variables du jeu
xana_level = 1
last_attack_time = 0
cooldown_time = 300  # 5 minutes entre les attaques
xana_exp = 0
exp_to_level_up = 100

# Liste d'attaques
attacks = {
    "banquise": {
        "name": "Gel Soudain",
        "type": "glace",
        "effect": "Gèle une zone entière pendant plusieurs minutes."
    },
    "armée": {
        "name": "Armée Spectrale",
        "type": "invasion",
        "effect": "Invoque une armée virtuelle pour attaquer les héros."
    },
    "électricité": {
        "name": "Surcharge Électrique",
        "type": "électricité",
        "effect": "Fait griller les circuits du Supercalculateur."
    },
    "infiltration": {
        "name": "Infiltration Virale",
        "type": "virus",
        "effect": "Corrompt les tours de Lyoko pour voler des données."
    },
    "fusion": {
        "name": "Fusion des Mondes",
        "type": "chaos",
        "effect": "Fusionne monde réel et virtuel pour semer la confusion."
    }
}

# Liste de quêtes secondaires
quests = [
    "🌐 Trouver une ancienne archive dans Carthage pour ralentir XANA.",
    "🌡️ Sauver un héros coincé dans une tour corrompue.",
    "🛡️ Proteger la tour coeur contre une vague de virus."
]

@bot.event
async def on_ready():
    print(f'Connecté en tant que {bot.user}')

@bot.command()
async def activer(ctx):
    global xana_level
    xana_level = 1
    await ctx.send("⚠️ **XANA est de retour.** Les premières perturbations apparaissent...")

@bot.command()
async def attaque(ctx, type_attaque=None):
    global last_attack_time, xana_exp
    now = time.time()
    if now - last_attack_time < cooldown_time:
        await ctx.send("⏱️ **Attendez avant de lancer une nouvelle attaque !**")
        return

    last_attack_time = now
    xana_exp += 20

    if type_attaque is None:
        choix = random.choice(list(attacks.keys()))
        attaque_choisie = attacks[choix]
    else:
        attaque_choisie = attacks.get(type_attaque)

    if attaque_choisie:
        await ctx.send(f"🔥 **XANA attaque : {attaque_choisie['name']}**")
        await ctx.send(f"**Type** : {attaque_choisie['type'].capitalize()}\n**Effet** : {attaque_choisie['effect']}")
        await progression(ctx)
    else:
        await ctx.send("⚠️ Cette attaque n'existe pas. Utilisez !listes_attacks pour voir les choix.")

async def progression(ctx):
    global xana_exp, xana_level
    if xana_exp >= exp_to_level_up:
        xana_exp = 0
        xana_level += 1
        await ctx.send(f"🎉 **XANA a évolué au niveau {xana_level} !** Ses attaques deviennent plus puissantes...")

        if xana_level == 5:
            await ctx.send("💥 **XANA a atteint son niveau maximum ! L'attaque finale se prépare...**")
            await conclusion(ctx)

@bot.command()
async def conclusion(ctx):
    await ctx.send("""
💥 **ATTAQUE FINALE : Fusion Totale !**
XANA a brisé les frontières entre le monde réel et virtuel.
Tous les héros doivent unir leurs forces pour sauver Lyoko et la Terre !
""")

@bot.command()
async def avancer_histoire(ctx):
    event = random.choice(quests)
    await ctx.send(f"📚 **Quête secondaire** : {event}")

@bot.command()
async def listes_attacks(ctx):
    msg = "**📜 Liste des attaques :**\n"
    for key, atk in attacks.items():
        msg += f"- {key} : {atk['name']} ({atk['type']})\n"
    await ctx.send(msg)

@bot.command()
async def sabotage(ctx):
    sabotages = [
        "❌ Scanner en panne pour 10 minutes !",
        "🔥 Surchauffe du Supercalculateur, risque de crash.",
        "🧬 Tour principale corrompue, accès limité."
    ]
    await ctx.send(random.choice(sabotages))

@bot.command()
async def manipulation(ctx):
    illusions = [
        "🧙 Un héros est manipulé pour attaquer un autre.",
        "👽 Illusion d'une fausse mission urgente pour diviser l'équipe.",
        "🧬 Doubles de héros apparaissent et créent la confusion."
    ]
    await ctx.send(random.choice(illusions))

@bot.command()
async def commandes(ctx):
    await ctx.send("""
**🔧 Liste des commandes disponibles :**
- !activer : Déclenche l'activité de XANA
- !attaque [type] : Lance une attaque de XANA
- !avancer_histoire : Lance une quête secondaire
- !listes_attacks : Affiche les attaques disponibles
- !sabotage : Crée un sabotage
- !manipulation : Crée une illusion
- !conclusion : Lance l'attaque finale
""")

import os
keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))

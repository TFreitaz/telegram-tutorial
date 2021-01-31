import re
import json
import telebot
import requests


TOKEN = ">>INSIRA SEU TOKEN AQUI<<"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(5)
    msg = 'Olá! Eu sou seu Pokedex! Digite o nome de um Pokémon.'
    bot.send_message(message.chat.id, msg)
    
@bot.message_handler(func=lambda message: "pokemon" in message.text.lower())
def retorna_pokemon(message):
    bot.send_chat_action(message.chat.id, 'typing')
    pokemon_id = re.search(r"pokemon\s[\w\-]*", message.text.lower()).group().split()[1]
    r = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
    if r.ok:
        pokemon = json.loads(r.content)
        c = requests.get(pokemon["sprites"]["front_default"])
        with open("pokemon.png", "wb") as f:
            f.write(c.content)
        pokemon_image = open("pokemon.png", "rb")
        bot.send_photo(message.chat.id, photo=pokemon_image)
        info = f"Nome: {pokemon['forms'][0]['name']}   ID: {pokemon['id']}\n"
        info += "Tipo: " + ", ".join(type_["type"]["name"] for type_ in pokemon["types"]) + "\n"
        info += f"Altura: {pokemon['height']*10} cm   Peso: {pokemon['weight']/10} kg\n"
        info += "Status:\n"
        info += f" - HP: {pokemon['stats'][0]['base_stat']}\n"
        info += f" - Ataque: {pokemon['stats'][1]['base_stat']}\n"
        info += f" - Defesa: {pokemon['stats'][2]['base_stat']}\n"
        info += f" - Ataque especial: {pokemon['stats'][3]['base_stat']}\n"
        info += f" - Defesa especial: {pokemon['stats'][4]['base_stat']}\n"
        info += f" - Velocidade: {pokemon['stats'][5]['base_stat']}\n"
        info += "Habilidades:\n"
        for ability in pokemon["abilities"]:
            info += f" - {ability['ability']['name']}\n"
        bot.send_message(message.chat.id, info)
    else:
        msg = f"Não encontrei nada sobre {pokemon_id}"
        bot.send_message(message.chat.id, msg)
        
bot.infinity_polling()

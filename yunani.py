#!/usr/bin/env python

import requests, qrtools
from urllib import urlretrieve
from re import findall
from PIL import Image, ImageOps

MORSE_CODE_DICT = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ', ': '--..--', '.': '.-.-.-',
                   '?': '..--..', '/': '-..-.', '-': '-....-',
                   '(': '-.--.', ')': '-.--.-'}

def decrypt(message):
    message += ' '

    decipher = ''
    citext = ''
    for letter in message:
        if (letter != ' '):
            i = 0
            citext += letter
        else:
            i += 1
            if i == 2:
                decipher += ' '
            else:
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(citext)]
                citext = ''

    return decipher

url = "http://35.187.236.126:8021/index.php"
user_agent = { 'User-agent' : 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' }
session = requests.Session()
decqr = qrtools.QR()

req = session.get(url)
gambar = findall('<div class="data"><img src="(.*?)"></div>', req.text)
res = urlretrieve(gambar[0], "img.png")
	
image = Image.open('img.png')
inverted_image = ImageOps.invert(image)
inverted_image.save('new_img.png')

dec = decqr.decode("new_img.png")
hasil = decrypt(decqr.data)
	
payload = { "solution" : hasil, "submit" : "Submit+Query" }
ex = session.post(url, headers=user_agent, data=payload)

print ex.text
print "[+] Flag : B2P{%s}" %findall('B2P{(.*?)}', ex.text)[0]

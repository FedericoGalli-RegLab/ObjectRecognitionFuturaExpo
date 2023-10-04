import openai
import os
import json

emissions_dictionary = {
    "persona": 0,
    "bicicletta" : 197,
    "automobile": 7000,
    "motocicletta" : 2000 ,
    "aereo di linea": 65000,
    "autobus": 45000,
    "treno": 20000,
    "camion": 11000,
    "barca": 8400,
    "semaforo": 150,
    "idrante": 40,
    "cartello stradale": 50,
    "parcometro": 70,
    "panchina": 400,
    "uccello": 2000,
    "gatto": 6000,
    "cane": 8000,
    "cavallo": 300000,
    "pecora": 15000,
    "mucca": 50000,
    "elefante": 1000000,
    "orso": 50000,
    "zebra": 50000,
    "giraffa": 100000,
    "zaino": 30,
    "ombrello": 15,
    "borsetta": 25,
    "cravatta": 12,
    "borsa": 40,
    "frisbee": 3,
    "sci": 24,
    "snowboard": 24,
    "pallone da calcio": 6,
    "aquilone": 3,
    "mazza da baseball": 20,
    "guanti da baseball": 12,
    "skateboard": 30,
    "tavola da surf": 45,
    "racchetta da tennis": 25,
    "bottiglia": 4,
    "bicchiera da vino": 7,
    "tazza": 6,
    "forchetta": 10,
    "coltello": 10,
    "cucchiaio": 10,
    "ciotola": 5,
    "banana": 0,
    "mela": 0,
    "panino": 1,
    "arancia": 0,
    "broccoli": 0,
    "carota": 0,
    "hot dog": 1,
    "pizza": 2,
    "ciambella": 1,
    "torta": 2,
    "sedia": 40,
    "poltrona": 230,
    "pianta": 0,
    "letto": 250,
    "tavolo da pranzo": 40,
    "bagno": 70,
    "televisore": 112,
    "laptop": 331,
    "mouse": 8,
    "remote": 5,
    "tastiera": 32,
    "smartphone": 63,
    "microonde": 300,
    "forno": 400,
    "toaster": 200,
    "lavandino": 150,
    "frigorifero": 300,
    "libro": 2,
    "orologio": 100,
    "vaso": 50,
    "forbici": 70,
    "peluches": 40,
    "asciugacapelli": 200,
    "spazzolino da denti": 5


}


class GPTService:
    api_key = None

    def __init__(self):
        with open("api_gpt_key.json") as f:
            key = json.load(f)
            self.api_key = key['api_key']

        os.environ['OPENAI_API_KEY'] = self.api_key
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def query_gpt(self, pred_object:str):
        
        content = "Utilizzando questo dizionario: " + str(emissions_dictionary) + ". Rispondi alla domanda: qual è il numro associato a " + pred_object + " ?"

        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                        {"role": "user", 
                        "content": content}
            ],
            temperature=0,
            max_tokens=30,
            frequency_penalty=0,
            presence_penalty=0
        )

        return (response['choices'][0]['message']['content'])
    
test = GPTService()
print()

str_temp = ""
gpt_response = test.query_gpt("vaso")
for i, char in enumerate(gpt_response):
    if (ord(char) >=48 and ord(char) <= 57):
        #if i != len(gpt_response) - 1:
        str_temp += char
print(int(str_temp))

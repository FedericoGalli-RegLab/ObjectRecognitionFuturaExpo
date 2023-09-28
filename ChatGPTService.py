import openai
import os
import json

class GPTService:
    api_key = None

    def __init__(self):
        with open("api_gpt_key.json") as f:
            key = json.load(f)
            self.api_key = key['api_key']

        os.environ['OPENAI_API_KEY'] = self.api_key
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def query_gpt(self, pred_object:str):
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                        {"role": "user", "content": "Rispondi alla frase senza aggiungere ulteriori considerazioni e con un numero: {Quanti Kg di CO2 si emettono in atmosfera per produrre l'oggetto " + pred_object + "?}"}
            ],
            temperature = 0
        )

        return (response['choices'][0]['message']['content'])



test = GPTService()

print(test.query_gpt("Bottiglia in metallo"))
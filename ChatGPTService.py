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
        
        content = "Rispondi alla domanda utilizzando solo ed esclusivamente un singolo numero espresso in chilogrammi. Quanta CO2 si emette per produrre " + pred_object + " ? Non aggiungere altre informazioni oltre il numero e unità di misura"
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                        {"role": "user", 
                        "content": content}
            ],
            temperature=0,
            max_tokens=100,
            frequency_penalty=0,
            presence_penalty=0
        )

        return (response['choices'][0]['message']['content'])
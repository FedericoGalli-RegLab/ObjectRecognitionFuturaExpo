import openai
import os
import json

class GPTService:
    api_key = None
    emission_json = None

    def __init__(self, use_gpt:bool):
        if use_gpt:
            with open("api_gpt_key.json") as f:
                key = json.load(f)
                self.api_key = key['api_key']

            os.environ['OPENAI_API_KEY'] = self.api_key
            openai.api_key = os.getenv("OPENAI_API_KEY")

        with open("emissions_dictionary.json") as f:
            self.emission_json = json.load(f)

    def query_gpt(self, pred_object:str):
        
        content = "Utilizzando questo dizionario: " + str(self.emission_json) + ". Rispondi alla domanda: qual è il numro associato a " + pred_object + " ?"

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
    
    def query_no_gpt(self, pred_object:str):
        return self.emission_json[pred_object]
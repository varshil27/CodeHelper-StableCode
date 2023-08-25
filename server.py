from huggingface_hub import notebook_login
import time
notebook_login()

from transformers import AutoTokenizer
import transformers
import torch
import locale
locale.getpreferredencoding = lambda: "UTF-8"
from flask import Flask, request, jsonify, Response
import pandas as pd
import numpy as np
import pickle
import json
import os
model = "stabilityai/stablecode-completion-alpha-3b-4k"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16,
    device_map="auto",
)


app = Flask(__name__)

@app.route('/instruct', methods=['POST'])
def instructans():
    with app.app_context():  # Create an application context
        data = request.get_json()
        question = data["input"]
        conversation_text = f'''SYSTEM: You are a helpful coding assistant that provides code based on the given query in context.
        ### Instruction: {question}
        ### Response: '''
        sequences = pipeline(
            conversation_text.format(question),
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            max_length=2048,
        )

        x = 0
        code = ""
        for seq in sequences:
            print(x)
            x = x+1
            code = f"Result: {seq['generated_text']}"
            break
        print(code)
        
        return jsonify({"code": code})

@app.route('/complete', methods=['POST'])
def completer():
    with app.app_context():  # Create an application context
        data = request.get_json()
        question = data["question"]
        conversation_text = f'''SYSTEM: You are a helpful coding assistant that completes the code given by user.
        ### Instruction:{question}
        ### Response: '''

        sequences = pipeline(
            conversation_text.format(question),
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            max_length=2048,
        )

        x = 0
        code = "hello"
        for seq in sequences:
            print(x)
            x = x+1
            code = f"Result: {seq['generated_text']}"
            break
        return ({"code": code})

if __name__ == "__main__":
    try:
        app.run(debug=True,port=5000)
    except Exception as e:
        print(f"Error: {e}")
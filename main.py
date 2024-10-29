import streamlit as st
from streamlit_modal import Modal
import requests

HUGGINGFACE_TOKEN = HUGGINGFACE_TOKEN
API_URL = "https://api-inference.huggingface.co/models/RussianNLP/FRED-T5-Summarizer"
headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

def query(text):
    payload = {"inputs": text, "parameters": {"max_length": 300, "min_length": 100, "do_sample": False}}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return {"error": f"Ошибка: {response.status_code}, попробуйте позже."}
    result = response.json()
    if "error" in result and "is currently loading" in result["error"]:
        return {"error": "Модель загружается. Подождите несколько секунд и попробуйте снова."}
    return result

input_text = st.text_input("Введите текст")
output = query(input_text) if input_text else {"error": "Ожидание ввода текста"}

modal = Modal("Суммаризация текста", key="demo-modal")
open_modal = st.button("Открыть модальное окно")

if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        if "error" in output:
            st.write(output["error"])
        else:
            st.write(output[0]['summary_text'])
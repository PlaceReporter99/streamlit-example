import os
os.system("python3 -m pip install tensorflow transformers")
import streamlit as st
from transformers import pipeline
import secrets
um = pipeline("fill-mask", model="bert-base-cased")
unmask = lambda x: um(x)[0]["sequence"]
def fill_masks(text):
    text = text.replace("[MASK]", "[UNK]")
    for _ in range(text.count("[UNK]")):
        text = unmask(text.replace("[UNK]", "[MASK]", 1))
    return text.replace('##', '')
def mask_corrupt(text, num):
    for _ in range(num):
        m = list(text)
        for x in range(len(m)):
            if secrets.randbits(1):
                m[x] = "[MASK]"
        text = fill_masks(text)
    return text
text = st.text_area("Text to mask corrupt", value = "A ble con s j jd tin")
num = st.number_input("Number of iterations", 1)
st.button("Mask Corrupt", on_click = lambda: st.write(mask_corrupt(text, num)))

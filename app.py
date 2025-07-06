from flask import Flask, request, render_template, jsonify
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from langdetect import detect, DetectorFactory
from googletrans import Translator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

app = Flask(__name__)

DetectorFactory.seed = 0
MODEL_NAME = "unitary/toxic-bert"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

TOXIC_LABELS = ["toxicity", "severe_toxicity", "obscene", "identity_attack", "insult", "threat"]
translator = Translator()


def is_probably_tamil_roman(text):
    tamil_roman_keywords = ['enna', 'illa', 'podu', 'poda', 'dei', 'machan', 'madiri', 'romba', 'unga', 'evlo', 'aama']
    return any(word in text.lower() for word in tamil_roman_keywords)


def translate_to_english(text):
    try:
        detected_lang = detect(text)
    except:
        detected_lang = "unknown"

    if is_probably_tamil_roman(text):
        tamil_script = transliterate(text, sanscript.ITRANS, sanscript.TAMIL)
        translated = translator.translate(tamil_script, src='ta', dest='en')
        return translated.text, 'tunglish'

    if detected_lang != "en" and len(text.split()) <= 4 and all(char.isalpha() or char.isspace() for char in text):
        return text, 'en'

    if detected_lang == "en":
        return text, 'en'
    elif detected_lang != "unknown":
        translated = translator.translate(text, src=detected_lang, dest='en')
        return translated.text, detected_lang
    else:
        return text, 'unknown'


def predict_toxicity(text, threshold=0.5):
    eng_text, lang = translate_to_english(text)
    inputs = tokenizer(eng_text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        scores = torch.sigmoid(outputs.logits)[0].tolist()

    result = {
        "original_language": lang,
        "translated_text": eng_text
    }

    is_toxic = False
    for label, score in zip(TOXIC_LABELS, scores):
        result[label] = round(score, 4)
        if score >= threshold:
            is_toxic = True

    result["final_decision"] = "Blocked" if is_toxic else "Allowed"
    return result


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    comment = request.form['comment']
    result = predict_toxicity(comment)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)

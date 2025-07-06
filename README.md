# Toxic Comment Classification and Inhibition System

A real-time, AI-powered comment moderation system designed to detect and prevent the posting of toxic, offensive, and harmful language—especially in romanized and multilingual formats such as Tanglish, Hinglish, and more.

---

## 🧠 Introduction

In today’s hyper-connected world, toxic comments—spread via social media, messaging apps, and forums—have become a silent epidemic. From students to public figures, no one is immune to the damage caused by online abuse and cyberbullying.

Despite increased awareness, gaps in moderation systems continue to allow harmful content to slip through. This project addresses those issues head-on with a machine learning-powered system that works in real time to detect and inhibit toxicity before it reaches the public.

---

## 🚨 Problem Areas

- **Romanized Language Complexity**: Difficulty in detecting mixed-language toxic text due to lack of grammar, slang, and spelling variations.
- **Post-Delete Loophole**: Users can post toxic comments and delete them before moderation catches on.
- **Lack of Real-Time Moderation**: Most tools moderate only after submission.
- **Creative Masking**: Toxicity hidden in intentional spelling changes or emojis (e.g., `l0ser`, `f@ke`).
- **Low-Resource Language Challenges**: Many local languages lack sufficient datasets for effective moderation.

---

## 🛠 Designing the Fix

We developed a machine learning-based solution that:

- Analyzes user comments in **real time** before they are posted.
- Detects toxic content across **multiple languages** and **romanized scripts**.
- **Disables the post button** if toxicity is detected.
- Shows a **friendly warning** with a link to community guidelines.
- Continuously learns and adapts using real-world multilingual data.

---

## ⚙️ Technology Stack

| Module | Technology |
|--------|------------|
| Frontend | React.js |
| Backend | Flask (Python) |
| Preprocessing | Python, Regex |
| Language Detection | FastText, langdetect |
| Transliteration & Translation | Google Translate API, indic-transliteration |
| Toxicity Detection | BERT (`unitary/toxic-bert`) |
| Inhibition Module | Python, Flask |

---

## 🔁 System Workflow

### 🖥 Frontend

1. User types a comment in the text area.
2. On submission attempt, comment is sent to the Flask backend.
3. Backend response includes:
   - Translated comment (if needed)
   - Detected language
   - Toxicity scores
   - Final decision: **Allowed** or **Blocked**
4. Based on result:
   - ✅ **Allowed** → Post button stays active.
   - 🚫 **Blocked** → Post button is disabled and a warning is shown.

---

### 🧪 Backend

The Flask backend exposes a REST API that:

1. Accepts user comment.
2. Performs preprocessing, language detection, and (if needed) transliteration or translation.
3. Uses a fine-tuned BERT model to classify the text.
4. Sends back a structured JSON response:

```json
{
  "original_language": "ta",
  "translated_text": "You are stupid",
  "toxicity": 0.85,
  "insult": 0.91,
  "final_decision": "Blocked"
}

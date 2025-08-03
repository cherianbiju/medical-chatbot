# 🩺 Medical Chatbot with Streamlit, LLaMA 3 & MedQuAD

A smart medical chatbot that uses:
- 💬 Streamlit for UI
- 🤖 LLaMA 3 (via Ollama)
- 🧠 Sentence Transformers
- 🗂️ MedQuAD medical QA dataset
- 😃 Sentiment analysis
- 🌍 Multilingual support

## 🛠 How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```


## 📁 Project Structure

```bash

medical-chatbot/
├── app.py 
├── modules/
│   ├── medqa.py
│   ├── analytics.py
│   └── sentiment.py
├── README.md
├── requirements.txt

```

    app.py: Main chatbot interface

    medqa.py: Handles medical QA logic

    llm.py: LLaMA 3 LLM integration

    sentiment.py: Sentiment classifier

    analytics.py: Logs and visual analytics

    multilingual.py: Translation & support for other languages


    multimodal.py: (if used) handles image/text/audio


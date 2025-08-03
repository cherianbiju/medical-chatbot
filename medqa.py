import os
import torch
import xml.etree.ElementTree as ET
from sentence_transformers import SentenceTransformer, util

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_medquad_data():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "MedQuAD"))

    if not os.path.exists(base_dir):
        raise FileNotFoundError(f"❌ MedQuAD folder not found at: {base_dir}")

    data = []
    questions = []

    print(f"📁 Searching recursively in: {base_dir}")
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".xml"):
                file_path = os.path.join(root, file)
                try:
                    tree = ET.parse(file_path)
                    root_elem = tree.getroot()
                    qapairs = root_elem.findall(".//QAPair")
                    for pair in qapairs:
                        q = pair.findtext("Question")
                        a = pair.findtext("Answer")
                        if q and a:
                            data.append({"question": q.strip(), "answer": a.strip()})
                            questions.append(q.strip())
                except Exception as e:
                    print(f"❌ Failed to parse {file_path}: {e}")

    if not data:
        raise RuntimeError("❌ No valid Q&A pairs found in MedQuAD XML files.")

    embeddings = model.encode(questions, convert_to_tensor=True)
    print(f"✅ Loaded {len(data)} Q&A pairs from MedQuAD")
    return data, embeddings

def get_medical_answer(query, data, embeddings, threshold=0.6):
    query_embedding = model.encode(query, convert_to_tensor=True)
    if query_embedding.dim() == 1:
        query_embedding = query_embedding.unsqueeze(0)

    scores = util.cos_sim(query_embedding, embeddings)[0]
    best_idx = torch.argmax(scores).item()
    best_score = scores[best_idx].item()

    print(f"[Match Score]: {best_score:.3f}")

    if best_score >= threshold:
        return data[best_idx]["answer"]
    return "❌ No relevant answer found in MedQuAD."

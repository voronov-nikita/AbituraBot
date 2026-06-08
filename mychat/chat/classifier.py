# chat/classifier.py

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from .models import Program

model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

programs_cache = []
embeddings_cache = None


def rebuild_index():

    global programs_cache
    global embeddings_cache

    programs_cache = list(Program.objects.all())

    texts = []

    for p in programs_cache:

        text = f"""
        {p.name}
        {p.profession}
        {p.code}
        """

        texts.append(text)

    embeddings_cache = model.encode(texts)


def find_program(user_text):

    if not programs_cache:
        rebuild_index()

    query_embedding = model.encode([user_text])

    similarities = cosine_similarity(
        query_embedding,
        embeddings_cache
    )[0]

    best_idx = similarities.argmax()

    score = similarities[best_idx]

    if score < 0.35:
        return None

    return programs_cache[best_idx]
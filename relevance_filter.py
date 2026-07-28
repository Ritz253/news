"""
Relevance filter — classifies a headline+description as 'liked' or
'disliked' against a specific category's labeled examples, using a
small pretrained embedding model (no LLM, runs fully offline once
the model is downloaded).
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from labeled_examples import CATEGORIES

_model = None
_cache = {}  # category name -> (labeled_vecs, labeled_labels)


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _prepare(category):
    if category in _cache:
        return _cache[category]
    liked, disliked = CATEGORIES[category]
    model = _get_model()
    liked_vecs = model.encode(liked, normalize_embeddings=True)
    disliked_vecs = model.encode(disliked, normalize_embeddings=True)
    labeled_vecs = np.vstack([liked_vecs, disliked_vecs])
    labeled_labels = ["liked"] * len(liked) + ["disliked"] * len(disliked)
    _cache[category] = (labeled_vecs, labeled_labels)
    return _cache[category]


def classify(text, category, k=3):
    labeled_vecs, labeled_labels = _prepare(category)
    model = _get_model()
    vec = model.encode([text], normalize_embeddings=True)[0]
    similarities = labeled_vecs @ vec
    top_k_idx = np.argsort(similarities)[-k:]
    top_labels = [labeled_labels[i] for i in top_k_idx]
    liked_votes = top_labels.count("liked")
    return "liked" if liked_votes > k / 2 else "disliked"

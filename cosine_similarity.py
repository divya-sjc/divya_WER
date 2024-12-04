from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def fun1(sen1, sen2):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    emb = model.encode([sen1, sen2])
    cos_similarity = cosine_similarity([emb[0]], [emb[1]])[0][0]
    return cos_similarity


a = input("Enter 1 numbers")
b = input("Enter 2 numbers")
x = fun1(a, b)
print("cos_similarity=", x)

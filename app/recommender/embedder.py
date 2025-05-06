from sentence_transformers import SentenceTransformer

# 모델 로딩 (서버 시작 시 메모리에 올린다)
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

def embed_text(texts):
    """
    주어진 텍스트 리스트를 임베딩 벡터로 변환
    Args:
        texts (list[str]): 임베딩할 문장 리스트
    Returns:
        np.ndarray: (N, hidden_dim) 형태의 벡터
    """
    embeddings = model.encode(texts, convert_to_numpy=True)
    return embeddings
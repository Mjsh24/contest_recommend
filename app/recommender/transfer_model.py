import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.recommender.embedder import embed_text

class TransferRecommender:
    def __init__(self,contests):
        """
        Args:
            corpus_texts (list[str]): 공모전 설명 텍스트 리스트
        """
        self.contests=contests
        name=[x['name'] for x in self.contests]
        self.corpus_texts =name
        self.corpus_embeddings = embed_text(self.corpus_texts)  # 미리 임베딩
    def recommend(self,keyword, top_k=5):
        """
        Args:
            query_text (str): 사용자 입력 키워드
            top_k (int): 추천할 개수
        Returns:
            list[tuple]: (index, score) 리스트
        """
        query_embedding = embed_text([keyword])  # 입력 키워드 임베딩
        cosine_scores = cosine_similarity(query_embedding, self.corpus_embeddings)[0]
        # 높은 순으로 top_k 개 추출
        top_indices = np.argsort(cosine_scores)[::-1][:top_k]
        top_scores = cosine_scores[top_indices]
        total_list=[]
        for x in top_indices:
            total_list.append(self.contests[x])
        # return list(zip(top_indices, top_scores))
        return total_list
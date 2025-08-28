import logging
import time
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Tuple
import numpy as np
import json
import google.generativeai as genai
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        # Configure the generative AI model
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.llm = genai.GenerativeModel('gemini-1.5-flash')

        # Load a pre-trained sentence-transformer model for embeddings
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    def generate_embedding(self, text: str) -> List[float]:
        """Generates a vector embedding for the given text."""
        start_time = time.time()
        logger.info("Generating embedding...")
        embedding = self.embedding_model.encode(text)
        end_time = time.time()
        logger.info(f"Embedding generation took: {end_time - start_time:.4f} seconds")
        return embedding.tolist()

    def semantic_search(self, query_embedding: List[float], knowledge_bases: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
        """ 
        Performs a semantic search to find the most relevant knowledge base entries.
        """
        start_time = time.time()
        logger.info("Performing semantic search...")
        if not knowledge_bases:
            return []

        query_embedding_np = np.array(query_embedding)
        
        # Extract embeddings from knowledge_bases and convert to numpy array
        kb_embeddings = np.array([json.loads(kb['embedding']) for kb in knowledge_bases])

        # Calculate cosine similarity
        similarities = np.dot(query_embedding_np, kb_embeddings.T)

        # Get indices of top_k most similar entries
        top_k_indices = similarities.argsort()[-top_k:][::-1]

        # Return the top_k relevant knowledge base entries
        relevant_knowledge = [knowledge_bases[i] for i in top_k_indices]
        end_time = time.time()
        logger.info(f"Semantic search took: {end_time - start_time:.4f} seconds")
        return relevant_knowledge

    def generate_response_with_llm(self, query: str, relevant_knowledge: List[Dict[str, Any]]) -> Tuple[str, int]:
        """
        Generates a response using the Gemini LLM and returns the response and token count.
        """
        start_time = time.time()
        logger.info("Generating response with LLM...")
        total_token_count = 0

        if not relevant_knowledge:
            return "I'm sorry, I couldn't find relevant information in the knowledge base for your query.", total_token_count

        context = "\n".join([kb['content'] for kb in relevant_knowledge])

        # Construct a prompt for the LLM
        prompt = f"""
        You are a helpful customer support assistant for a company.
        Based on the following context from the company's knowledge base, please answer the user's question.
        Provide a clear, concise, and direct answer. Do not make up information.
        If the context does not contain the answer, say that you don't have enough information to answer.

        CONTEXT:
        ---
        {context}
        ---

        USER'S QUESTION:
        ---
        {query}
        ---

        ANSWER:
        """

        try:
            response = self.llm.generate_content(prompt)
            total_token_count = response.usage_metadata.total_token_count
            logger.info(f"Gemini API Response: {response.text}")
            logger.info(f"Tokens used: {total_token_count}")
            end_time = time.time()
            logger.info(f"LLM generation took: {end_time - start_time:.4f} seconds")
            return response.text, total_token_count
        except Exception as e:
            logger.error(f"An error occurred during LLM generation: {e}", exc_info=True)
            return "I'm sorry, but I encountered an error while trying to generate a response.", 0

rag_service = RAGService()

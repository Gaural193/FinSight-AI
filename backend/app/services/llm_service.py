import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

class LLMService:
    def __init__(self):
        # We will initialize the model only when answering to ensure the env var is loaded
        pass
        
    def _get_model(self):
        # Using the absolute latest Gemini model available in the API!
        return ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0.2)

    def answer_question(self, query: str, context_chunks: list[dict]) -> str:
        """
        Takes the user's question and the raw chunks from Qdrant,
        builds a prompt, and asks Gemini to answer it.
        """
        # If we didn't find any context in Qdrant, let Gemini know
        if not context_chunks:
            return "I could not find any relevant information in the uploaded documents to answer your question."
            
        # 1. Combine all the raw chunks into one big string
        context_text = "\n\n---\n\n".join([chunk["text"] for chunk in context_chunks])
        
        # 2. Build the Hidden System Prompt
        prompt_template = PromptTemplate.from_template("""
        You are a highly intelligent financial AI assistant. 
        Please answer the user's question based strictly on the provided Context below.
        If the answer cannot be found in the context, politely say that you don't have enough information.
        Do not make up facts or hallucinate numbers.
        
        CONTEXT:
        {context}
        
        USER QUESTION:
        {question}
        """)
        
        # 3. Ask Gemini!
        prompt = prompt_template.format(context=context_text, question=query)
        model = self._get_model()
        
        print("Sending prompt to Gemini LLM...")
        response = model.invoke(prompt)
        
        return response.content

# Create a single instance
llm = LLMService()

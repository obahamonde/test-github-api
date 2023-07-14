from api.services.openai import OpenAIChat
from api.services.pinecone import PineConeClient
from .services import *

llm = OpenAIChat()
memory = PineConeClient()
embeddings = OpenAIVectors()


async def chat_handler(prompt:str,namespace:str):
    messages = [Message(role="user", content=prompt)]
    prompt_embedding = await embeddings.create_embeddings(prompt)
    prompt_vector = prompt_embedding.data[0].embedding
    similarity_search_result = await memory.query(EmbeddingQuery(namespace=namespace,vector=prompt_vector))
    if similarity_search_result.matches:
        similar_messages = [{"text":match.metadata["text"],"score":match.score} for match in similarity_search_result.matches]
        sorted(similar_messages, key=lambda x: x["score"], reverse=True)
        system_prompt = f"""
        Here are some similar messages:
        {similar_messages}
        
        AI Message:
        """
        messages.append(Message(role="system", content=system_prompt))  
    completion_response = await llm.chat(messages)
    message = completion_response.choices[0].message.content 
    message_embedding = await embeddings.create_embeddings(message)
    message_vector = message_embedding.data[0].embedding            
    vectors = [Embedding(values=prompt_vector,metadata={"text":prompt}), Embedding(values=message_vector,metadata={"text":message})] 
    await memory.upsert(EmbeddingUpsert(vectors=vectors,namespace=namespace))
    return message




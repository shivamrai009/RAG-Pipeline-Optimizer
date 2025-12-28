from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Define the output structure we want
class EvaluationScore(BaseModel):
    relevance_score: int = Field(description="Score 1-10 on how relevant the answer is")
    accuracy_score: int = Field(description="Score 1-10 on if the answer matches the context")
    explanation: str = Field(description="Short explanation of the score")

# Initialize Groq LLM
llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0)

def evaluate_response(question, answer, context):
    # Set up the parser
    parser = JsonOutputParser(pydantic_object=EvaluationScore)
    
    prompt_template = """
    You are an expert judge evaluating a RAG system.
    
    User Question: {question}
    System Answer: {answer}
    Retrieved Context: {context}
    
    Evaluate the answer based on:
    1. Relevance: Does it directly answer the question?
    2. Accuracy: Is the answer supported by the provided context?
    
    Return the result in JSON format with keys: 'relevance_score', 'accuracy_score', and 'explanation'.
    
    {format_instructions}
    """
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    
    chain = prompt | llm | parser
    
    try:
        result = chain.invoke({
            "question": question,
            "answer": answer,
            "context": context[:2000], # Truncate context to save tokens/speed
            "format_instructions": parser.get_format_instructions()
        })
        return result
    except Exception as e:
        # Fallback if the LLM output is messy
        return {"relevance_score": 0, "accuracy_score": 0, "explanation": "Evaluation failed."}
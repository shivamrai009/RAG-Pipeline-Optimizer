import shutil
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# --- FIX IS HERE: Use 'backend.' prefix ---
from backend.pipelines import run_experiments
from backend.evaluator import evaluate_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "RAG Optimizer Backend is running"}

@app.post("/optimize")
async def optimize_rag(
    file: UploadFile = File(...), 
    question: str = Form(...)
):
    # Save uploaded file temporarily
    temp_filename = f"temp_{file.filename}"
    
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        print(f"File saved: {temp_filename}. Starting experiments...")

        # Run the 3 RAG Pipelines
        experiment_results = await run_experiments(temp_filename, question)
        
        # Run Evaluation
        final_report = []
        print("Starting evaluation of results...")
        for res in experiment_results:
            score = evaluate_response(question, res["answer"], res["context"])
            res["scores"] = score
            final_report.append(res)
            
        return {"results": final_report}

    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            print(f"Cleaned up {temp_filename}")
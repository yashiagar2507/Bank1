from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
# Configure AI API Key (Backend)
genai.configure(api_key="Enter Your API Key")
app = FastAPI()

# Enable CORS (Allow frontend to communicate with backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all domains (Change this for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers
)

# AI-Based Dispute Classification
def classify_dispute_ai(dispute_reason):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(f"Classify this dispute into one of these types: [Billing Issue, Fraud, Service Issue, Product Issue, Customer Support]. Dispute: {dispute_reason}")
        return response.text.strip()
    except Exception as e:
        if "Resource has been exhausted" in str(e):
            return "Error: AI quota exceeded, please try again later."
        raise HTTPException(status_code=500, detail=f"Error in Classifying Dispute: {str(e)}")

# AI-Based Priority Assignment
def assign_priority_ai(dispute_reason):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(f"Based on urgency and severity, assign a priority (Low, Medium, High) to this dispute: {dispute_reason}")
        return response.text.strip()
    except Exception as e:
        if "Resource has been exhausted" in str(e):
            return "Medium"  # Default fallback priority
        raise HTTPException(status_code=500, detail=f"Error in Assigning Priority: {str(e)}")

# AI-Based Routing Recommendation
def recommend_team_ai(dispute_type):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(f"Based on the dispute type '{dispute_type}', which department should handle it? Options: [Billing, Fraud Investigation, Technical Support, Customer Service, Product Returns]")
        return response.text.strip()
    except Exception as e:
        if "Resource has been exhausted" in str(e):
            return "General Support"  # Fallback team
        raise HTTPException(status_code=500, detail=f"Error in Team Recommendation: {str(e)}")

# AI-Based High-Risk Detection
def is_high_risk_ai(dispute_reason):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(f"Determine if this dispute is high-risk (fraud-related). Respond with only 'True' or 'False'. Dispute: {dispute_reason}")
        return response.text.strip().lower() == "true"
    except Exception as e:
        if "Resource has been exhausted" in str(e):
            return False  # Default fallback
        raise HTTPException(status_code=500, detail=f"Error in High-Risk Detection: {str(e)}")

# API Endpoint to process disputes (with full details)
@app.post("/classify")
def classify_dispute_api(data: dict):
    try:
        customer_id = data.get("customer_id", "")
        dispute_reason = data.get("dispute_reason", "")
        transaction_amount = data.get("transaction_amount", 0)
        past_disputes = data.get("past_disputes", 0)

        dispute_type = classify_dispute_ai(dispute_reason)
        priority = assign_priority_ai(dispute_reason)
        high_risk = is_high_risk_ai(dispute_reason)  # AI-based high-risk detection
        recommended_team = recommend_team_ai(dispute_type)

        return {
            "customer_id": customer_id,
            "dispute_reason": dispute_reason,
            "transaction_amount": transaction_amount,
            "past_disputes": past_disputes,
            "dispute_type": dispute_type,
            "priority_level": priority,
            "high_risk": high_risk,
            "recommended_team": recommended_team
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
# AI Chatbot to handle user input
@app.post("/chatbot")
def chatbot_response(data: dict):
    try:
        user_message = data.get("message", "")

        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(f"""
        You are a customer support assistant. Help classify disputes based on these categories: [Billing Issue, Fraud, Service Issue, Product Issue, Customer Support].
        Also, assign priority [Low, Medium, High] and suggest which department should handle the issue.
        
        User's message: {user_message}
        
        Respond with:
        - Dispute Type: [One of the categories]
        - Priority Level: [Low/Medium/High]
        - Recommended Team: [Billing, Fraud Investigation, Technical Support, Customer Service, Product Returns]
        """)

        return {"response": response.text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in AI response: {str(e)}")

@app.get("/")
def home():
    return {"message": "Chatbot API is running!"}
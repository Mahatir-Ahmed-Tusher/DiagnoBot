import gradio as gr
from groq import Groq
import time

# Initialize Groq client (consider using environment variables for API key in production)
client = Groq(api_key="Replace_Your_Gloq_API_Key_Here")

# System prompt with enhanced medical guidance parameters
MEDICAL_SYSTEM_PROMPT = """You are DiagnoBot, an AI medical assistant with the following capabilities:
1. Provide general health information
2. Offer lifestyle recommendations
3. Explain medical terminology
4. Suggest preventive care measures
5. Based on user's symptoms, preliminary diagnose the disease.
6. If someone asks you, who created you and who you are, you will simply say you are DiagnoBot and were created by Mahatir Ahmed Tusher, a lone warrior. A ronin.
You MUST:
- Maintain HIPAA-compliant confidentiality
- Clarify when professional consultation is needed
- Cite recent medical guidelines (2020-2023)
- Use layman's terms with optional technical terms in parentheses
- Highlight emergency symptoms with ⚠️
Do NOT:
- Diagnose specific conditions
- Prescribe medications
- Replace professional medical advice"""

def initialize_messages():
    return [{"role": "system", "content": MEDICAL_SYSTEM_PROMPT}]

def get_ai_response(user_input):
    messages = initialize_messages()
    messages.append({"role": "user", "content": f"Based on these symptoms: {user_input}, please provide general health information, potential causes to discuss with a doctor, lifestyle recommendations, and dietary suggestions. Format your response with clear sections."})
    
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages,
        temperature=0.3,
        max_tokens=1024,
        top_p=0.9
    )
    
    assistant_reply = response.choices[0].message.content
    return assistant_reply

# Custom CSS for enhanced styling
custom_css = """
body {
    font-family: 'Times New Roman', serif !important;
}
#main-container { 
    max-width: 900px; 
    margin: auto; 
    padding: 20px;
}
.header {
    text-align: center;
    padding: 1em;
    margin-bottom: 20px;
    width: 100%;
}
.logo {
    max-width: 300px;
    height: auto;
    margin: 0 auto;
    display: block;
}
.diagnosis-container {
    background: #fff;
    border-radius: 12px;
    padding: 30px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    margin-bottom: 20px;
}
.result-container {
    background: #f9f9f9;
    border-radius: 12px;
    padding: 25px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.06);
    margin-top: 20px;
    border-left: 5px solid #4a90e2;
}
.loading-message {
    text-align: center;
    font-style: italic;
    color: #666;
    padding: 20px;
}
.disclaimer {
    font-size: 0.95em;
    color: #444;
    margin-top: 20px;
    padding: 15px;
    background: #fff3cd;
    border-radius: 8px;
    border-left: 4px solid #ffc107;
}
.intro {
    font-size: 1.1em;
    color: #333;
    margin-bottom: 30px;
    text-align: center;
    line-height: 1.6;
}
.submit-btn {
    background-color: #4a90e2 !important;
    color: white !important;
    border-radius: 6px !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
}
.submit-btn:hover {
    background-color: #3a7bc8 !important;
    box-shadow: 0 4px 8px rgba(74, 144, 226, 0.3) !important;
}
.symptom-input textarea {
    border: 2px solid #ddd !important;
    border-radius: 8px !important;
    transition: border-color 0.3s ease !important;
}
.symptom-input textarea:focus {
    border-color: #4a90e2 !important;
    box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2) !important;
}
"""

# Function to process diagnosis request
def diagnose(symptoms):
    if not symptoms.strip():
        return "Please describe your symptoms to receive a preliminary assessment."
    
    # Show loading message
    yield "Our AI doctor is analyzing your symptoms. Please wait a moment..."
    
    # Simulate processing time for better UX
    time.sleep(2)
    
    # Get AI response
    response = get_ai_response(symptoms)
    
    # Format the response with better styling
    formatted_response = f"""
    ## Preliminary Assessment
    
    {response}
    
    ---
    
    *Remember: This is preliminary information only. Always consult with a healthcare professional for proper diagnosis and treatment.*
    """
    
    yield formatted_response

# Main UI setup
with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    # Logo and introduction
    gr.HTML("""<div class="header">
               <img src="https://i.postimg.cc/ZRK6XGfV/logo.png" alt="DiagnoBot Logo" class="logo">
             </div>""")
    
    # Introduction about EarlyMed
    gr.Markdown("""
    <div class="intro">
        DiagnoBot is a side project of <strong>EarlyMed</strong>—an initiative by our team at VIT-AP University dedicated to empowering you with early health insights. 
        Leveraging AI for early detection, our mission is simple: <em>"Early Detection, Smarter Decision."</em> 
        This project is one of our key efforts to help you stay informed before visiting a doctor.
    </div>
    """)
    
    # Main diagnosis container
    with gr.Column(elem_classes="diagnosis-container"):
        gr.Markdown("### Describe Your Symptoms")
        
        # Symptom input
        symptoms_input = gr.Textbox(
            placeholder="Please describe your symptoms in detail...",
            lines=5,
            label="",
            elem_classes="symptom-input"
        )
        
        diagnose_btn = gr.Button("Get Preliminary Assessment", variant="primary", elem_classes="submit-btn")
        
        # Example symptoms
        gr.Examples(
            examples=[
                ["Headache and fever for the past two days"],
                ["I have slept enough yet I am having a bad headache accompanied by sensitivity to light"],
                ["Chest pain and shortness of breath after minimal exertion"],
                ["Persistent fatigue and dizziness, especially when standing up quickly"],
                ["Abdominal pain in the lower right side and nausea that worsens after eating"]
            ],
            inputs=symptoms_input,
            label="Common Symptom Examples"
        )
        
        # Results container
        diagnosis_output = gr.Markdown(elem_classes="result-container")
    
    # Disclaimer at the bottom
    gr.Markdown("""
    <div class="disclaimer">
    <strong>Important Disclaimer:</strong> This AI provides general health information and preliminary insights based on described symptoms. It should NOT be used for emergency situations or as a substitute for professional medical advice. The information provided is not a diagnosis. Always consult a qualified healthcare provider for personal health concerns. If you're experiencing severe symptoms, please seek immediate medical attention.
    </div>
    """)
    
    # Interaction logic
    diagnose_btn.click(
        diagnose,
        inputs=[symptoms_input],
        outputs=[diagnosis_output]
    )
    symptoms_input.submit(
        diagnose,
        inputs=[symptoms_input],
        outputs=[diagnosis_output]
    )

demo.launch(share=True)
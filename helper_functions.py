import google.generativeai as genai

def generate_response(prompt, history, model_name, temperature, api_key): 
    genai.configure(api_key=api_key)
    
    # 1. Setup the Gemini Model
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config={
            "temperature": temperature,
            "top_p": 0.95,
        },
        system_instruction="You are Glorious, a professional AI assistant."
    )
    
    # 2. Format history (Gemini uses 'model' instead of 'assistant')
    formatted_history = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        formatted_history.append({"role": role, "parts": [msg["content"]]})
    
    try:
        chat_session = model.start_chat(history=formatted_history)
        # 4. Stream the response
        response = chat_session.send_message(prompt, stream=True)
        
        for chunk in response:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        yield f"Gemini Error: {str(e)}"
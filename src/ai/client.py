# src/ai/client.py
import os

def get_llm_response(system_prompt, user_content):
    """
    Wrapper for OpenAI/Anthropic API.
    Returns a string response.
    
    If no API key is found, returns a simulated response to prevent crashing.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        # Simulated response for demo/testing purposes
        return """
        {
            "maintenance_sga_percent": 0.40,
            "maintenance_rnd_percent": 0.30,
            "reasoning": "Simulated Analysis: Strong Net Revenue Retention (120%+) implies majority of S&M is for expansion. R&D is heavily weighted towards new product modules."
        }
        """
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenAI: {e}"

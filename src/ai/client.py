# src/ai/client.py
import os

def get_llm_response(system_prompt, user_content):
    """
    Wrapper for OpenAI/Anthropic API.
    Returns a string response.
    
    If no API key is found, returns a simulated response to prevent crashing.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("OPENAI_MODEL", "gpt-5.1")
    reasoning_effort = os.getenv("OPENAI_REASONING", "high")
    
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
        
        try:
            request_kwargs = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                "temperature": 0.0
            }

            if reasoning_effort:
                request_kwargs["reasoning"] = {"effort": reasoning_effort}

            response = client.chat.completions.create(**request_kwargs)
            return response.choices[0].message.content
        except Exception as first_error:
            # Fallback to gpt-4o if the requested model is unavailable
            try:
                fallback_model = "gpt-4o"
                response = client.chat.completions.create(
                    model=fallback_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ],
                    temperature=0.0
                )
                return response.choices[0].message.content
            except Exception as second_error:
                return f"Error calling OpenAI: {first_error}; fallback error: {second_error}"
    except Exception as e:
        return f"Error calling OpenAI: {e}"

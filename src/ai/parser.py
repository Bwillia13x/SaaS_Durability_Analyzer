# src/ai/parser.py
import json
import time
from src.ai.prompts import EPV_ANALYSIS_SYSTEM_PROMPT
from src.ai.client import get_llm_response

def analyze_growth_spend(mda_text, financials_json):
    """
    Analyzes MD&A text to estimate Maintenance vs Growth spend.
    Includes retry mechanism and fallback to conservative defaults.
    
    Args:
        mda_text (str): The Management Discussion & Analysis text
        financials_json (dict): Financial data context
        
    Returns:
        dict: Contains 'maintenance_sga_percent', 'maintenance_rnd_percent', 'reasoning'
    """
    
    CONSERVATIVE_DEFAULTS = {
        # Bias toward growth-heavy spend when the AI is unavailable to avoid underestimating EPV
        "maintenance_sga_percent": 0.20,
        "maintenance_rnd_percent": 0.20,
        "reasoning": "⚠️ AI Unavailable - Using Conservative Defaults (80% Growth / 20% Maintenance). Check API keys or connection."
    }
    
    MAX_RETRIES = 3
    user_content = f"Financials: {json.dumps(financials_json)}\n\nMD&A Text:\n{mda_text[:5000]}..." # Truncate for token limits
    
    for attempt in range(MAX_RETRIES):
        try:
            response_text = get_llm_response(
                system_prompt=EPV_ANALYSIS_SYSTEM_PROMPT, 
                user_content=user_content
            )
            
            # Clean potential markdown code blocks
            cleaned_text = response_text.strip()
            if cleaned_text.startswith("```json"):
                cleaned_text = cleaned_text[7:]
            elif cleaned_text.startswith("```"):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith("```"):
                cleaned_text = cleaned_text[:-3]
                
            cleaned_text = cleaned_text.strip()
            
            data = json.loads(cleaned_text)
            
            # Validate keys
            required_keys = ["maintenance_sga_percent", "maintenance_rnd_percent", "reasoning"]
            if not all(key in data for key in required_keys):
                raise ValueError("Missing required keys in LLM response")
                
            # Validate value ranges (0.0 to 1.0)
            if not (0 <= data['maintenance_sga_percent'] <= 1 and 0 <= data['maintenance_rnd_percent'] <= 1):
                raise ValueError("Percentages must be between 0 and 1")

            return data
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(1) # Backoff
            
    # If all retries fail, return defaults
    return CONSERVATIVE_DEFAULTS

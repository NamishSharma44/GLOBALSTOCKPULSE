"""
Script to check Gemini AI configuration and available models
"""
import os
import time
from dotenv import load_dotenv
load_dotenv()

def check_gemini_setup():
    """Check if Gemini AI is properly configured"""
    api_key = os.getenv("GEMINI_API_KEY")
    
    print("=" * 50)
    print("Gemini AI Configuration Check")
    print("=" * 50)
    
    if not api_key:
        print("❌ GEMINI_API_KEY not found in .env file")
        return False
    
    if api_key == "default_key" or api_key == "your_actual_api_key_here":
        print("❌ GEMINI_API_KEY is using a placeholder value")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        from google import genai
        from google.genai import types
        
        print("\n📦 google-genai package imported successfully")
        
        # Initialize client
        client = genai.Client(api_key=api_key)
        print("✅ Gemini client initialized successfully")
        
        # Test models with proper delay
        print("\n🧪 Testing Model Connectivity (with rate limit handling):")
        print("-" * 40)
        
        # Test with the model used in the code - prioritize flash models
        test_models = [
            "gemini-2.5-flash",   # Fast and efficient
            "gemini-2.0-flash",   # Good alternative
            "gemini-2.5-pro",     # Powerful but rate limited
        ]
        
        working_model = None
        for i, model_id in enumerate(test_models):
            if i > 0:
                print("  (waiting 3 seconds to avoid rate limits...)")
                time.sleep(3)
            
            try:
                response = client.models.generate_content(
                    model=model_id,
                    contents="Say 'OK' if you're working.",
                    config=types.GenerateContentConfig(
                        temperature=0.1,
                        max_output_tokens=50
                    )
                )
                if response.text:
                    print(f"  ✅ {model_id}: Working! Response: {response.text.strip()[:30]}")
                    if not working_model:
                        working_model = model_id
            except Exception as e:
                error_msg = str(e)
                if "404" in error_msg or "not found" in error_msg.lower():
                    print(f"  ❌ {model_id}: Model not available")
                elif "429" in error_msg or "resource_exhausted" in error_msg.lower():
                    print(f"  ⚠️ {model_id}: Rate limited (429) - try again later")
                elif "403" in error_msg or "permission" in error_msg.lower():
                    print(f"  ⚠️ {model_id}: Permission denied (may need billing)")
                else:
                    print(f"  ⚠️ {model_id}: {error_msg[:80]}...")
        
        if working_model:
            print(f"\n✅ Recommended model to use: {working_model}")
            return working_model
        else:
            print("\n⚠️ All models rate-limited. The app has fallback analysis mode.")
            print("   Wait a few minutes and try again, or upgrade your API plan.")
            return "fallback"
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Run: pip install google-genai")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    result = check_gemini_setup()
    print("\n" + "=" * 50)
    if result and result != "fallback":
        print(f"✅ Setup complete! Use model: {result}")
    elif result == "fallback":
        print("⚠️ Rate limits active - app will use fallback analysis")
    else:
        print("❌ Configuration needs attention")

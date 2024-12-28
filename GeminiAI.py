# github/twiez
import requests
import json

def ask_gemini(api_key, prompt):
    """Sends a request to the Gemini API."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        json_response = response.json()

        if 'candidates' in json_response and json_response['candidates']:
            first_candidate = json_response['candidates'][0]
            if 'content' in first_candidate and 'parts' in first_candidate['content']:
                parts = first_candidate['content']['parts']
                gemini_text = "".join(part.get('text', '') for part in parts)
                return gemini_text, response.status_code

        print(f"Unexpected JSON response: {json_response}")
        return "No response from Gemini", response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Gemini API: {e}")
        return None, None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None, None

if __name__ == "__main__":
    print("AI Chat -- Made by @twiez")
    
    # Prompt for API key
    api_key = input("Please enter your Gemini API key: ").strip()
    if not api_key:
        print("Error: No API key provided. Exiting.")
        exit(1)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break

        gemini_response, status_code = ask_gemini(api_key, user_input)

        if gemini_response:
            print(f"AI: {gemini_response}")
        else:
            print("Error: Could not get a response from Gemini.")
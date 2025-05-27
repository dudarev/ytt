import requests
from bs4 import BeautifulSoup # Kept for get_video_opengraph_data, can be removed if that func is removed
import re # For regular expressions
import json # For parsing JSON

# URL of the YouTube video
VIDEO_URL = "https://www.youtube.com/watch?v=SS39yl1UiNA&ab_channel=NEXTALive"

# --- Configuration for snippet extraction ---
# Number of characters to extract before the found snippet
CHARS_BEFORE_SNIPPET = 50
# Number of characters to extract after the found snippet
CHARS_AFTER_SNIPPET = 300
# Number of characters from the OG description to use as a search snippet
SNIPPET_LENGTH = 30
# --- End of Configuration ---

# Existing function, can be kept or removed if only new one is needed
def get_video_opengraph_data(url):
    """
    Fetches a YouTube video page and extracts title and description
    from Open Graph meta tags.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        title_tag = soup.find("meta", property="og:title")
        description_tag = soup.find("meta", property="og:description")

        title = title_tag["content"] if title_tag else "No title found"
        description = description_tag["content"] if description_tag else "No description found"

        return title, description, response.text # Return raw response text as well

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None, None, None

def get_youtube_description_from_json(url):
    """
    Fetches a YouTube video page, finds the JSON object associated with the key "description",
    parses it, and returns the value of its "simpleText" sub-key.
    Returns None if any step fails or the key is not found.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        page_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL for JSON description: {e}")
        return None

    key_name = "description"
    sub_key_name = "simpleText"
    
    # Regex to find the key, colon, and ensure an opening brace follows.
    pattern = f'("{key_name}"\s*:\s*)(?={{)'
    
    match_instance = re.search(pattern, page_content) # We only need the first good one for "description"

    if not match_instance:
        print(f"Could not find key '{key_name}' followed by JSON object.")
        return None

    json_start_index = match_instance.end()
    
    brace_level = 0
    in_string = False
    escaped = False
    json_end_index = -1

    for i in range(json_start_index, len(page_content)):
        char = page_content[i]
        if escaped:
            escaped = False
            continue
        if char == '\\':
            escaped = True
            continue
        if char == '"':
            in_string = not in_string
        if not in_string:
            if char == '{':
                brace_level += 1
            elif char == '}':
                brace_level -= 1
        if brace_level == 0 and i >= json_start_index and page_content[json_start_index] == '{':
            json_end_index = i
            break
    
    if json_end_index != -1:
        json_object_string = page_content[json_start_index : json_end_index + 1]
        try:
            parsed_object = json.loads(json_object_string)
            if isinstance(parsed_object, dict):
                value = parsed_object.get(sub_key_name)
                if value is not None:
                    return str(value) # Ensure it's a string
                else:
                    print(f"Sub-key '{sub_key_name}' not found in JSON for '{key_name}'.")
                    return None
            else:
                print(f"Parsed JSON for '{key_name}' is not a dictionary.")
                return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for '{key_name}': {e}")
            return None
    else:
        print(f"Could not find a balanced JSON object for '{key_name}'.")
        return None

if __name__ == "__main__":
    # --- Demonstrate OpenGraph fetching (optional) ---
    og_title, og_description_text, _ = get_video_opengraph_data(VIDEO_URL) # page_content not needed here
    if og_title:
        print(f"OG Title: {og_title}")
    if og_description_text:
        print(f"OG Description: {og_description_text}")
    print("-" * 30) 

    # --- Demonstrate new JSON-based description fetching ---
    print(f"\nFetching description for URL: {VIDEO_URL} using JSON method...")
    json_derived_description = get_youtube_description_from_json(VIDEO_URL)

    if json_derived_description:
        print("\nSuccessfully extracted description via JSON method:")
        print(json_derived_description)
    else:
        print("\nFailed to extract description using JSON method.")

    # --- Previous detailed JSON key exploration (now largely superseded by the function above) ---
    # This part can be removed or kept for more detailed debugging if needed.
    '''
    if page_content: # This page_content would need to be fetched again or passed if we remove the OG call
        print("\n--- Extracting specific values from JSON objects (Detailed Exploration) ---")
        target_json_keys_and_subkeys = {
            "description": "simpleText",
            "attributedDescription": "content",
            "attributedDescriptionBodyText": "content"
        }
        # ... (rest of the detailed exploration loop from previous version) ...
    '''

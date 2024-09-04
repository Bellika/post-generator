import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key= os.getenv("OPENAI_API_KEY")

value_a = "The health benefits of cold brew coffee"
value_b = "Embed examples froms studies"

def generate_headings(value_a):
  prompt = f"""
    Act as an SEO expert speaking fluent English to write only headings (h1, h2, and h3) for an article about "{value_a}",
    adhere to these guidelines: "{value_b}". 
    Return strictly only a JSON object that contains the attribute "title" with a rephrased SEO-optimized article title, 
    and another attribute called "outline" that contains a flat array of exactly 5 items, each item is a top level (h2) 
    headline of an article paragraph. The array will contain string items only. Don't include the word "h2" in any of 
    the items, don't wrap titles in quotation marks, each heading is only the text of the heading.
    """

  response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": prompt},
      ],
    temperature=0.9
  )

  response_content = response.choices[0].message.content.strip()

  try:
    json_response = json.loads(response_content)
  except json.JSONDecodeError:                        # This error handling needs to be fixed, but code still runs atm
    print("Error: The response is not valid JSON.")
    json_response = response_content

  return json_response

def generate_content(headings_json):
    # Check if the JSON structure is valid
    if not isinstance(headings_json, dict):
        print("Error: Invalid JSON format.")
        return

    title = headings_json.get("title", "No title provided")
    outline = headings_json.get("outline", [])

    content_dict = {"title": title, "sections": {}}

    # Generate content for each heading
    for heading in outline:
        prompt = f"""
        Write the content of the section titled \"{heading}\". This section is part of a bigger article called \"{title}\". 
        Don't include the title in your output, only include the paragraphs content. Don't create a summary or conclusion paragraph. 
        Use html tags for sub headings, create one level of sub headings only which is (h3). You can create two or three of these h3 
        subheadings. Don't make the subheadings sound too similar to the original section title provided to you.
        """

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.9
        )

        response_content = response.choices[0].message.content.strip()
        content_dict["sections"][heading] = response_content

    return content_dict

if __name__ == "__main__":
    # Generate headings and store the JSON result in headings_json
    headings_json = generate_headings(value_a)
    print("Headings JSON:", headings_json)
    
    # Generate content based on the headings and store the result in content_json
    content_json = generate_content(headings_json)
    print("Content JSON:", content_json)

import openai
import json
import re

openai.api_key = "api_key"


def parse_trading_signals(text: str) -> str:
    prompt_template = f"""
    Extract structured trading signals from the following text. Ignore unrelated content and only extract valid signals in the format:

    1. Instrument: (e.g., "DMART25MAR3700PE", "BSE25MAR4400PE") Note - append 25APR in every signal.
    2. Buy Instruction: (e.g., "BUY ABV 140" or "BUY ABV 185-86").
    3. Stop Loss (SL): (e.g., "SL 130").
    4. Target Prices: (e.g., "TARGET 145,150,160++" or "Target 145").

    Output a dictionary where each object contains:
    - instrument: (string)
    - trigger_price: (consider first number)
    - stop_loss: (number)
    - target: (consider first number)

    if any one of the above value is not present or not given, return empty dictionary

    Input:
    {text}

    Output dictionary:
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            # model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a trading signal extraction expert."},
                {"role": "user", "content": prompt_template}
            ],
            max_tokens=400,
            temperature=0,
        )

        # Extract text response safely
        if "choices" in response and response["choices"]:
            output_text = response["choices"][0]["message"]["content"].strip()
            # print("Raw API Response:", output_text)  # Debug print

            # Remove code block formatting (```json ... ```)
            output_text = re.sub(r"```json|```", "", output_text).strip()

            # print("Cleaned API Response:", output_text)  # Debug print after cleanup

            # Check if response is empty
            if not output_text:
                return "[]"

            parsed_data = json.loads(output_text)  # Convert JSON string to Python list
            return json.dumps(parsed_data, indent=4)  # Return formatted JSON string
            # print("res: ",res)
            # return convert_instrument(res)

    except json.JSONDecodeError as e:
        print("JSON decoding error:", e)
    except openai.error.OpenAIError as e:
        print("OpenAI API error:", e)
    except Exception as e:
        print("Unexpected error:", e)

    return "[]"  # Return empty JSON array in case of failure

import requests
import pandas as pd

access_token="eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI1S0JaOFEiLCJqdGkiOiI2N2NmMmRlOGFiOGI4ZTA0OTRjODFjZWUiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzQxNjMwOTUyLCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3NDE2NDQwMDB9.xqzw3JU_rC3fYDwPMnVrRXMOXQo_sve484o4leBC00M"

# def get_lot_size(instrument_key):
#     try:
#         # Load the CSV file
#         csv_path = 'NSE.csv'
#         df = pd.read_csv(csv_path)

#         # Ensure required columns exist
#         if 'instrument_key' not in df.columns or 'lot_size' not in df.columns:
#             raise ValueError("CSV file must contain 'instrument_key' and 'lot_size' columns")

#         # Fetch lot_size for the given instrument_key
#         lot_size = df.loc[df['instrument_key'] == instrument_key, 'lot_size']

#         # Return the lot_size if found, else return None
#         return lot_size.iloc[0] if not lot_size.empty else None

#     except Exception as e:
#         print(f"Error: {e}")
#         return None

def fetch_current_price(instrument_key):
    url = f'https://api.upstox.com/v2/market-quote/ltp?instrument_key={instrument_key}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    instruments = data.get('data', {})

    # Iterate through the 'data' to find the matching instrument_token
    for key, value in instruments.items():
        if value.get('instrument_token') == instrument_key:
            return value['last_price']

    raise ValueError(f"Instrument key {instrument_key} not found in data.")

import requests

def place_gtt_order(instrument,trigger_price,target,stop_loss,quentity):
    url = 'https://api.upstox.com/v3/order/gtt/place'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    data = {
        "type": "MULTIPLE",
        "quantity": quentity,
        "product": "D",
        "rules": [
            {
                "strategy": "ENTRY",
                "trigger_type": "ABOVE",
                "trigger_price": trigger_price
            },
            {
                "strategy": "TARGET",
                "trigger_type": "IMMEDIATE",
                "trigger_price": target
            },
            {
                "strategy": "STOPLOSS",
                "trigger_type": "IMMEDIATE",
                "trigger_price": stop_loss
            }
        ],
        "instrument_token": instrument,
        "transaction_type": "BUY"
    }

    try:
        # Send the POST request
        response = requests.post(url, json=data, headers=headers)

        # Print the response status code and body
        print('Response Code:', response.status_code)
        print('Response Body:', response.json())

    except Exception as e:
        # Handle exceptions
        print('Error:', str(e))

def place_order(parsed_signals):
    if parsed_signals['trigger_price']>=fetch_current_price(parsed_signals['instrument']):
        # lot_size=get_lot_size(parsed_signals['instrument'])
        # print("Lot size:",lot_size)
        # print("Instrument key:",parsed_signals['instrument'])
        # print("Trigger price:",parsed_signals['trigger_price'])
        # print("Target:",parsed_signals['target'])
        # print("Stop loss:",parsed_signals['stop_loss'])
        # print(type(parsed_signals['instrument']))
        # print(type(parsed_signals['trigger_price']))
        # print(type(parsed_signals['target']))
        # print(type(parsed_signals['stop_loss']))
        # print(type(lot_size))
        place_gtt_order(parsed_signals['instrument'],parsed_signals['trigger_price'],parsed_signals['target'],parsed_signals['stop_loss'],parsed_signals['lot_size'])
        # print(parsed_signals)
        # print(type(parsed_signals))
    else:
        print(fetch_current_price(parsed_signals['instrument']))
        print("Trigger price is above")

# print(get_lot_size("NSE_FO|50903"))
# print(place_gtt_order("NSE_FO|80918", 200, 210, 195, 125))

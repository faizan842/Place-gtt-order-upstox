# Global dictionaries to store data across function calls
_symbol_to_key = {}
_symbol_to_lot_size = {}
_csv_loaded = False

def load_csv_to_dict(csv_filename):
    global _symbol_to_key, _symbol_to_lot_size, _csv_loaded
    
    # Only load the CSV if it hasn't been loaded already
    if not _csv_loaded:
        import csv
        with open(csv_filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                _symbol_to_key[row['tradingsymbol']] = row['instrument_key']
                if 'lot_size' in row:
                    _symbol_to_lot_size[row['tradingsymbol']] = row['lot_size']
        _csv_loaded = True
    
    return _symbol_to_key, _symbol_to_lot_size

def get_lot_size(symbol):
    return _symbol_to_lot_size.get(symbol, "1")  # Default to 1 if not found

def convert_instrument(text: str) -> tuple:
    # Load the data into dictionaries if not already loaded
    # csv_filename = 'NSE.csv'
    # load_csv_to_dict(csv_filename)
    
    # Look up instrument key and lot size for the symbol
    symbol = text
    instrument_key = _symbol_to_key.get(symbol, "Symbol not found")
    lot_size = get_lot_size(symbol)
    
    # Return both values as a tuple
    return instrument_key, lot_size

load_csv_to_dict('NSE.csv')
print("csv loaded")

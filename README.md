# Place GTT Order

A Python-based trading automation tool for placing Good Till Triggered (GTT) orders using the Upstox API.

## Overview

This project provides functionality to:
- Parse trading signals
- Place GTT orders automatically
- Handle instrument key mapping
- Manage trading operations through a Telegram interface

## Prerequisites

- Python 3.x
- Upstox trading account
- Telegram account (for signal integration)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Place-GTT-order
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
OPENAI_API_KEY=your_openai_api_key
```

## Project Structure

- `main.py` - Main entry point of the application
- `place_order.py` - Core functionality for placing GTT orders
- `parsing_trading_signal.py` - Logic for parsing trading signals
- `instrument_key.py` - Mapping and handling of instrument keys
- `NSE.csv` - Database of NSE instruments
- `requirements.txt` - Project dependencies

## Usage

1. Ensure all environment variables are properly set in the `.env` file
2. Run the main application:
```bash
python main.py
```

## Dependencies

- telethon - For Telegram integration
- nest_asyncio - For handling async operations
- openai - For AI-powered features
- python-dotenv - For environment variable management

## Security

- Never commit your `.env` file or expose your API keys
- Keep your trading credentials secure
- Regularly update your dependencies

## Contributing

Feel free to submit issues and enhancement requests.

## License

[Add your license information here] 
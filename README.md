# File Converter Telegram Bot

This Telegram bot allows users to convert files to various formats including ZIP, IMG, MP4, MP3, and GIF.

## Features

- Convert files to ZIP, IMG, MP4, MP3, and GIF formats
- Web interface with QR code for easy bot access
- Deployable on Render

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/file-converter-bot.git
   cd file-converter-bot
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a new bot on Telegram by talking to [@BotFather](https://t.me/BotFather) and get your bot token.

4. Set your bot token as an environment variable:
   ```
   export TELEGRAM_BOT_TOKEN=your_bot_token_here
   ```

5. Run the bot:
   ```
   python bot.py
   ```

## Usage

1. Start a chat with your bot on Telegram.
2. Send a file to the bot.
3. Choose the format you want to convert the file to.
4. The bot will process the file and send back the converted version.

## Deployment on Render

1. Fork this repository to your GitHub account.
2. Create a new Web Service on Render.
3. Connect your GitHub account and select the forked repository.
4. Set the following:
   - Environment: Docker
   - Build Command: (leave empty)
   - Start Command: (leave empty)
5. Add the environment variable `TELEGRAM_BOT_TOKEN` with your bot token.
6. Deploy the bot.

## Web Interface

The bot comes with a simple web interface that displays a QR code for easy access to the bot. After deployment, you can access this interface at your Render app's URL.

## License

This project is licensed under the MIT License.

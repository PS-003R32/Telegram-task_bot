# Telegram-task_bot
How to create your own TELEGRAM bot.
This repo will guide you to create a task bot that has commands that can be used for your daily requirements. ;)

This is a complete guide to create a Telegram bot with the given functionalities using Python and the pyTelegramBotAPI library, as it’s widely used, beginner-friendly, and well-suited for integrating with web searches, notifications, and QR code generation. The bot will have distinct commands for each function:

Search the web for a query (/search).
Set a daily goal with notifications at the start and near the deadline (/setgoal).
Add a user by phone number (/adduser).
Create a QR code for a provided link (/qrcode).
Fetch group data (members and roles) (/groupdata).
Make a user a member or admin in a group (/promote).


Step 1: create a virtual environment using python3 in bash.
    >python3 -m venv folderName
    >cd folderName
    > source bin/activate
Step 2: install dependencies.
    >pip install pyTelegramBotAPI requests python-telegram-bot python-qrcode pillow

    "API Key for Web Search: Use a search API like Google Custom Search JSON API (requires an API key and Custom Search Engine ID) or a free alternative like SerpAPI. For this guide, I’ll use SerpAPI (requires an API key). Sign up at serpapi.com and get your API key."

Open Telegram and follow the folloeing steps:-
    Step 1: Create the Bot with BotFather
        Open Telegram and Find BotFather:
        Search for @BotFather (official bot with a blue checkmark) and click Start.
        Create a New Bot:
        Send /newbot.
        Provide a name (e.g., TaskMasterBot) and a username (e.g., @TaskMasterBot, must end with bot or _bot).
        BotFather will return a token (e.g., 21137876:......................0K5PALDssw).
        Save the token securely.
    Step 2: Set Bot Commands:
        Send /setcommands to BotFather and provide the following list to define commands:
        
        search - Search the web for a query
        setgoal - Set a daily goal with notifications
        adduser - Add a user by phone number
        qrcode - Generate a QR code for a link
        groupdata - Fetch group members and roles
        promote - Promote a user to member or admin
        (send this to the chat in this format only.)
        
Enable Group Features (for /groupdata and /promote):
Send /setjoingroups to BotFather and enable group joining.
Add the bot to a group where it has admin privileges (required for /promote and /groupdata).


_Create the Bot Script_
find the bot script in the repo. The script uses pyTelegramBotAPI for Telegram interaction, requests for web searches, qrcode for QR code generation, and Telegram API methods for group management.

*FINAL STEPS:*

Set Up Environment Variables
To secure the bot token and SerpAPI key, store them in environment variables:
Set environment variables in your terminal:
    >export BOT_TOKEN='YOUR_BOT_TOKEN'
    >export SERPAPI_KEY='YOUR_SERPAPI_KEY'

To make them persistent, add to ~/.zshrc:
    >echo 'export BOT_TOKEN="YOUR_BOT_TOKEN"' >> ~/.zshrc
    >echo 'export SERPAPI_KEY="YOUR_SERPAPI_KEY"' >> ~/.zshrc
    >source ~/.zshrc

Make the Script Executable from Anywhere
Since you asked about making scripts executable from anywhere, follow these steps:
Move the Script to ~/bin:
    >mkdir -p ~/bin
    >mv bot.py ~/bin/
    >chmod +x ~/bin/bot.py

Add ~/bin to PATH (if not already done):
    >echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc
    >source ~/.zshrc


Run the Bot from the terminal and keep it runninn:
    >bot.py

This only works if the bot.py script is running on your machine. You can host this in cloud.

ENJOY...........;)

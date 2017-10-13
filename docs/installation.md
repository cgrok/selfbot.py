## Python

This is a self-bot written in the python programming language. So if you don't already have python correctly installed, you must install it. When installing python, you *must* tick `add to path` so that you can use it in your terminal. Make sure you go with the recommended options as it installs `pip` for you. 


## Installing the self-bot

Now that you have python installed, you are good to go. Follow the steps below for a successful installation.

1. Download the selfbot from the [github page](https://github.com/verixx/selfbot/archive/master.zip).
2. Extract the zip file to the desktop or wherever you want.
3. Open your terminal or cmd.
4. Navigate to the bot folder. i.e `cd desktop/selfbot-master`
5. Install all the requirements: `pip install -r requirements.txt`
6. Run the bot with `python selfbot.py` or on mac `python3 selfbot.py`
7. Enter your token and prefix in the wizard.

If you need to edit your token or prefix, navigate into the data folder and open `config.json` and change the values.

```json
{
    "TOKEN": "your_token_here",
    "PREFIX": "r."
}
```
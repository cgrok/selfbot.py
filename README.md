<div align="center">
        <p> <img src="https://i.imgur.com/lBSqWgt.png"/> </p>
        <p><i><b>Moderation, fun, utility and much more!</b></i></p>
	<p> 
		<a href="https://discord.gg/pmQSbAd"><img src="https://discordapp.com/api/guilds/345787308282478592/widget.png?style=banner2" alt="" /></a>
	</p>
	<p>	<img src="https://img.shields.io/badge/build-passing-brightgreen.svg" alt="passing" /></a>
		<img src="https://img.shields.io/badge/python-3.5-brightgreen.svg" alt="python 3.5" /></a>
		<a href="https://github.com/Rapptz/discord.py"><img src="https://img.shields.io/badge/discord-py-orange.svg" alt="discord.py" /></a>
	</p>
</div> 


## [Installation via Heroku](https://github.com/verixx/selfbot/wiki/heroku)
There are two ways of using the bot, one way is to download it and install it on your computer, the other is to host for free 24/7 on a service called **Heroku**. No download is required, everything is done online. Read the installation guide [here](https://github.com/verixx/selfbot/wiki/Heroku). Its possible to install the selfbot using your phone and it has been done before. If you have any questions, join the support discord server and we will be happy to help.

## [Normal Installation](https://github.com/verixx/selfbot/wiki)
You need the following to run the bot: This can be done by `pip install -r /path/to/requirements.txt`
```py
discord.py
requests
PythonGists
bs4
lxml
Pillow
mtranslate
```

Open a terminal in the directory of the bots location and type
```
$ python3 selfbot.py
```
On first start the launcher will run and you will need to input data. After that the bot will launch without setup neccessary.

If you need to edit your token or prefix, navigate into the data folder and open `config.json` and change the values.
```json
{
    "FIRST": false,
    "BOT": {
        "PREFIX": "s.",
        "TOKEN": "token_here"
    }
}
```

## Features

* Moderation commands
* Global emoji commands
* Complex embed commands
* Custom formatted paginated help
* Miscellaneous commands
* Easy to make your own commands

If you want to request features, [create an issue](https://github.com/verixx/selfbot/issues) on this repo.


This is a `stateless selfbot` (Saves no data) *This means that you can [host it on heroku](https://github.com/verixx/selfbot/wiki/Heroku) 24/7 for free*  

These are the [default commands](https://github.com/verixx/selfbot/wiki/Default-Commands)
## Contributors

> [@kwugfighter](https://github.com/kwugfighter)

> [@FloatCobra](https://github.com/FloatCobra)

> [@umbresp](https://github.com/umbresp)

> [@fourjr](https://github.com/fourjr)

## Acknowledgements

> Eval command by [Rapptz](https://github.com/Rapptz) from R.Danny

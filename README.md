<div align="center">
        <p> <img src="https://i.imgur.com/lBSqWgt.png"/> </p>
        <p><i><b>Moderation, fun, utility and much more! (Rewrite)</b></i></p>
	<p> 
		<a href="https://discord.gg/pmQSbAd"><img src="https://discordapp.com/api/guilds/345787308282478592/widget.png?style=banner2" alt="" /></a>
	</p>
	<p>	<img src="https://img.shields.io/badge/build-passing-brightgreen.svg" alt="passing" /></a>
		<img src="https://img.shields.io/badge/python-3.6-brightgreen.svg" alt="python 3.6" /></a>
		<a href="https://github.com/Rapptz/discord.py"><img src="https://img.shields.io/badge/discord-py-orange.svg" alt="discord.py" /></a>
	</p>
</div> 

## [Welcome](http://selfbot-py.tk) 
This branch of the selfbot runs on discord.py rewrite, the next major version of the library. The selfbot has been completely rewritten with better code and structure. Head on to the website for documentation and easy to understand install guides: http://selfbot-py.tk

## [Installation via Heroku](https://github.com/verixx/selfbot/wiki/heroku)
There are two ways of using the bot, one way is to download it and install it on your computer, the other is to host for free 24/7 on a service called **Heroku**. No download is required, everything is done online. Read the installation guide [here](https://github.com/verixx/selfbot/wiki/Heroku) or watch the video tutorial [here](https://youtu.be/1c0fJ8KcHcM). Its possible to install the selfbot using your phone and it has been done before. If you have any questions, join the support discord server and we will be happy to help.

## [Normal Installation](https://github.com/verixx/selfbot.py/wiki/Hosting-on-your-own-PC)
You need the following to run the bot: (currently) 
```py
git+https://github.com/Rapptz/discord.py@rewrite
lxml
mtranslate
colorthief
sympy
psutil
emoji
```
Do `pip install -r path/to/requirements.txt` to install the requirements.
## Setup

Open a terminal in the directory of the bots location and type
```
$ python3 selfbot.py
```
On first start the launcher will run and you will need to input data. After that the bot will launch without setup neccessary.

If you need to edit your token or prefix, navigate into the data folder and open `config.json` and change the values.
```json
{
    "TOKEN": "your_token_here",
    "PREFIX": "r."
}
```

## Features

* Moderation commands
* Global emoji commands
* Complex embed commands
* Miscellaneous commands
* Easy to make your own commands
* Community Cogs *(coming soon, join [our discord](https://discord.gg/pmQSbAd) for updates)*

If you want to request features, [create an issue](https://github.com/verixx/selfbot/issues) on this repo.


This is a `stateless selfbot` (Saves no data) *This means that you can [host it on heroku](https://github.com/verixx/selfbot/wiki/Heroku) 24/7 for free*  

## Community Cogs

**This is coming soon, so it's not working at the moment.**

To submit a cog, submit a [pull request](https://github.com/verixx/selfbot.py/pulls) into the [/cogs/community](https://github.com/verixx/selfbot.py/tree/rewrite/cogs/community) folder.        
To download a cog, add the Cog Name in `data/community_cogs.txt`. Invalid cog names will return an error in your console.

Currently available cogs:-    
* cog1
* cog2

Note: You **do not** have to add default cogs into `data/community_cogs.txt`.

## Acknowledgements

> Eval and google commands by [Rapptz](https://github.com/Rapptz) from R.Danny

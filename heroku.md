# Using with Heroku

If you choose to install the bot using heroku, you dont need to download anything. In fact you can set it all up on a phone. (Provided you have your token). Watch the video tutorial below for an easy installation guide.

<div>
<iframe src="https://www.youtube.com/embed/1c0fJ8KcHcM" 
        width="640" height="360"
        frameborder="0"
        allowfullscreen="allowfullscreen"
        mozallowfullscreen="mozallowfullscreen" 
        msallowfullscreen="msallowfullscreen" 
        oallowfullscreen="oallowfullscreen" 
        webkitallowfullscreen="webkitallowfullscreen"> </iframe> 
</div>

### GitHub Account

For this to work you will need to make a Github account (If you don't have one already). After you have made your Github account go to this repository and fork it.

### Heroku Account

After making a Github account, you need to make a Heroku account. Make one at https://heroku.com/ and then follow the steps below: 

### Setting it up

1. Create a python application on Heroku (this is pretty straightforward)
2. Go to your application settings and find the `config vars` section. 
3. Create a config variable, name the key to be `TOKEN` and the value to be your discord token
4. Find the `deploy` section on your applications dashboard.
5. In deploy method, click on the GitHub option and link your Github account to Heroku.
6. Now select the forked repository and click `deploy application`
7. Go to the `resources` tab and turn on the worker.
8. If you want, you can go over and check the application logs to see if everything is running smoothly.

Now you should be done. Go over to discord and try it out!

If you do use the selfbot, a star on this repository is appreciated ;)

Join the support server [here](https://discord.gg/pmQSbAd) for fun and a special role!

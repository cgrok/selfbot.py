# Reference

Here you can find information relevent to the selfbot.


# Retrieving Your Token

### PC
1. Open Discord, the Web App works too
2. Press Ctrl+Shift+i
3. Click "Application" tab (Click the 2 arrows on the right if you can't find it)
4. Expand Storage > Local Storage > <https://discordapp.com/>
5. Find "token" under "key"
6. Copy the text in quotes on the same row
7. Remove the quotes if using [[Heroku]]

### Android
1. Download [this](https://play.google.com/store/apps/details?id=ai.agusibrahim.xhrlog) from the Google Play Store
2. Press the `>` icon at the top right
3. Type in `discordapp.com/login`
4. Log in
5. Press the 3 dots at the top right and click `XHR Logs`
6. You should see this
```elm
REQ:https://discordapp.com/api/v6/auth/mfa/totp
ARG:{"0":{"isTrusted":true}}
REAP:{"token":"your token here"} 
```
7. Copy your token
8. Remove the quotes if using [[Heroku]]

### iOS
We have not found a working solution yet. If you found one, inform us in our [Discord Server](https://discord.gg/pmQSbAd)! 

# Possible Errors

!> If you see this: `[SSL: CERTIFICATE_VERIFY_FAILED]` and you are using Python 3.6, navigate to your `Applications/Python 3.6/` folder and double click the `Install Certificates.command` to fix this.
Happy coding!

!> Improper Token passed? This means that the token you have inputted is invalid. Check again if your token is correct and edit your config accordingly.

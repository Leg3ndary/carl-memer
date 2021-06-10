# Carl-bot Tag - Dank Memer Copy
Github for the Carl Memer Tag, I have no idea what to call this.

This project is not supported by either Carl-bot or Dank Memer, this is simply a fun project to teach me more about APIs and python in general.

This tag will be free to import with Carl-bot from discord: `ADD IMPORT LINK AND SHIT HERE LATER`

### API Endpoints
In essence this is creating an API so I might as well tell you its endpoints not that it would do much

**API Endpoints** 
```
https://carlmemer.tagscript1.repl.co/
```
Shows wether the api endpoint is alive and working...
This is the base URL    

**Actual Endpoints**
```
/beg/userid/unix
```
Beg command, classic

```
/search/userid/unix
```
Search command, sadly we cannot await options as we only really have one oppurtunity or request if you will :p

```
/pickup/userid/unix
```
Pickup command, just another way to earn money

```
/shop/unix/page_number
```
Shows shop with given page_number

```
/info/userid/unix/object
```
View an item, another player, you're profile... Up to you

```
/inv/userid/unix/page_number
```
View your inventory which also includes a page_number

```
/buy/userid/unix/item/amount
```
Buy something, simple.

```
/sell/userid/unix/item/amount
```
Sell something, extremely difficult.

```
/use/userid/unix/item
```
Use an item... What else

```
/hourly/userid/unix
```
Hourly command to get your hourly reward since I need more ways to get money

```
/daily/userid/unix
```
Daily Command to get your daily reward since we still need more ways to get money

```
/leaderboards/unix/type
```
Leaderboards for the following types, Wallet Bal, Bank Bal, Bank Space

Error/Testing Endpoints
```
/cnf/unix/command
```
Command not found, just an error image saying the command wasn't found

Read stuff under here if you want, I won't explain any of it really further

### Setup/Installation
This is not meant for you to setup nor install, it will be complicated and tedious, however for those of you who want to try and setup this I will not stop you. Please don't ask for help though as I thoroughly think you shouldn't try it.

**Steps:** 
1. You need a web server, I just used repl.it for simplicity
2. Install of the imports you don't have already, if you do use repl.it keep the os.system messages as repl.it will delete your packages
3. You will need a pymongo account, create one.
    - Create a organization
    - Create a project
    - Create a cluster
    - Allow access from anywhere in database access
    - Connect to your cluster and select the application method
    - Somewhere during this process you will be asked to create a Database user, do this and keep the password and username
    - Change to python and select the version of python you will be using, would recommend you use latest.
    - Repl has a new env system which I hate but I can't do anything about it, add the keys and call them in the os.environ variables, make sure to replace the connection string with the correct one
4. Now you need to find the coroutine that should keep the bot alive
    - Run the project... It should say `API ALIVE` or something of the sort
    - A new window should've opened up select the link it's given you, paste that into the url that we open in the coroutine
5. Finally head over to [UptimeRobot](https://uptimerobot.com/)
    - Create an account
    - Create a new monitor, set interval to 5 minutes (Lowest possible)
    - Select the http option and paste the link you put in the urlopen, create the monitor
    - This will ping our server every 5 min trying to keep it alive, you can also configure it to send you emails when it doesn't get a header with 200 in it (200 means its fine)
6. You now have to create the image requesting part
    - For discord it would be best to use an embed and use the image field, alter the endpoint passed to the embed as needed
    - For other apps I'm not sure how you would integrate it as there's probably much better options anyways, not sure how to help
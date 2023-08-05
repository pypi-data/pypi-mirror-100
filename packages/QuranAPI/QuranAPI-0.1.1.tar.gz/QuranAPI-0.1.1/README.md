* Updating to the newest version of QuranAPI is reccomended always

# QuranAPI

## New Release Notes
  - Prayer times are now available as a function (v0.1.1)
  - Fixed bugs and errors (v0.1.1)
  - Random verse function available (v0.0.9)
  
## Details
QuranAPI was built so you can get single verses into your discord server through your discord bot!
For any suggestions of concerns please email nooby xviii: xviii2008@gmail.com

## Features
  * Modern module to get single verses for your discord bot
  * Built with ```asyncio``` and ```aiohttp```
  * Trusted backend Quran API

## How It Works (Verse Function)
  * Install the module: ```pip install QuranAPI```
  * Import the module to your code: ```import QuranAPI```
  * Write this function in this format for an event or command: ```await QuranAPI.get_verse({verse ID}, "{language}", {channel}) 
    - Explanation for the function:
        - {verse ID} stands for the Ayah you want
          - For Example: {verse ID} can be 1:1, which will give us the first Ayah in the first Surah. Remember it is formatted Surah:Ayah
        - "{language}" stands for the Language you want the Ayah's to be displayed
          - For Example: "{language}" can be "arabic" or "english"
            - Note that only english and arabic are available as of version 0.0.7
        - {channel} stands for the channel in your server or a server your bots in where you want the verse to be sent
          - For Example: {channel} can be ctx.channel if you are using the module for an quran command and can be message.channel when you are using the module for an on_message event
    - Examples of the function:
      - Quran Command (English Translation):
       ```python
      @client.command()
      async def quran(ctx, ayah): #ayah will be the ayah your bot gets from a surah
        await QuranAPI.get_verse(ayah, "english", ctx.channel)
        ```
        - The Command Usage Will Be:
          ```~quran 1:2```
            * Using this command, your bot will give you the translation for the second ayah from the first surah in english
            
      - Quran Command (Arabic Translation):
       ```python
      @client.command()
      async def quran(ctx, ayah): #ayah will be the ayah your bot gets from a surah
        await QuranAPI.get_verse(ayah, "arabic", ctx.channel)
        ```
        - The Command Usage Will Be:
          ```~quran 1:3```
            * Using this command, your bot will give you the translation for the third ayah from the first surah in arabic
            
## How It Works (Random Verse Function) 
If you want a random verse to be sent, do everything the same as above, but instead use this function: ```await QuranAPI.random_verse("{language}", channel)```
  - Examples:
    - Random Verse Function (english):
      ```await QuranAPI.random_verse("english", ctx.channel)```
    - Random Verse Function (arabic):
      ```await QuranAPI.random_verse("arabic", ctx.channel)```

## How It Works (Prayer Times)
  * Install QuranAPI: ```pip install QuranAPI```
  * Import QuranAPI to your code: ```import QuranAPI```
  * Write the function in this format: ```await QuranAPI.prayer_times({location}, {channel})
  - Explanation of the function:
    - The {location} part is the location you want prayer times for
      - For Example: {location} can be Dubai UAE 
    - The {channel} part is the same as the other functions, it is to let the module know where to send the message
      - For Example: {channel} can be ctx.channel (if you are using a command) or message.channel (if using the function on an event) or can be simply a channel ID that you want all your bots messages to be sent
  - Examples of the function:
    ```python
    @client.command()
    async def prayertimes(ctx, location): #location is the place your bot will get the prayer times for
      await QuranAPI.prayer_times(location, ctx.channel)
    ```
      - The Command Usage Will Be:
        ```~prayertimes {location}```
          For Example: ```~prayertimes Dubai UAE```
            * Your bot will then send the prayertimes for all 5 prayers for that day to the specified channel you have written in the function
## Extra Notes
  * Versions 0.0.2 - 0.1.0 were deleted for bugs and faulty code
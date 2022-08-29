# HorrorBot for Instagram 🧟‍♀️

**🚨 HorrorBot was retired in August 2022. Thank you everybody! 🚨**

An Instagram bot that utilizes DeepAI's API.

If you'd like to learn more about how this bot works, I highly recommend you check out [my blog post](https://ckyy.medium.com/creating-horrorbot-46072dd5de2e) about it, which goes into this a lot deeper.

To give you a brief summary of what this bot does:
> Once a month, this bot will pull all of the comments from my most recent Instagram post and select any comments starting with the keyword imagine. It will then randomly choose one of the comments and run that comment as an image search query with SerpAPI. After grabbing the output URL, it runs it through the DeepAI Deep Dream API for 5 iterations to give it a more ‘wild look’. Then the resulting image is posted, describing the input the AI was given and crediting the user who originally supplied it.

Note: This script must be set to run on a cronjob

Here are the resources that you'll need to get the APIs from:<br>
| API Sources   |      
| ------------- |
| [Apify](https://apify.com)         |
| [SerpApi](https://serpapi.com)     |
| [DeepAI](https://deepai.org)           |
| [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/getting-started) |

*Be sure to run `pip install -r requirements.txt` before anything else

## To-Do:
### Implement saveBot() Function
If you take a look at the image/caption generation in the script, you’ll notice error checking for Aspect Ratios. Meta doesn’t allow certain aspect ratios to be posted directly, resulting in the script erroring out. I want to implement a saveBot() function where it automatically resizes the aspect ratio to 1:1 so the bot will be able to post the image regardless.

### Fix Comment Limit
Apify's Instagram API can only pull the safe amount of 24 comments while not being authenticated. As of right now, I’m not worried about the 24 comment limit being hit, but the main problem is that regardless of whether or not someone types the keyword, that still counts as 1 of the 24 comments. The comment checking is only done AFTER all of them have been pulled. This isn't something I'm looking to fix right away. As of right now I don't want to risk having any of my API rights stripped away or blocked. So unless this is NEEDED, this won't be changed.

### Improve Logging
As of now, logs that are generated each run have to be manually moved to their respective folder. I kept it in this state during its ‘beta’ to make sure things have been going well, but now that I’ve fixed most issues and it seems to be stable, this is very high on my list.

### Improve Error Logging
While the majority of errors are handled well and give meaningful output, the rare errors (such as invalid aspect ratios from Meta) aren't handled correctly and causes a nondescript error to be pushed out.

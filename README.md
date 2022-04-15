# HorrorBot for Instagram 🧟‍♀️
An Instagram bot that utilizes DeepAI's API.

If you'd like to learn more about how this bot works, I highly recommend you check out [my blog post](https://ckyy.medium.com/creating-horrorbot-46072dd5de2e) about it, which goes into this a lot deeper.

To give you a brief summary of what this bot does:
> Once a week, this bot will pull all of the comments from my most recent Instagram post and select any comments starting with the keyword imagine. It will then randomly choose one of the comments and run it through DeepAI’s Text2Img API. After grabbing the output URL, it runs it through another API from DeepAI simply called Deep Dream, for 5 iterations to give it a more ‘wild look’. Then the resulting image is posted, describing the input the AI was given and crediting the user who originally supplied it.

Here are the resources that you'll need to get the APIs from:<br>
| API Sources   |      
| ------------- |
| [Apify](https://apify.com)         |
| [SerpApi](https://serpapi.com)     |
| [DeepAI](https://deepai.org)           |
| [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/getting-started) |

*Be sure to run `pip install -r requirements.txt` before anything else

## Please Read:
The resulting log file(s) that are created after a successful run must be **MANUALLY** moved over to logs/.<br><br>
**Q**: Why is this?<br>
**A**: You should be keeping up to date with how this bot runs. I suggest you review your log files after each run just to make sure you fully understand what's happening behind the scenes.
In all seriousness, I will probably push a commit with some changes that allow for the files to automatically be moved to their respective directory, but as of right now this bot is in its beta. Making sure you know what's happening in the mean time creates better understanding for what's really going on. When this is *actually* stable this won't be something to take note of and I'll be all for running this bot on a cronjob for months without ever checking on it.

If you have any questions, please feel free to reach out to me.<br>
**04/13/2022**: I'm working on resolving this to make things easier. I'll push a commit when I have time. Thank you!

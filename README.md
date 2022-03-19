# HorrorBot for Instagram 🧟‍♀️
An Instagram bot that utilizes DeepAI's API.

If you'd like to learn more about how this bot works, I highly recommend you check out [my blog post](https://ckyy.medium.com/creating-horrorbot-46072dd5de2e) about it, which goes into this a lot deeper.

To give you a brief summary of what this bot does:
> Once a week, this bot will pull all of the comments from my most recent Instagram post and select any comments starting with the keyword imagine. It will then randomly choose one of the comments and run it through DeepAI’s Text2Img API. After grabbing the output URL, it runs it through another API from DeepAI simply called Deep Dream, for 5 iterations to give it a more ‘wild look’. Then the resulting image is posted, describing the input the AI was given and crediting the user who originally supplied it.

Here are the resources that you'll need to get the APIs from:<br>
| API Sources   |      
| ------------- |
| [Apify](https://apify.com)         |
| [DeepAI](https://deepai.org)           |
| [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/getting-started) |

If you have any questions, please feel free to reach out to me. 

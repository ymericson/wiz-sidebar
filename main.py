import praw, config
from nba_data import perGame, schedule, standings

print(schedule, "\n", standings, "\n", perGame )

def editSidebar():
    reddit = praw.Reddit(
        client_id = config.client_id,
        client_secret = config.client_secret,
        user_agent = config.user_agent,
        password = config.password,
        username = config.username,
    )
    subreddit = reddit.subreddit("washingtonwizards")
    # old_sidebar = subreddit.mod.settings()['description']
    # print(old_sidebar)

    sidebar = subreddit.wiki["config/sidebar"]
    sidebar.edit(content = 
                 
"""
*****

[/r/WashingtonWizards Chat on Discord](https://discord.gg/bZMNwXB)

*****

[Official Site of the Washington Wizards](http://www.nba.com/wizards/)

[Facebook page](http://www.facebook.com/Wizards)

[Twitter \\(@WashWizards\\)](http://twitter.com/washwizards)

*****
[Wizards Schedule](http://www.nba.com/wizards/schedule)

""" 

+ "\n\n\n" + schedule + "\n\n\n" + standings + "\n\n\n" +  perGame + "\n\n\n" +  
# + "\n\n\n" + schedule + "\n\n\n" + standings + "\n\n\n" + 


"""

*****

**Rules**


* Be civil. This is for respectful discussion about the Wizards, constructive criticism of the team and the occasional friendly banter with opposing fans. If you are racist, sexist, or homophobic, you will be banned without a warning.

* Follow [Reddiquette](http://www.reddit.com/wiki/reddiquette) when posting/voting. Only downvote posts/comments that are off-topic or offensive.

* If you think your post has been caught in the spam filters, please message the moderators.
    
* NO NSFW content unless it is somehow on-topic, and if so please mark it NSFW.

* No obvious karma grabs (i.e. "<-- amount of assists John Wall will get today" "Today is my cakeday, here is a silly picture of Bradley Beal"). Self-posts of this nature are not encouraged but allowed. Low-effort self-posts with just a title and nothing to add will be removed. 

*****

***Related Subreddits***

* /r/nba 
* /r/basketball
* /r/washingtondc
* /r/Nationals 
* /r/washingtonNFL
* /r/caps 
* /r/DCUnited 
* /r/DCDefenders
                           
"""                     
    )
                           

if __name__ == "__main__":
    editSidebar()

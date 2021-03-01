import praw, config, requests
from nba_data import perGame, schedule, standings
import tabulate


def editSidebar():
    reddit = praw.Reddit(
        client_id = config.client_id,
        client_secret = config.client_secret,
        user_agent = config.user_agent,
        password = config.password,
        username = config.username,
    )
    subreddit = reddit.subreddit("windsandtime")
    # old_sidebar = subreddit.mod.settings()['description']
    # print(old_sidebar)

    sidebar = subreddit.wiki["config/sidebar"]
    sidebar.edit(content = schedule + "\n\n\n" + 
                           standings + "\n\n\n" +
                           perGame
                           )

if __name__ == "__main__":
    editSidebar()

# https://praw.readthedocs.io/en/latest/code_overview/other/subredditmoderation.html?highlight=sidebar#praw.models.reddit.subreddit.SubredditModeration.update
# https://github.com/praw-dev/praw

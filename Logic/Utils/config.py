class Configuration:
    """
    Define the credentials needed to establish a connection with twitter and do streaming.
    https://apps.twitter.com/
    """

    def __init__(self):
        self.Version = 0.1
        self.Author = 'CAOBA_Extraccion'

    #### Variables Twitter
    def TWITTER_CONSUMER_KEY(self):
        """

        :rtype: String
        :returns:Consumer key to allow the streaming from twitter.
        """
        return 'r8g1ylfHtqmdD09GJQwBWEuen'

    def TWITTER_CONSUMER_SECRET(self):
        """

        :rtype: String
        :returns:Consumer secret to allow the streaming from twitter.
        """
        return 'OlbOiGAs5i2MLNrlXy8tEWYby4O8m8YbSzsUd62KXJbNqhxNJp'

    def TWITTER_OAUTH_TOKEN(self):
        """

        :rtype: String
        :returns:Authentication token to allow the streaming from twitter.
        """
        return '563154603-BMOkX4yBnCUNuYT7UQFvqm7ixvBptba8z8CacqNZ'

    def TWITTER_OAUTH_TOKEN_SECRET(self):
        """

        :rtype: String
        :returns:Authentication token secret to allow the streaming from twitter.
        """
        return 'V7f1HjgTnlEH3Wl0XP0XEwlKohxAi8yeYI1Yhl9fwgJNf'

    ### MongoDB Variables

    def MONGO_URL(self):
        """

        :rtype: String
        :returns:mongodb server direction
        """

        return 'mongodb://localhost:27017//'

    def MONGO_DB(self):
        """

        :rtype: String
        :returns:String: name of the data base to be created on mongo
        """
        return 'Caoba'

    def MONGO_COLL_TWEET(self):
        """

        :rtype: String
        :returns:name of the collection where the Twitter data will be saved
        """
        return 'Tweets'

    def MONGO_COLL_TweetsGnip(self):
        return "tweetsGNIP24"

    def MONGO_COLL_LOGICCONVERSATION(self):
        """

        :rtype: String
        :returns:String::name of the collection where the processing data will be saved
        """

        return 'UserGeneratedContent'

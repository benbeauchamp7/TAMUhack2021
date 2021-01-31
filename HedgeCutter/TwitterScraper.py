import tweepy
import psycopg2

# Based off code from:
# https://www.storybench.org/how-to-collect-tweets-from-the-twitter-streaming-api-using-python/

# authorization tokens
consumer_key = "1355580293227417600-FAcjHFVbPLI73H26x2o63b6T4SaWum"
consumer_secret = "7WWUf0jMLP9sVYIBS647vq6ZWaI8nJ3vFchyYUkCphQhM"
access_key = "JOKkLqw9I7joLgcDZYVNy3DKc"
access_secret = "pqhqbrsoA8XAG0Y4VEfOio97iCPsecrVW7U8PI1RKlCYq90rkl"
con = psycopg2.connect(database="HedgeCutter_development", user="tamuhack2021", password="cheese", host="localhost", port="5432")
con.autocommit = True
cursor = con.cursor()
tickers = []

# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")

        # check if text has been truncated
        if hasattr(status,"extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text

        # check if this is a quote tweet.
        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            # check if quoted tweet's text has been truncated before recording it
            if hasattr(status.quoted_status,"extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

        # remove characters that might causde problems with csv encoding
        text.replace("\n"," ")
        quoted_text.replace("\n", " ")
    
        quoted_text = quoted_text if quoted_text != "" else " "
        username = status.user.screen_name.replace("'", "''")
        text = text.replace("'", "''")
        quoted_text = quoted_text.replace("'", "''")
        
        print(text)
        def parse(text):
            tag = ""
            for i in range(len(text)):
                if text[i] == '$':
                    for j in range(i, len(text)):
                        if text[j] not in ['\n', ' ']:
                            tag += chr(ord(text[j]))
                        else:
                            return tag

        try:
            tag = parse(text).upper()
            tag = tag if len(tag) > 0 else "$GME"
        except:
            tag = "$GME"
        
        dbStr = f"INSERT INTO tweets (id, username, datetime, isrt, isquote, text, quoted_text, tag) VALUES \
        ({status.id_str}, '{status.user.screen_name}', '{status.created_at}',  {is_retweet}, {is_quote}, '{text}', '{quoted_text}', '{tag}');"
        try: 
            cursor.execute(dbStr)
        except:
            pass 

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        exit()

if __name__ == "__main__":
    f = open("StockTickers.txt", "r")
    for i in range(6414):
        tickers.append("$"+f.readline())
    print(tickers[0])
    # complete authorization and initialize API endpoint
    auth = tweepy.OAuthHandler(access_key, access_secret)
    auth.set_access_token(consumer_key, consumer_secret)
    api = tweepy.API(auth)
    
    # initialize stream
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener,tweet_mode='extended')

    try:
        stream.filter(track = tickers[0:100])
    except KeyboardInterrupt as e:
        con.close()
        print("Connection Closed!")

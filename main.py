#!/usr/bin/env python
"""
    hot2bot

    Twitter bot framework for use with Cobe

    File name: main.py
    Author: Jesse Hamilton
    Date created: 9/30/2016
    Date last modified: 10/2/2016
    Python Version: 2.7
"""

# importing so many things!!
from cobe.brain import Brain
from collections import Counter
import configparser
import random
import re
import time
import twitter
import unicodedata

config = configparser.RawConfigParser()
configPath = r'config.conf'
config.read(configPath)



# api constants, might move these to a config later
consumerKey = config.get('api', 'consumerKey')
consumerSecret = config.get('api', 'consumerSecret')
tokenKey  = config.get('api', 'tokenKey')
tokenSecret  = config.get('api', 'tokenSecret')

# other constants, same with these
tweetFreq  = config.getint('options', 'tweetFrequency') #60 # how many minutes between tweets
subtweetChance  = config.getint('options', 'chanceToSubtweet') #10 # percent chance that the bot subtweets
topWords  = config.getint('options', 'topSubtweetSeeds') #5 # number of top words to potentially choose from for our seed phrase
tweetCount  = config.getint('options', 'maxTimelineTweets') #200 # max number of tweets to pull from timeline, up to 200


# other variables, hugeass list of stopwords from http://www.ranks.nl/stopwords with a couple twitter-specific ones added
lastId = '1'
lastMentionId = '1'
lastDMId = '1'
statuses = ''
timeCount = 0
stopwords = ['a','able','about','above','abst','accordance','according','accordingly','across','act','actually','added','adj','affected','affecting','affects','after','afterwards','again','against','ah','all','almost','alone','along','already','also','although','always','am','among','amongst','an','and','announce','another','any','anybody','anyhow','anymore','anyone','anything','anyway','anyways','anywhere','apparently','approximately','are','aren','arent','arise','around','as','aside','ask','asking','at','auth','available','away','awfully','b','back','be','became','because','become','becomes','becoming','been','before','beforehand','begin','beginning','beginnings','begins','behind','being','believe','below','beside','besides','between','beyond','biol','both','brief','briefly','but','by','c','ca','came','can','cannot','can\'t','cause','causes','certain','certainly','co','com','come','comes','contain','containing','contains','could','couldnt','d','date','did','didn\'t','different','do','does','doesn\'t','doing','done','don\'t','down','downwards','due','during','e','each','ed','edu','effect','eg','eight','eighty','either','else','elsewhere','end','ending','enough','especially','et','et-al','etc','even','ever','every','everybody','everyone','everything','everywhere','ex','except','f','far','few','ff','fifth','first','five','fix','followed','following','follows','for','former','formerly','forth','found','four','from','further','furthermore','g','gave','get','gets','getting','give','given','gives','giving','go','goes','gone','got','gotten','h','had','happens','hardly','has','hasn\'t','have','haven\'t','having','he','hed','hence','her','here','hereafter','hereby','herein','heres','hereupon','hers','herself','hes','hi','hid','him','himself','his','hither','home','how','howbeit','however','hundred','i','id','ie','if','i\'ll','im','immediate','immediately','importance','important','in','inc','indeed','index','information','instead','into','invention','inward','is','isn\'t','it','itd','it\'ll','its','itself','i\'ve','j','just','k','keep','keeps','kept','kg','km','know','known','knows','l','largely','last','lately','later','latter','latterly','least','less','lest','let','lets','like','liked','likely','line','little','\'ll','look','looking','looks','ltd','m','made','mainly','make','makes','many','may','maybe','me','mean','means','meantime','meanwhile','merely','mg','might','million','miss','ml','more','moreover','most','mostly','mr','mrs','much','mug','must','my','myself','n','na','name','namely','nay','nd','near','nearly','necessarily','necessary','need','needs','neither','never','nevertheless','new','next','nine','ninety','no','nobody','non','none','nonetheless','noone','nor','normally','nos','not','noted','nothing','now','nowhere','o','obtain','obtained','obviously','of','off','often','oh','ok','okay','old','omitted','on','once','one','ones','only','onto','or','ord','other','others','otherwise','ought','our','ours','ourselves','out','outside','over','overall','owing','own','p','page','pages','part','particular','particularly','past','per','perhaps','placed','please','plus','poorly','possible','possibly','potentially','pp','predominantly','present','previously','primarily','probably','promptly','proud','provides','put','q','que','quickly','quite','qv','r','ran','rather','rd','re','readily','really','recent','recently','ref','refs','regarding','regardless','regards','related','relatively','research','respectively','resulted','resulting','results','right','run','s','said','same','saw','say','saying','says','sec','section','see','seeing','seem','seemed','seeming','seems','seen','self','selves','sent','seven','several','shall','she','shed','she\'ll','shes','should','shouldn\'t','show','showed','shown','showns','shows','significant','significantly','similar','similarly','since','six','slightly','so','some','somebody','somehow','someone','somethan','something','sometime','sometimes','somewhat','somewhere','soon','sorry','specifically','specified','specify','specifying','still','stop','strongly','sub','substantially','successfully','such','sufficiently','suggest','sup','sure','take','taken','taking','tell','tends','th','than','thank','thanks','thanx','that','that\'ll','thats','that\'ve','the','their','theirs','them','themselves','then','thence','there','thereafter','thereby','thered','therefore','therein','there\'ll','thereof','therere','theres','thereto','thereupon','there\'ve','these','they','theyd','they\'ll','theyre','they\'ve','think','this','those','thou','though','thoughh','thousand','throug','through','throughout','thru','thus','til','tip','to','together','too','took','toward','towards','tried','tries','truly','try','trying','ts','twice','two','u','un','under','unfortunately','unless','unlike','unlikely','until','unto','up','upon','ups','us','use','used','useful','usefully','usefulness','uses','using','usually','v','value','various','\'ve','very','via','viz','vol','vols','vs','w','want','wants','was','wasnt','way','we','wed','welcome','we\'ll','went','were','werent','we\'ve','what','whatever','what\'ll','whats','when','whence','whenever','where','whereafter','whereas','whereby','wherein','wheres','whereupon','wherever','whether','which','while','whim','whither','who','whod','whoever','whole','who\'ll','whom','whomever','whos','whose','why','widely','willing','wish','with','within','without','wont','words','world','would','wouldnt','www','x','y','yes','yet','you','youd','you\'ll','your','youre','yours','yourself','yourselves','you\'ve','z','zero','rt','twt','fans']

def subtweet(subtweetCorpus):
    """
        Function: subtweet

        Recieves: multiword string
        Returns: single word string

        Outline:
            Takes string, normalizes to ascii, removes any stopwords/urls/mentions to make a new corpus
            Counts up all words in corpus, takes the most common words, randomly chooses one, and returns seed word
    """
    subtweetCorpus = re.sub(r'@\w+', r'', subtweetCorpus) # @mentions
    subtweetCorpus = re.sub(r'#\w+', r'', subtweetCorpus) # #hashtags
    subtweetCorpus = re.sub(r'\(x[1-9]*\)', r'', subtweetCorpus) # (x1000) rt numbers from oysttyr
    subtweetCorpus = re.sub(r'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r'', subtweetCorpus) # urls
    subtweetCorpus = subtweetCorpus.replace('\n', ' ').replace('\r', '')
    print subtweetCorpus

    # only keep ascii characters from 32-122 in our subtweet corpus
    subtweetCorpus = ''.join([i if ord(i) > 31 and ord(i) < 123 else '' for i in subtweetCorpus])

    #split the string into a list again
    subtweetWords = subtweetCorpus.split()
    remainingWords = []

    # for every word in our corpus, normalize to ascii (which should be done by the join a couple lines up, i can probably remove this),
    # remove all non-alphanumeric characters, and check if it exists in our stopword list. If it doesn't, add it to a new list for coutning
    for word in subtweetWords:
        word = unicodedata.normalize('NFKD', word).encode('ascii','ignore')
        word = re.sub(r'[^\w]', '', word)
        if word.lower() not in stopwords:
            remainingWords.append(word)
    print remainingWords

    # there might be zero-length strings in our list, so join our list into a string (delimited by spaces) then split again!
    remainingWords = ' '.join(remainingWords).split()
    print remainingWords

    # count all of our words, saving this to a list of tuples containing the top words and how often they appeared
    counts = [word for word, count in Counter(remainingWords).most_common(topWords)]
    print 'top ' + str(topWords) + ' counted terms: ' + ', '.join(counts)

    # choose a random word from our list to use as a seed, and return it
    seed = random.choice(counts)
    print seed
    return seed

# init our parser and our cobe brain
b = Brain('cobe.brain')

#connect to the api
api = twitter.Api(consumer_key=consumerKey,consumer_secret=consumerSecret,access_token_key=tokenKey,access_token_secret=tokenSecret)
print(api.VerifyCredentials())

"""
    main loop

    Increments a counter, and grabs our timeline, only pulling since the last tweet we pulled.
    Learns all tweets.
    If counter is greater than our tweetFreq variable, we also post a tweet.
        First we find out if we'll subtweet by choosing a random in from 0-100 and seeing if it is less than our subtweetChance
        if it is, we'll generate a seed word from the subtweet() function amd use that to generate a tweet through Cobe
        if not, we'll just generate a tweet without a seed through Cobe.
        we then remove any mentions, urls, hashtags, and RT counts that Cobe may have returned

        we then post the tweet, ignoring the exception if it is a duplicate tweet.

        finally, we reset our variables
    we then sleep for a minute before learning and possibly tweeting again

"""
while 1:
    timeCount = timeCount + 1
    timeline = api.GetHomeTimeline(exclude_replies=True, count=tweetCount, since_id=lastId)
    for s in timeline:
        statuses = statuses + ' ' + s.text
        print "learning " + s.text
        b.learn(s.text)
    lastTweet = timeline[-1]
    print lastId
    lastId = lastTweet.id
    print lastId
    if timeCount >= tweetFreq:
        print "TWEETING TIME"
        if random.randint(0,100) < subtweetChance:

            tweet = b.reply(subtweet(statuses))
        else:
            tweet = b.reply('')
        print tweet

        tweet = re.sub(r'@\w+', r'', tweet)
        tweet = re.sub(r'#\w+', r'', tweet)
        tweet = re.sub(r'\(x[1-9]*\)', r'', tweet)
        tweet = re.sub(r'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', r'', tweet)

        try:
            api.PostUpdate(tweet)
        except:
            pass

        print 'emptying our vars now'
        timeCount = 0
        statuses = ""
        statusesWords = []
        remainingWords = []
        counts = []
        seed = ""
        tweet = ""

    print "sleeping now"
    time.sleep(60) # one minute
    print "I'm awake i swear mom"

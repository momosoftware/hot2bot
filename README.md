# hot2bot

## Synopsis

#### Python Twitter bot framework for use with [Cobe](https://github.com/pteichman/cobe)

**Currently**:

* Authenticates to Twitter or [Mastodon](https://github.com/Gargron/mastodon)
* Grabs timeline since last run
* Has Cobe learn the statuses
* Tweets:
* * Decides whether or not to subtweet, subtweets by counting common words, choosing one of the most common words, using that as seed phrase in cobe
* * Uses seed phrase (or lack thereof if not subtweeting) to get a tweet from Cobe, posts that tweet

## To Do

* Save lastId to config file in case of restart (in prep for replies as to not spam on restart)
* Test Mastodon integration more fully, expand readme with instructions for it
* Reply to tweets w/ a random seed word from their tweet
* Reply to DMs in a similar fashion
* ~~Make a proper config file~~ done!
* log to file instead of console
* More options to decide how it functions
* Possibly write to use Classes and Methods instead of Functions




## Installation

**Install [Cobe](https://github.com/pteichman/cobe)**:
* `git clone https://github.com/pteichman/cobe.git`
* Navigate to the cobe directory
* `easy_install cobe`

**Install Python-Twitter**:
* `pip install python-twitter`

**Use hot2bot with Twitter**:
* Navigate to the hot2bot directory
* Run `cobe init` to create a Cobe Brain for hot2bot to operate with
* At the [Twitter Apps](https://apps.twitter.com/) page, create a new twitter app.
* Give it a unique name, a description, fill in the [hot2bot github page](https://github.com/acostoss/hot2bot) for the website. Leave callback blank, Accept the agreement, and click the "Create your app" button
* On your app  management screen, click the "Keys and Access Tokens" tab
* Generate Access tokens. Take note of the Consumer Key, Consumer Secret, Access Token and Access Token Secret
* Copy/rename `config.default.conf` to `config.conf`
* Fill in the Consumer and Token info on the corresponding lines, without quotes.
* Run with `python main.py`. It will begin learning from your timeline every minute and posting every 60 minutes. If you'd like it to post more often, change the `tweetFrequency` value in the config file

## Credits
Credit to [@Masaka_Arienai](https://twitter.com/Masaka_Arienai) on Twitter [for the name](https://twitter.com/Masaka_Arienai/status/782644624288575492)

Credit to @Gargron on [Twitter](https://twitter.com/Gargron) and [Github](https://github.com/Gargron) for the [Mastodon](https://github.com/Gargron/mastodon) integration

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

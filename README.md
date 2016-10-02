# hot2bot

## Synopsis

#### Python Twitter bot framework for use with Cobe

**Currently**:

* Authenticates to twitter
* Grabs timeline since last run
* Has Cobe learn the statuses
* Tweets:
* * Decides whether or not to subtweet, subtweets by counting common words, choosing one of the most common words, using that as seed phrase in cobe
* * Uses seed phrase (or lack thereof if not subtweeting) to get a tweet from Cobe, posts that tweet

## To Do

* Reply to tweets w/ a random seed word from their tweet
* Reply to DMs in a similar fashion
* ~~Make a proper config file~~ done!
* log to file instead of console
* More options to decide how it functions
* Possibly write to use Classes and Methods instead of Functions




## Installation

* install cobe and python-twitter
* put your API credentials in
* run with `python main.py`

proper instructions coming soonish

## Credits
Credit to [@Masaka_Arienai](https://twitter.com/Masaka_Arienai) on Twitter [for the name](https://twitter.com/Masaka_Arienai/status/782644624288575492)

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

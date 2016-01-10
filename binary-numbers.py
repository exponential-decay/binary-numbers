# https://github.com/exponential-decay/binary-numbers
#
# Application to automatically update a Twitter profile picture with a 
# dynamically created image. The code currently makes use of the Python 
# Imaging Library (PIL) to create dynamic images and then push them to 
# twitter daily.
#
# License: Beerware. For more information see GitHub repository:
# https://github.com/exponential-decay/binary-numbers/blob/master/license.md
# 
#
from twitter import *
import auth
import oauth
import oauth2
import oauth_dance
import os
import base64
import binarygenerator

write_dir = 'image-history/'   #'/var/www/static/images/'
write2file = True
   
def twitter_authentication():
   CONSUMER_KEYS = os.path.expanduser('.twitter-consumer-keys')
   CONSUMER_KEY, CONSUMER_SECRET = oauth.read_token_file(CONSUMER_KEYS)

   MY_TWITTER_CREDS = os.path.expanduser('.twitter-bin-numbers-credentials')
   if not os.path.exists(MY_TWITTER_CREDS):
      oauth_dance("binary-numbers", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)

   oauth_token, oauth_secret = oauth.read_token_file(MY_TWITTER_CREDS)
   twitter = Twitter(auth=oauth.OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))
   
   return twitter

def write_to_file(output, bingen):
   fname = bingen.get_date('fname')
   f = open(write_dir + fname + '.png', 'wb')
   f.write(output.getvalue())
   f.close()

def update_profile_pic(twitter):
   bingen = binarygenerator.BinaryGenerator()
   output = bingen.create_image()
   if write2file == True:
      write_to_file(output, bingen)
   profile_picture = base64.b64encode(output.getvalue())
   #twitter.account.update_profile_image(image=profile_picture, _base64=True)
   
def main():
   twitter = twitter_authentication()
   update_profile_pic(twitter)

if __name__ == "__main__":
    main()

import oauth2 as oauth
import urllib2 as urllib
import sys
import time
import os

time_input = sys.argv[1]
max_time = int(time_input)
start_time = time.time()

# See Assignment 1 instructions for how to get these credentials
access_token_key = str(os.environ.get('access_token_key'))
access_token_secret = str(os.environ.get('access_token_secret'))

consumer_key = str(os.environ.get('consumer_key'))
consumer_secret = str(os.environ.get('consumer_secret'))


_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://stream.twitter.com/1.1/statuses/sample.json"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  for line in response:
    if time.time() - start_time < max_time:
      print line.strip()
    else:
      return

if __name__ == '__main__':
  while (time.time() - start_time) < max_time:
   fetchsamples()
  

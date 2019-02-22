import os
import time
from tempfile import gettempdir

from selenium.common.exceptions import NoSuchElementException

from instapy import InstaPy

insta_username = 'x'
insta_password = 'x'

# set headless_browser=True if you want to run InstaPy on a server

# set these in instapy/settings.py if you're locating the
# library in the /usr/lib/pythonX.X/ directory:
#   Settings.database_location = '/path/to/instapy.db'
#   Settings.chromedriver_location = '/path/to/chromedriver'

session = InstaPy(username=insta_username,
                  password=insta_password,
                  headless_browser=False,
                  multi_logs=True)

try:
    session.login()

    # settings
    session.set_relationship_bounds(enabled=True,
				 potency_ratio=-1.21,
				  delimit_by_numbers=True,
				   max_followers=4590,
				    max_following=5555,
				     min_followers=45,
				      min_following=77)
    
    
    #Commenting based on percentage (1 photo out of every 10 = 10%)
    session.set_do_comment(False, percentage=10)
    
    #Liking based on the current number of likes on a post
    session.set_delimit_liking(enabled=True, max=100, min=None)
    
    #commenting based on the current number of comments on a post
    session.set_delimit_commenting(enabled=False, max=32, min=0)
    
    #comments to write on peoples posts. Can specify "Photo" or "Video" can add username with @{}
    session.set_comments(['aMEIzing!', 'So much fun!!', 'Nicey!'], media = 'Photo')
    
    #Dont unfollow these people
    #session.set_dont_include(['friend1', 'friend2', 'friend3'])
    
    #follow users x times (1 photo out of every 10 = 10%)
    session.set_do_follow(enabled=True, percentage=10, times=1)
    
    #wont like a photo if these hashtags are in the photo
    session.set_dont_like(['pizza', 'girl'])

    #wont unfollow users based on the likes of the past x photos
    session.set_dont_unfollow_active_users(enabled=True, posts=10)

    # actions
    
    #Like by certain hashtags
    session.like_by_tags(['rescuepup', 'dogsofinstagram', 'cutepup', 'dogmom', 'chubbypup', 'cuddlepup', 'sleepypup', 'sleepydog', 'chubbydog', 'cutedog', 'cuddledog'], amount=1)

    #control the bot
    session.set_quota_supervisor(enabled=True, sleep_after=["likes", "comments_d", "follows", "unfollows", "server_calls_h"], sleepyhead=True, stochastic_flow=True, notify_me=True,
                                  peak_likes=(30, 185),
                                   peak_comments=(21, 182),
                                    peak_follows=(48, None),
                                     peak_unfollows=(35, 402),
                                      peak_server_calls=(None, 4700))


    #unfollow users followed by instapy that dont follow you back, will unfollow after 
    session.unfollow_users(amount=60, InstapyFollowed=(True, "nonfollowers"), style="FIFO", unfollow_after=2*60*60, sleep_delay=501)

except Exception as exc:
    # if changes to IG layout, upload the file to help us locate the change
    if isinstance(exc, NoSuchElementException):
        file_path = os.path.join(gettempdir(), '{}.html'.format(time.strftime('%Y%m%d-%H%M%S')))
        with open(file_path, 'wb') as fp:
            fp.write(session.browser.page_source.encode('utf8'))
        print('{0}\nIf raising an issue, please also upload the file located at:\n{1}\n{0}'.format(
            '*' * 70, file_path))
    # full stacktrace when raising Github issue
    raise

finally:
    # end the bot session
    session.end()

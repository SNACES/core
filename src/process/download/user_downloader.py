from src.dao.twitter.twitter_dao import TwitterGetter
from src.dao.user.setter.user_setter import UserSetter
from src.shared.logger_factory import LoggerFactory
import MACROS

log = LoggerFactory.logger(__name__)

class TwitterUserDownloader():
    """
    Downloads a twitter User
    """

    def __init__(self, twitter_getter: TwitterGetter, user_setter: UserSetter):
        self.twitter_getter = twitter_getter
        self.user_setter = user_setter

    def download_user_by_screen_name(self, screen_name: str):
        if screen_name not in MACROS.DOWNLOAD_USER_NAME:
            log.debug("calling twitter getter with screen name %s" % (screen_name))
            user = self.twitter_getter.get_user_by_screen_name(screen_name)
            log.debug("storing user %s" % (str(user)))
            self.user_setter.store_user(user)

            MACROS.DOWNLOAD_USER_NAME.append(screen_name)


    def download_user_by_id(self, user_id: int):
        if user_id not in MACROS.DOWNLOAD_USER_ID:
            log.debug("calling twitter getter with user id %s" % (str(user_id)))
            if not self.user_setter.contains_user(user_id):
                user = self.twitter_getter.get_user_by_id(user_id)
                log.debug("storing user %s" % (str(user)))
                self.user_setter.store_user(user)

            MACROS.DOWNLOAD_USER_ID.append(user_id)


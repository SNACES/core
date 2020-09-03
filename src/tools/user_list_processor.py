from src.process.twitter_download.twitter_downloader import *

# TODO: rework this
class UserListProcessor:
    """
    Return a list of users given the path to a file containing a list of users.
    """

    def user_list_parser(self, user_list_file_path):
        with open(user_list_file_path, 'r') as stream:
            return [user.strip() for user in stream]

    """
    Precondition: argv matches the args for download_function
    """

    def download_function_by_user_list(self, download_function, user_list, *argv):
        def curried_operation(acc, id): return download_function(
            id, *argv)  # acc is a dummy var

        self.process_user_list(user_list, curried_operation)

    def process_user_list(self, user_list, curried_function):
        functools.reduce(curried_function, user_list)

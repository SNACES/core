class UserListProcessor:
    def user_list_parser(self, user_list_file_path):
        """
        Return a list of users given the path to a file containing a list of users.
        """
        with open(user_list_file_path, 'r') as stream:
            return [user.strip() for user in stream]

    def download_function_by_user_list(self, download_function, user_list, *argv):
        """
        Precondition: argv matches the args for download_function
        """
        # def curried_download(id): return download_function(id, *argv) 
        curried_download = lambda id: download_function(id, *argv)
        return list(map(curried_download, user_list))
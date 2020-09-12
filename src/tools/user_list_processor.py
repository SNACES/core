class UserListProcessor:
    def user_list_parser(self, user_list_file_path):
        """
        Return a list of users given the path to a file containing a list of users.
        """
        with open(user_list_file_path, 'r') as stream:
            return [user.strip() for user in stream]

    def run_function_by_user_list(self, function, user_list, *argv):
        """
        Precondition: argv matches the args for function
        """
        curried_func = lambda id: function(id, *argv)
        return list(map(curried_func, user_list))
#  The file should contain a list of all transactions.store made during a year or more.
#  Operate on a file that contains a list of transaction detail


class FileStoresList:
    def __init__(self, full_path_to_the_file):
        self.opened_file = open(full_path_to_the_file)
        self.list_stores_i_went = self.get_list_from_file()
        dic_stores_and_n_times = self.get_dictionary_with_n_times_i_shopped()
        self.dic_sorted_by_times = sorted(dic_stores_and_n_times.items(), key=lambda kv: kv[1], reverse=True)
        self.opened_file.close()

    def print(self):
        for each in self.dic_sorted_by_times:
            print(each)


    def get_list_from_file(self):
        result = []
        for i in self.opened_file.readlines():
            result.append(i.rstrip())
        return result

    def get_dictionary_with_n_times_i_shopped(self):
        result = {}
        for store in self.list_stores_i_went:
            if store in result:
                result[store] += 1
            else:
                result[store] = 0
        return result

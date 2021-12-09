

class FileStoresList:
    def __init__(self, full_path_to_the_file):
        self.opened_file = open(full_path_to_the_file)
        list_transactions = self.get_list_from_file()


        dictionary = {}
        for transaction in list_transactions:
            if transaction in dictionary:
                dictionary[transaction] += 1
            else:
                dictionary[transaction] = 0

        sorted_x = sorted(dictionary.items(), key=lambda kv: kv[1], reverse=True)

        for key in sorted_x:
            print(key)

    def get_list_from_file(self):
        result = []
        for i in self.opened_file.readlines():
            result.append(i.rstrip())
        return result

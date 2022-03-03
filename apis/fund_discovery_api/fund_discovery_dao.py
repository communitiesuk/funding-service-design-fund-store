class FundDiscoveryDAO:
    """A dummy interface to use instead of a database ORM."""

    def __init__(self):
        self.funds = {}

    def create(self, data):
        key = data["fund_name"]
        self.funds[key] = data["fund_description"]
        print(self.funds)

    def load_dummy(self, fund_data):

        for fund in fund_data:

            self.create(fund)

    def search(self, words):
        return_list = []
        word_list = words.split("-")
        for key, value in self.funds.items():
            for word in word_list:
                if word in key or word in value:
                    return_list.append(
                        {"fund_name": key, "fund_description": value}
                    )
        return return_list

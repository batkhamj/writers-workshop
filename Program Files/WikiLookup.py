import wikipedia


class WikiInfo:
    def __init__(self):
        super().__init__()

        self.info = []

    def find(self, string):
        #Call the Wikipedia api to look up the word
        self.info = wikipedia.search(string)
        ret_list = self.info

        #Get the full info of the page
        Contents = wikipedia.page(self.info[0])
        self.mv = len(self.info)
        print(self.info)

        #separate summary / content
        summary = Contents.summary
        title = Contents.title

        return summary, ret_list, title
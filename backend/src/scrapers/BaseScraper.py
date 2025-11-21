class BaseScraper: 
    def run(self):
        # pass
        data = self.scrape()
        # res = self.parse(data)
        return data
        # self.normalize()

    def scrape(self):
        raise NotImplementedError
    
    def parse(self, data):
        raise NotImplementedError

    def normalize(self, res):
        raise NotImplementedError
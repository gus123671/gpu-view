from scrapers.bestbuy import BestBuyScraper

def print_listings(gpus):
    # print out listings
    for pairs in gpus:
        for k, v in pairs.items():
            if k == "name":
                print("gpu-view> GPU found! : {}".format(v))
            if k == "price":
                print("\t for {}".format(v))
            if k == "link":
                print("\t @ {}".format(v))

        print(f"\ngpu-view> Summary -- captured {len(gpus)} GPU listings. Happy hunting!")

def run():
    print_listings(BestBuyScraper().run())

if __name__ == "__main__":
    run()
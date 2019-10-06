import requests
from bs4 import BeautifulSoup
import os
import re
import urllib.request
import time

BASE_URL = "https://www.pokemon.co.jp/ex/shirts/en/pattern_all/"
BASE_IMG = "https://www.pokemon.co.jp/ex/shirts/en/img/pattern_all/"

def main():
    for i in range(1, 152):
        r = requests.get("{}{}.html".format(BASE_URL, i))
        soup = BeautifulSoup(r.text, "html.parser")

        designer = soup.find("p", class_="credit").text.split("：")[1].strip()
        pokemon = soup.find("h1").text

        print(i, pokemon, designer)

        # clean dir name
        designer = re.sub("é", "e", designer)
        designer = re.sub("[^a-zA-Z0-9]", "_", designer).strip("_")

        # make a folder for the lovely designer if it does not exist already
        if not os.path.exists(designer):
            os.mkdir(designer)

        # download image into that path
        img_path = "{}/{}_{}.jpg".format(designer, i, pokemon)

        if not os.path.exists(img_path):
            urllib.request.urlretrieve("{}{}.jpg".format(BASE_IMG, i), img_path)

        time.sleep(1.5)
        break

if __name__ == "__main__":
    main()

import logging
from dateutil import parser
from os.path import join, dirname
import  sys, environ, os
from pathlib import Path
from dnbcreditparser.parser import parse_credit_rating
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler("pdfparser.log"),
                              logging.StreamHandler()])


if __name__ == '__main__':
    starter=dirname(__file__)
    from pathlib import Path
    for p in os.listdir("./data/"):
        print(p)
        path = Path("./data/" + str(p))
        filep = os.path.join(starter, path.absolute())
        #print(filep)
        dtiso, df=parse_credit_rating(filep)
        print(dtiso, df)


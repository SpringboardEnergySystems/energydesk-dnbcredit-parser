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
    path = Path("./data/221102_WeeklyCreditReport.pdf")
    filep = os.path.join(starter, path.absolute())
    print(filep)
    df=parse_credit_rating(filep)
    print(df)


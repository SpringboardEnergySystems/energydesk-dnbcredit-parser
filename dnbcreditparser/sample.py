import logging
from dateutil import parser
from os.path import join, dirname
import  sys, environ, os
from pathlib import Path
from energydeskapi.sdk.common_utils import init_api
from dnbcreditparser.parser import parse_credit_rating
from dnbcreditparser.uploader import upload_ratings
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(message)s',
                    handlers=[logging.FileHandler("pdfparser.log"),
                              logging.StreamHandler()])


if __name__ == '__main__':
    starter=dirname(__file__)
    api_conn = init_api(dirname(__file__))
    from pathlib import Path
    for p in os.listdir("./data/"):
        path = Path("./data/" + str(p))
        filep = os.path.join(starter, path.absolute())
        dtiso, df=parse_credit_rating(filep)
        if dtiso is None:
            continue
        upload_ratings(api_conn, dtiso, df)



import pandas as pd
import json
from energydeskapi.counterparts.counterparts_api import CounterPartsApi, CounterPartRating
def upload_ratings(api_conn, isodt,df):
    result = df.to_json(orient="records")
    print(df)

    result=json.loads(result)
    for rec in result:
        cc=CounterPartRating( rec['company'], isodt, rec)

        CounterPartsApi.upsert_credit_rating(api_conn, cc)

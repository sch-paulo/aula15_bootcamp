from datasource.api import APICollector
from contracts.schema import PurchaseSchema
from tools.aws.client import S3Client

import time
import schedule

schema = PurchaseSchema
aws = S3Client()

def apiCollector(schema, aws, repeat):
    response = APICollector(schema, aws).start(repeat)
    print('Executed')
    return

schedule.every(1).minutes.do(apiCollector, schema, aws, 50)

while True:
    schedule.run_pending()
    time.sleep(1)
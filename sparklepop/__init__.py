import boto3
from datetime import datetime,timedelta


class SparklePop:
    def __init__(self, rds_instance: str, region: str ='us-east-1'):
        self.cw_client = boto3.client('cloudwatch', region_name=region)
        self.rds_instance = rds_instance

    def cw_free_disk_space_request(self):
        response = self.cw_client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'fetching_FreeStorageSpace',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/RDS',
                            'MetricName': 'FreeStorageSpace',
                            'Dimensions': [
                                {
                                    "Name": "DBInstanceIdentifier",
                                    "Value": self.rds_instance
                                }
                            ]
                        },
                        'Period': 18000,
                        'Stat': 'Minimum'
                    }
                }
            ],
            StartTime=(datetime.now() - timedelta(seconds=300 * 3)).timestamp(),
            EndTime=datetime.now().timestamp(),
            ScanBy='TimestampDescending'
        )
        return response['MetricDataResults'][0]['Values']
    
    @staticmethod
    def convert_bytes_to_gb(bytes):
        return bytes / 1024 / 1024 / 1024
    
    def get_free_disk_space(self):
        free_storage_space = self.cw_free_disk_space_request()
        gbs = self.convert_bytes_to_gb(free_storage_space[0])
        return gbs
    
    def check_on_free_disk_space(self, minimum_gb=10):
        free_storage_space = self.get_free_disk_space()
        if free_storage_space < minimum_gb:
            raise Exception(f"Free storage space is less than {minimum_gb}GB. Current free storage space is {free_storage_space}GB")
        else:
            print(f"Free storage space is {free_storage_space}GB. No action required.")
    
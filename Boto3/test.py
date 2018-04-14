import boto3

print ( boto3.Session().get_credentials().access_key )

print ( boto3.Session().get_credentials().secret_key )

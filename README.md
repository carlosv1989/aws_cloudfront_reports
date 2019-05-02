# aws_cloudfront_reports
AWS Cloudfront Reports

#### AWS Lambda Example for storage CloudFront RTMP events to DynamoDB

##### How to use

##### Copy, paste and change 'table_name'

```sh
 table = dynamodb.Table('table_name')
```
##Requirements
| ------ | 
|Python 3.7|
|S3 Bucket with ObjectCreated Trigger|
|Cloudfront configured for [Access Log]|

[Access Log]: <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/AccessLogs.html>



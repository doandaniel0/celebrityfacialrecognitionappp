import boto3

# Reference: https://docs.aws.amazon.com/rekognition/latest/dg/create-collection-procedure.html
# collection name: celeb-collection
def create_collection(collectionName):
    maxResults=2
    collectionId=collectionName
	
    client=boto3.client('rekognition')

    #Create a collection
    print('\nCreating collection:' + collectionId)
    response=client.create_collection(CollectionId=collectionId)
    print('Collection ARN: ' + response['CollectionArn'])
    print('Status code: ' + str(response['StatusCode']))
    print('Done...')


from botocore.exceptions import ClientError
from os import environ

# Reference: https://docs.aws.amazon.com/rekognition/latest/dg/delete-collection-procedure.html
# collection name: celeb-collection
def delete_collection(collectionName):
    collectionId=collectionName
    print('\nAttempting to delete collection ' + collectionId)
    client=boto3.client('rekognition')
    statusCode=''
    try:
        response=client.delete_collection(CollectionId=collectionId)
        statusCode=response['StatusCode']
        
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print ('The collection ' + collectionId + ' was not found ')
        else:
            print ('Error other than Not Found occurred: ' + e.response['Error']['Message'])
        statusCode=e.response['ResponseMetadata']['HTTPStatusCode']
    print('Operation returned Status Code: ' + str(statusCode))
    print('Done...')
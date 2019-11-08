# Reference: https://docs.aws.amazon.com/rekognition/latest/dg/list-faces-in-collection-procedure.html
# collection name: celeb-collection
# bucket = celeb-collection

import boto3

def list_collection(bucketName, collectionName):
    bucket=bucketName
    collectionId=collectionName
    maxResults=2
    tokens=True

    client=boto3.client('rekognition')
    response=client.list_faces(CollectionId=collectionId,
                               MaxResults=maxResults)

    print('\nFaces in collection ' + collectionId)

    names = set()
 
    while tokens:
        faces=response['Faces']
        for face in faces:
            print (face)
            names.add(face['ExternalImageId'])
        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_faces(CollectionId=collectionId,
                                       NextToken=nextToken,MaxResults=maxResults)
        else:
            tokens=False

    print('\nPrinting out filenames')
    print(names)            
    return names


# Reference: https://docs.aws.amazon.com/rekognition/latest/dg/add-faces-to-collection-procedure.html
# collection name: celeb-collection
# bucket = celeb-collection

import os

def populate_collection(bucketName, collectionName):
    bucket=bucketName
    collectionId=collectionName
    
    client=boto3.client('rekognition')
    
    names = list_collection(bucketName, collectionName)
    
    print('\nPopulating collection:' + collectionId)
    for obj in boto3.resource('s3').Bucket(bucket).objects.all():
        photo=obj.key
        if photo not in names:
            response=client.index_faces(CollectionId=collectionId,
                                        Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                        ExternalImageId=photo,
                                        MaxFaces=1,
                                        QualityFilter="AUTO",
                                        DetectionAttributes=['ALL'])
        
            print ('Results for ' + photo) 	
            print('Faces indexed:')						
            for faceRecord in response['FaceRecords']:
                 print('  Face ID: ' + faceRecord['Face']['FaceId'])
                 print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))
        
            print('Faces not indexed:')
            for unindexedFace in response['UnindexedFaces']:
                print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
                print(' Reasons:')
                for reason in unindexedFace['Reasons']:
                    print('   ' + reason)
            print('')
        else:
            print(photo + ' is already in collection')
            
            
# Reference: https://docs.aws.amazon.com/rekognition/latest/dg/add-faces-to-collection-procedure.html
# collection name: celeb-collection
# bucket = celeb-collection
def search_collection(bucketName, filename, collectionName):
    bucket=bucketName
    collectionId=collectionName
    fileName=filename
    
    threshold = 10
    maxFaces=5

    client=boto3.client('rekognition')

    response = None
    faceMatches = {}

    try:
        response=client.search_faces_by_image(CollectionId=collectionId,
                                    Image={'S3Object':{'Bucket':bucket,'Name':fileName}},
                                    FaceMatchThreshold=threshold,
                                    MaxFaces=maxFaces)
    except:
        print('No face in image')

    if response:
        faceMatches=response['FaceMatches']
        print ('\nMatching faces')
        for match in faceMatches:
                print(' '.join(os.path.splitext(match['Face']['ExternalImageId'])[0].split('_')))
                print('FaceId:' + match['Face']['FaceId'])
                print('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
                print('')
    
    return faceMatches
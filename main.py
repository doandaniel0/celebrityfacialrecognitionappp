import createDelete
import populateSearch

import os

if __name__ == "__main__":
    collectionId='collectiondatabase'
    bucket='collectiondatabase'
    uploadBucket = 'uploadtomatch'
    
    #createDelete.delete_collection(collectionId)
    #createDelete.create_collection(collectionId)
    
    populateSearch.populate_collection(bucket, collectionId)
    results = populateSearch.search_collection(uploadBucket, 'Sarah_Hyland.jpg', collectionId)
    
    #print('\nPrinting results')
    #for result in results:
    #    print(' '.join(os. ' + "{:.2f}".format(result['Similarity']) + "%\n")path.splitext(result['Face']['ExternalImageId'])[0].split('_')))
    #     #    print('Similarity:
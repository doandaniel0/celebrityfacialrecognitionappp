from __future__ import print_function
import boto3
import os
from flask import Flask, flash, Markup, render_template, request, url_for
from werkzeug.utils import secure_filename
from populateSearch import search_collection

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

application = Flask(__name__)
application.secret_key = 'secret'

s3 = boto3.client('s3')
client = boto3.client('rekognition')


def upload_file_to_s3(file, bucket_name, acl='public-read'):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                'ACL': acl,
                'ContentType': file.content_type
            }
        )
    except Exception as e:
        print('Something Happened: ', e) 
        return e

    return "{}{}".format('http://{}.s3.amazonaws.com/'.format(bucket_name), 
                         file.filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route('/', methods=['POST', 'GET'])
def upload_file():
    error = None
    if 'upload_button' in request.form:
        try:
            file = request.files['user_file']
            if file and allowed_file(file.filename) and file.filename != '':
                # Upload to S3
                file.filename = secure_filename(file.filename)
                output = upload_file_to_s3(file, 'css490-uploaded')
                
                # Retrieve and display Rekognition results
                results = search_collection('css490-uploaded', file.filename, 'celeb-collection')
                if results:
                    for result in results:
                        flash(' '.join(os.path.splitext(result['Face']['ExternalImageId'])[0].split('_')) +
                        ' Similarity: ' + "{:.2f}".format(result['Similarity']) + "%\n", 'status')
                    
                    # Display user uploaded image
                    user_image = Markup("<img src='{url}'/>".format(url=output))
                    flash(user_image, 'user_image')
                    
                    # Display celeb image
                    celeb_path = "{}{}".format('http://{}.s3.amazonaws.com/'.format('celeb-collection'), 
                                 results[0]['Face']['ExternalImageId'])
                    celeb_image = Markup("<img src='{url}'/>".format(url=celeb_path))
                    flash(celeb_image, 'celeb_image')
                    
                    # s3.delete_objects(
                    #     Bucket='css490-uploaded',
                    #     Delete={
                    #         'Objects': [
                    #             {
                    #                 'Key': file.filename
                    #             }
                    #         ]
                    #     }
                    # )
                else:
                    error = 'No face found in image'
                #flash('Upload successful: ' + str(output), 'status')
            else:
                error = 'Invalid file type (png, jpg, or jpeg only)'
        except:
            error = 'No image selected'
            
    return render_template('index.html', error=error)


@application.route('/compare', methods=['POST', 'GET'])
def upload_two_files():
    error = None
    if 'double_upload_button' in request.form:
        try:
            file1 = request.files['user_file1']
            file2 = request.files['user_file2']
            
            if (file1 and allowed_file(file1.filename) and file1.filename != '' and
                file2 and allowed_file(file2.filename) and file2.filename != ''):
                
                # Upload to S3
                file1.filename = secure_filename(file1.filename)
                file2.filename = secure_filename(file2.filename)
                output1 = upload_file_to_s3(file1, 'css490-uploaded')
                output2 = upload_file_to_s3(file2, 'css490-uploaded')
                
                response = None
                try:
                    response = client.compare_faces(SimilarityThreshold=0,
                                                    SourceImage={ 
                                                       "S3Object": { 
                                                          "Bucket": "css490-uploaded",
                                                          "Name": file1.filename
                                                       }
                                                    },
                                                    TargetImage={ 
                                                       "S3Object": { 
                                                          "Bucket": "css490-uploaded",
                                                          "Name": file2.filename
                                                       }
                                                    })
                except:
                    error = 'No face found in image'
                
                if response:
                    flash('Similarity: ' + "{:.2f}".format(response['FaceMatches'][0]['Similarity']) + '%', 'status')
                        
                    # Display user uploaded image
                    user_image = Markup("<img src='{url}'/>".format(url=output1))
                    flash(user_image, 'user_image1')
                        
                    # Display user uploaded image
                    user_image = Markup("<img src='{url}'/>".format(url=output2))
                    flash(user_image, 'user_image2')
                
                # flash('Upload successful: ' + str(output1), 'status')
                # flash('Upload successful: ' + str(output2), 'status')
            else:
                error = 'Invalid file type (png, jpg, or jpeg only)'
        except:
            error = 'Two images must be selected'
            
    return render_template('compare.html', error=error)


@application.route('/detect', methods=['POST', 'GET'])
def upload_detect_file():
    error = None
    if 'upload_button' in request.form:
        try:
            file = request.files['user_file']
            if file and allowed_file(file.filename) and file.filename != '':
                # Upload to S3
                file.filename = secure_filename(file.filename)
                output = upload_file_to_s3(file, 'css490-uploaded')
                
                response = None
                try:
                    response = client.detect_labels(Image={ 
                                                        "S3Object": { 
                                                           "Bucket": "css490-uploaded",
                                                           "Name": file.filename
                                                        }
                                                    },
                                                    MaxLabels=13)
                except:
                    error = 'No objects found in image'

                if response:
                    for label in response['Labels']:
                        flash(label['Name'] + ': ' + "{:.2f}".format(label['Confidence']) + '%', 'status')
                        
                    # Display user uploaded image
                    user_image = Markup("<img src='{url}'/>".format(url=output))
                    flash(user_image, 'user_image')
                    
                #flash('Upload successful: ' + str(output), 'status')
            else:
                error = 'Invalid file type (png, jpg, or jpeg only)'
        except:
            error = 'No image selected'
            
    return render_template('detect.html', error=error)
    
    
@application.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':    
    application.run(host='0.0.0.0', port=8080)

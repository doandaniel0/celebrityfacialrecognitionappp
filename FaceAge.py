from __future__ import print_function
import boto3
import json
import os
from flask import Flask, flash, Markup, render_template, request, url_for
from werkzeug.utils import secure_filename
from populateSearch import search_collection

client = boto3.client('rekognition',
                      aws_access_key_id='AKIAIBOPYCUVJVK3P3LA',
                      aws_secret_access_key='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')

response = client.detect_faces(Image={'S3Object': {
    'Bucket': 'uploadtomatch',
    'Name': 'Shannon.jpg'
}},

    Attributes=["ALL"]
)


print (response['FaceDetails'][0]['AgeRange'])



# RekogU
http://rekogu-dev.us-west-2.elasticbeanstalk.com/\
celebrityfacialrecognitionapp\
\
application.py - main application using flask to create webpage and interaction.\
createDelete.py - used to initially create aws Rekognitions "collection"\
main.py - simple driver to utilize createDelete.py  and populateSearch.py\
populateSearch.py - contains method called by application.py used to search and display matching celebrity photo. Also contains method to initally populate the collection with images.

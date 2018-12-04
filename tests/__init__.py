import sys
import os

PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PATH + '/../serverlessrepo/')

# set expected aws region environment variable
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

import os
import boto.s3
from django.http import HttpResponseRedirect
import datetime


conn = boto.connect_s3(aws_access_key_id='#########',
                       aws_secret_access_key='###########')


def percent_cb(complete, total):
    print('.')


def upload_to_s3_bucket_path(bucketname, path, filename):
    mybucket = conn.get_bucket(bucketname)
    fullkeyname = os.path.join(path, filename)
    key = mybucket.new_key(fullkeyname)
    key.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)


def upload_to_s3_bucket_root(bucketname, filename):
    mybucket = conn.get_bucket(bucketname)
    key = mybucket.new_key(filename)
    key.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)


def getuserfiles(bucketname, username):
    mybucket = conn.get_bucket(bucketname)
    keys = mybucket.list(username)
    totalsize = 0.0
    userfiles = {}
    for key in keys:
        value = []
        filename = key.name
        filename = filename.replace(username+'/media/', '')
        modified = datetime.datetime.strptime(key.last_modified[:19], '%Y-%m-%dT%H:%M:%S')
        value.append(modified)
        keysize = float(key.size)/1000.0
        value.append(str(keysize))
        userfiles[filename] = value
        totalsize = totalsize + float(key.size)
    totalsize = totalsize/1000000.0
    return userfiles, totalsize


def delete_from_s3(bucketname, username, filename):
    mybucket = conn.get_bucket(bucketname)
    mybucket.delete_key(username+'/media/'+filename)


def get_from_s3(bucketname, file_path):
    bucket = conn.get_bucket(bucketname)
    s3_file_path = bucket.get_key(file_path)
    url = s3_file_path.generate_url(expires_in=600)  # expiry time is in seconds

    return HttpResponseRedirect(url)

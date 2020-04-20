import boto3

def upload_file(filename, file1):
    s3 = boto3.resource('s3')
    print('here upload')

    s3.Bucket('mediaguide').put_object(Key=filename, Body=file1)

    print('done upload')

    return 'true'

def dowload_file(filename, os_path):
    s3 = boto3.client('s3')

    print("try download")

    try:
        s3.download_file('mediaguide',filename, os_path)
    except Exception as err:
        print(err.message())


    #return s3.get_object(Bucket='mediaguide',Key=filename)

    # with open(filename, 'wb') as data:
    #     s3.download_fileobj('mediaguide', filename, data)
    return 'true'

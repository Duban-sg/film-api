import boto3
from tempfile import NamedTemporaryFile
import os
import uuid



class awsS3():
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    Session = None
    client = None
    bucket = ''
    
    def __init__(self,AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,bucket):
        self.AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
        self.AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
        self.bucket = bucket

    def connect(self):
        self.Session = boto3.Session(
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
        )
        self.client = self.Session.resource('s3')

    def send_attachment(self,file,filmname,ext):
        temp = NamedTemporaryFile(delete=False)
        try:
            filename = filmname+"-"+str(uuid.uuid4())+"."+ext
            try:
                contents = file.read()
                with temp as f:
                    f.write(contents)
            except Exception as e:
                raise e 
            finally:
                file.close()
            self.client.meta.client.upload_file(temp.name, self.bucket, filename)
            return filename
        except Exception as e:
            raise e
        finally:
            os.remove(temp.name)  # Delete temp file
    
    def update_attachment(self,file,filmname):
        temp = NamedTemporaryFile(delete=False)
        try:
            try:
                contents = file.read()
                with temp as f:
                    f.write(contents)
            except Exception as e:
                raise e 
            finally:
                file.close()
            self.client.meta.client.upload_file(temp.name, self.bucket, filmname)
            return filmname
        except Exception as e:
            raise e
        finally:
            os.remove(temp.name)
    
        
    def get_url_location_file(self, key_name: str) -> str:
        response = self.client.meta.client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": self.bucket,
                "Key": key_name,
            },
            ExpiresIn=3600,
        )
        return str(response)
            

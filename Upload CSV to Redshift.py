import psycopg2
import boto3

#Redshift Credentials
host = 'examplecluster.us-east-1.redshift.amazonaws.com'
port = '5439'
dbname = 'database_name'
username = 'redshift_username'
password = 'redshift_password'

#S3 Bucket and Key
bucket_name = 's3_bucket_name'
s3_key = 'folder/subfolder1/subfolder2'

#S3 Credentials Option 1
aws_access_key_id = 'aws_access_key_id'
aws_secret_access_key = 'aws_secret_access_key'

#S3 Credentials Option 2
#iam_role = 'iam_role'

def query_redshift(current_query,fetch):
      conn_string = "host = '" + str(host) + "' port ='" + str(port) +"' dbname = '" + str(dbname) + "' user = '" + str(username) + "' password = '" + str(password) + "' connect_timeout = 30000"
      conn = psycopg2.connect(conn_string)
      conn.autocommit=True
      cursor = conn.cursor()
      cursor.execute(current_query)

      if fetch==1:
          records=cursor.fetchall()
          conn.commit()
          return records
      cursor.close()
      conn.close()
      print ("S3 to Redshift Transfer Successful")

def upload_data_to_redshift(filename, tablename):
       print ('Creating S3 Connection')
       s3 = boto3.resource('s3')
       print ('Copying Local File to S3')
       data = open(filename, 'rb')
       s3.Bucket(bucket_name).put_object(Key = s3_key, Body = data, ServerSideEncryption='AES256')
       print ('Local to S3 Transfer Successful')
      
       #S3 Option 1
       query_redshift( "COPY "+ str(tablename)+ "  FROM   's3://" + str(bucket_name) + "/" + str(s3_key) + "' credentials 'aws_access_key_id = " + str(aws_access_key_id) + "; aws_secret_access_key = " + str(aws_secret_access_key) + "' delimiter as ',' escape removequotes ACCEPTINVCHARS maxerror as 250 ; ",0)
       
       #S3 Option 2
       #query_redshift( "COPY "+ str(tablename)+ "  FROM   's3://" + str(bucket_name) + "/" + str(s3_key) + "' iam_role '" + str(iam_role) + "' delimiter as ',' escape removequotes ACCEPTINVCHARS ; ",0)

       s3.Bucket(bucket_name).delete_objects(
          Delete={
             'Objects': [
                 {
                     'Key': s3_key,

                 },
             ],

         }
         )
       print ('Staging File Deleted')

file = 'path/upload.csv'
table = 'schema.tablename'
upload_data_to_redshift(file,table)

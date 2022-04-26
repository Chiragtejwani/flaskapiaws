from flask import Flask, jsonify, request,redirect, url_for,request
from flask_cors import CORS,cross_origin
import boto3 

app = Flask(__name__)
CORS(app)

s3 = boto3.resource('s3')
sess = boto3.Session(region_name = 'us-east-1')
s3client = sess.client('s3')
ec2Client = sess.client('ec2')

@app.route('/s3/list', methods = ['GET'])
def list_buckets():
    if(request.method == 'GET'):
        response = jsonify(s3client.list_buckets()['Buckets'])
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response     

@app.route('/s3/delete', methods = ['POST'])
def delete_bucket():
    if(request.method == 'POST'):
        req = request.json
        bucket_name = req["name"]
        s3client.delete_bucket(Bucket = bucket_name)
        response = jsonify({'message': 's3 deleted'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    


@app.route('/s3/create', methods = ['POST'])
def create_bucket():
    if request.method == 'POST' :
        print('post app')
        req = request.json
        print(req)
        bucket_name = req["name"]
        s3client.create_bucket(Bucket = bucket_name) 
        response = jsonify({'some': 'data'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/s3/<name>/', methods = ['GET'])
def lsitObjs_bucket(name):
    bucket_name = name
    return jsonify(s3client.list_objects(Bucket = bucket_name)["Contents"])

@app.route('/ec2/create', methods = ['POST'])
def create_ec2():
    if (request.method == 'POST'): 
        print("EC2 ROUTE HIT")
        req = request.json
        print(req)
        image = "ami-0f9fc25dd2506cf6d"
        ec2Client.run_instances (
            ImageId = image,
            MinCount =1,
            MaxCount=1,
            InstanceType="t2.micro"
        )
        response = jsonify({'some': 'data'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/ec2/list', methods = ['GET'])
def list_ec2():
    print("list route hit")
    return jsonify(ec2Client.describe_instances()["Reservations"])

@app.route('/ec2/stop/', methods = ['POST'])
def stop_ec2():
    id = request.form['id']
    ec2Client.stop_instances(InstanceIds= [id])

@app.route('/ec2/delete', methods = ['POST'])
def terminate_ec2():
    print("EC2 DELETE ROUTE HIT")
    req = request.json
    id = req["name"]
    ec2Client.terminate_instances(InstanceIds= [id])
    response = jsonify({'message': 'ec2 deleted'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    

@app.route('/', methods = ['GET'])
def home():
    if(request.method == 'GET'):
       return redirect(url_for('list_buckets')) 

if __name__ == '__main__':
    app.run(debug = True)
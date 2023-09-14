from flask import Flask, jsonify,render_template
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv('db_uri')
client = MongoClient(uri, server_api=ServerApi('1'))
beta = client[os.getenv('dbbeta')]
production=client[os.getenv('dbproduction')]
b_name = beta[os.getenv('list')]
b_details = beta[os.getenv('collection')]
p_name=production[os.getenv('list')]
p_details=production[os.getenv('collection')]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
######################## Production ###################################
# create
@app.route('/api/insert/<bookname>', methods=['POST'])
def insert_book(bookname):
    records=b_details.find_one({'act content.Act':bookname},{'_id':0})
    documents=p_details.find_one({'act content.Act':bookname},{"_id": 0})
    if documents==records:
        return jsonify({'message':f'Record {bookname} already exist'})
    elif records:
        p_details.insert_one(records)
        p_name.insert_one(b_name.find_one({'name':bookname},{"_id": 0}))
        return jsonify({'message': f'Record {bookname} copied successfully'})
    else:
        return jsonify({'message':'No documents to copy from the beta collection.'})
    

# read
@app.route('/api/list', methods=['GET'])
def list_book():
    records = list(p_name.find({"name": {"$exists": True}},{'_id':0}))
    return records

@app.route('/api/<bookname>', methods=['GET'])
def read_book(bookname):
    records = list(p_details.find({'act content.Act':bookname},{'_id':0}))
    return records

# update
@app.route('/api/update/<bookname>', methods=['PUT'])
def update_book(bookname):
    records=b_details.find_one({'act content.Act':bookname},{'_id':0})
    documents=p_details.find_one({'act content.Act':bookname},{"_id": 0})
    result=p_details.replace_one(documents,records)
    p_name.replace_one(p_name.find_one({'name':bookname},{"_id": 0}),b_name.find_one({'name':bookname},{"_id": 0}))
    if result.modified_count:
        return jsonify({'message': f'Record {bookname} updated successfully'})
    else:
        return jsonify({'message': 'Record not found'})

# delete
@app.route('/api/delete/<bookname>', methods=['DELETE'])
def delete_book(bookname):
    result=p_details.delete_one({"act content.Act": bookname})
    p_name.delete_one({"name": bookname})
    if result.deleted_count:
        return jsonify({'message': f'Record {bookname} deleted successfully'})
    else:
        return jsonify({'message': 'Record not found'})
   
   
    
######################## Beta ###################################
# create
#@app.route('/beta/api/insert', methods=['POST'])
#def beta_insert_book(bookname):
    #import app
    # records=details.find_one({'act content.Act':bookname},{'_id':0})
    # documents=act.find_one({'act content.Act':bookname},{"_id": 0})
    # if documents==records:
    #     return jsonify({'message':f'Record {bookname} already exist'})
    # elif records:
    #     act.insert_one(records)
    #     return jsonify({'message': f'Record {bookname} copied successfully'})
    # else:
    #     return jsonify({'message':'No documents to copy from the beta collection.'})
    

# read
@app.route('/beta/api/list', methods=['GET'])
def beta_list_book():
    records = list(b_name.find({"name": {"$exists": True}},{'_id':0}))
    return records

@app.route('/beta/api/<bookname>', methods=['GET'])
def beta_read_book(bookname):
    records = list(b_details.find({'act content.Act':bookname},{'_id':0}))
    return records

# update
@app.route('/beta/api/update/<bookname>', methods=['PUT'])
def beta_update_book(bookname):
    result=b_details.replace_one(documents,records)
    b_name.replace_one()
    if result.modified_count:
        return jsonify({'message': f'Record {bookname} updated successfully'})
    else:
        return jsonify({'message': 'Record not found'})

# delete
@app.route('/beta/api/delete/<bookname>', methods=['DELETE'])
def beta_delete_book(bookname):
    result=b_details.delete_one({"act content.Act": bookname})
    b_name.delete_one({"name": bookname})
    if result.deleted_count:
        return jsonify({'message': f'Record {bookname} deleted successfully'})
    else:
        return jsonify({'message': 'Record not found'})
    

if __name__ == '__main__':
    app.run(debug=True)

# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 17:11:37 2021

@author: SAM
"""
import flask
from flask import request, jsonify
import json
import boto3
from botocore.exceptions import ClientError

import time
time.sleep(10)
table_name = 'data'

app = flask.Flask(__name__)
@app.route('/api/getbooks/books', methods=['GET'])
def get_books():
    query_parameters = request.args

    filter = query_parameters.get('filter')
    start_page = query_parameters.get('start_page')
    page_size = query_parameters.get('page_size')
    
    if not (filter or start_page or page_size):
        return page_not_found(404)
    

    
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    try:
        table = dynamodb.Table(table_name)
        response = table.get_item(Key={ 'bookID': filter})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return jsonify(response)
@app.route('/api/getbook', methods=['GET'])
def get_book():
    query_parameters = request.args

    id = query_parameters.get('id')
    
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    try:
        table = dynamodb.Table(table_name)
        response = table.get_item(Key={ 'bookID': id})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return jsonify(response)
@app.route('/api/addbook', methods=['GET'])
def add_book():
    query_parameters = request.args
    

    id = query_parameters.get('id')
    authors = query_parameters.get('authors')
    average_rating = query_parameters.get('average_rating')
    isbn = query_parameters.get('isbn')
    language_code = query_parameters.get('language_code')
    price = query_parameters.get('price')
    ratings_count = query_parameters.get('ratings_count')
    title = query_parameters.get('title')
    param={}
    if not id:
        return "invalid Id"
    if id:
        param['id']=id
    if average_rating:
        param['average_rating']=average_rating
    if authors:
        param['authors']=authors
    if isbn:
        param['isbn']=isbn
    if language_code:
        param['language_code']=language_code
    if price:
        param['price']=price
    if ratings_count:
        param['ratings_count']=ratings_count
    if title:
        param['title']=title
    
    
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table(table_name)
    response=table.put_item(Item=param)
    
    return response

@app.route('/api/updatebook', methods=['GET'])
def update_book():
    query_parameters = request.args
    

    id = query_parameters.get('id')
    authors = query_parameters.get('authors')
    average_rating = query_parameters.get('average_rating')
    isbn = query_parameters.get('isbn')
    language_code = query_parameters.get('language_code')
    price = query_parameters.get('price')
    ratings_count = query_parameters.get('ratings_count')
    title = query_parameters.get('title')
    param={}
    print(id)
    if not id:
        return "invalid Id"
    if average_rating:
        param[':r']="average_rating"
    if authors:
        param[':a']="authors"
    if isbn:
        param[':s']="isbn"
    if language_code:
        param[':l']="language_code"
    if price:
        param[':p']="price"
    if ratings_count:
        param[':c']="ratings_count"
    if title:
        param[':t']="title"
    exp="set "
    for i,j in param.items():
        exp=exp+j+"="+i+","
    print(exp[:-1])
    print(param)
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
    try:
        table = dynamodb.Table(table_name)
    
        response = table.update_item(
            Key={
                'id': id,
            },
            UpdateExpression=exp[:-1],
            ExpressionAttributeValues=param,
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return jsonify(response)

app.run()

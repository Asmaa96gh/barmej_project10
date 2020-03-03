import psycopg2 as ps
from flask import Flask, jsonify
from flask import request
import json


con = ps.connect(user="postgres", password="postgres",host="localhost", database="imdb_dataset")


app = Flask(__name__)

@app.route('/get_total_data_count', methods=['GET'])
def get_total_data_count():
    count = 0
    cur = con.cursor()
    label_name = request.args.get('label_name')
    try:
      
        if label_name == "positive":  
            cur.execute("select count(input_id) from data_labling where label_id = 0 ;") 
            count =  cur.fetchall()   
        elif label_name == "negative":  
            cur.execute("select count(input_id) from data_labling where label_id = 1 ;") 
            count = cur.fetchall()  
        elif label_name == "all":  
            cur.execute("select count(input_id) from data_labling;") 
            count =  cur.fetchall()  

        return jsonify(count)

    except Exception as error:
        print ("ERROR IN get_total_data_count ")
        print ("Exception TYPE:", type(error))



@app.route('/get_data', methods=['GET'])
def get_data():
    cur = con.cursor()                                                                               
    max_count = request.args.get('max_count')
    page = request.args.get('page')
    sort_order = request.args.get('sort_order')
    try:
        query = "select x.text_input , y.label_id from data_input as x INNER JOIN data_labling as y ON x.input_id=y.input_id order by x.date_input %s limit %s offset %s ;"
        param = (sort_order, max_count, page)
        cur.execute(query % param)
        label_text = cur.fetchall()
        text, label = zip(*label_text)
        return jsonify(label_text)

    except Exception as error:
        print("Exception TYPE:", type(error))




if __name__ == "__main__":
    app.run(debug=True, port=3000)

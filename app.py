from flask import Flask,jsonify,request
import psycopg2

#establish connection to database hosted locally
def connect_to_db():
    try:
        connection = psycopg2.connect(
                    host='localhost',
                    user='postgres',
                    password='rahul123',
                    database='propreturns_db',
                    port='5432'
                    )
        return connection
    except Exception as e:
        print("error connecting to database: ", str(e))

app = Flask(__name__)

#search by document number
@app.route('/api/get_data_by_doc_no', methods=['GET'])
def get_data_by_doc_no(): 
    doc_no = request.args.get('doc_no')   
    conn = connect_to_db()   
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM mumbai_realestate_table WHERE doc_no = %s", (doc_no,))
        data = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})


#search by registration year
@app.route('/api/get_data_by_year', methods=['GET'])
def get_data_by_year():
    year = request.args.get('year')
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM mumbai_realestate_table WHERE EXTRACT(YEAR FROM registration_date) = %s", (year,))  #year extracted from data
        data = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)})

#search by partial name (first or middle or last name)
@app.route('/api/get_data_from_partial_names', methods=['GET'])
def partial_search():
    search_query = request.args.get('query')
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        query = """
            SELECT * FROM mumbai_realestate_table
            WHERE 
                mumbai_realestate_table.buyer_name ILIKE %s OR 
                mumbai_realestate_table.seller_name ILIKE %s OR
                mumbai_realestate_table.other_information ILIKE %s
        """
        cur.execute(query, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
        data = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)

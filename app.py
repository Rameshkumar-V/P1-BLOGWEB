from flask import Flask,render_template,request,jsonify,redirect,url_for,send_file,flash
from flask_sqlalchemy import SQLAlchemy
from database import (
	db,
	add_document,
	create_documents_table,
	get_document_details_all,
	delete_document,
	email_store_db,
	email_data_db_allget,
	get_document_details,
	get_document,email_del_by_id,
	get_document_detailsx
)
from io import BytesIO
from flask_login import LoginManager, UserMixin, login_user,login_required,logout_user,current_user


app=Flask(__name__,template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmproject.db'
#app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://rameshkumar@localhost/login'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key='fjhsdkjfhskfhasdkfsh'
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        

# Static users dictionary (You can replace this with any static user data)



  # Disable Flask-SQLAlchemy modification tracking


# 1 HOME PAGE
@app.route('/')
@app.route('/home')

def Home():
	return render_template("home.html")

# HOME PAGE END


# 2 ABOUT PAGE
@app.route('/about')

def About():
	return render_template("about.html")

# ABOUT PAGE END


# 3 PROFESSIONAL ACTS PAGE
@app.route('/professionalacts')

def Profession_acts():
    document_details=get_document_detailsx("PROFESSIONAL",0)
    if document_details:
        return render_template("professionalact.html",document_details=document_details)
    else:
        return "failed"
	#return "P. acts page"

# PROFESSIONAL ACTS PAGE end

# 4 LEARNING RESROUCES PAGE

@app.route('/learningresources')

def Learning_Resources():
    document_details=get_document_detailsx("RESOURCES",0)
    if document_details:
        return render_template("learningresource.html",document_details=document_details)
    else:
        return "Page unavailable !"
# LEARNING RESROUCES PAGE end

# 5 ENGLISH ESSAY
@app.route('/englishtips')
def Essay():
    document_details=get_document_detailsx("ENGTIPS",0)
    if document_details:
        return render_template("englishtips.html",document_details=document_details)
    else:
        return "Page unavailable !"

# ENGLISH ESSAY end


# 6 PUBLICATION
@app.route('/publications')
def Publication():
    document_details=get_document_detailsx("PUBLICATION",0)
    if document_details:
        return render_template("Publications.html",document_details=document_details)
    else:
        return "Page unavailable !"




# DATABASE OPERATIONS 
# ADMIN PAGE SENDING
"""
@login_manager.user_loader
def load_user(user_id):
    # Query the database or some other source for the user with the given user_id
    # For example:
    user = USERS.get(user_id)
    return user
    pass"""
@login_manager.user_loader
def load_user(user_id):
    # Query the database or some other source for the user with the given user_id
    # For example:
    user = User(user_id=1)
    
    return user


@app.route('/admin')
def Admin():
	return render_template('adminpannel_login.html')


# SECURITY FUNCTION FOR ADMIN

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    userpass = request.form['password']
    user_id=1
    
    user = User(user_id=1)
    if username=='tt' and 'tt' == str(userpass):
        login_user(user)
        load_user(user)
        # Log in the user
        return redirect(url_for('upload_documnent_page'))  # Redirect to a protected page
    else:
        return 'Invalid username or password.'





@app.route('/uploaddoc',methods=['GET'])
@login_required

def upload_documnent_page():
	return render_template('ap_interface.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'logouted success'

# learning resources page getting binary datg to send file.
@app.route('/getfile/<int:id>', methods=['GET'])
def get_file(id):
    print("id is:", id)
    document = get_document(id)
    if document:
    	file_data = BytesIO(document['ddata'])
    	return send_file(
    		file_data,
    		as_attachment=True,
    		mimetype='application/pdf',
    		download_name=str(document['dname'])
    		)
    else:
    	abort(404)

# DOCUMENT DELETE PAGE.




@app.route('/docdelete',methods=['GET'])
@login_required

def doc_del_page():

	if request.method=='GET':
		document_details=get_document_details_all()
		print("doc details = ",document_details)
		if document_details:
			#[{"document_id":1,"document_name":"NAME OF DOCUMENT"}]
			return render_template('ap_delete_i.html',document_details=document_details)
		else:
			document_details=[{"document_id":None,"document_name":"NAME OF DOCUMENT"}]

			return render_template('ap_delete_i.html',document_details=document_details)



	
# DELETE A DOCUMENT WITH THEIR DOC ID
@app.route('/deldoc',methods=["POST"])
@login_required

def del_publication():

	if request.method=='POST':
		try:
			document_id=int(request.args.get('docid'))
			result=delete_document(document_id)
			print("result is : ",result)

			if result:
				#"DELETED"
				return jsonify({"result":result})
			else:
				#"UN DELETED"
				return jsonify({"result":str(result)})


			
		except Exception as e:
			result=f"ERROR {type(e)}"
			return jsonify({"result":str(result)})
	else:
		return jsonify("INVALID METHOD")




# UPLOAD DOCUMENT S DATAS COLLECT AREA.

@app.route('/upldoc',methods=["POST"])
@login_required

def Upload_doc():
    if request.method=='POST':
        try:
            if 'document' in request.files:
                document=request.files['document']
                section=request.form['section']
                if document:
                    doc_blob_data=document.read()
                    doc_name=str(document.filename)
                    doc_sec=str(section)
                    result=add_document(dname=str(doc_name),ddata=doc_blob_data,  dtype=str(doc_sec))
                    if result:
                        return jsonify({"result":result})
                    else:
                        return jsonify({"result":result})
                else:
                    return 'document missing !'
            else:
                return jsonify({"result":"FILE NOT FOUND"})
        except Exception as e:
      				return jsonify({"result":f"ERROR :  {e}"})
    else:
        return jsonify({"result":"wrong method"})



# FOR EMAIL ADDRESS GETTER and store to database

@app.route('/email',methods=["POST"])

def email_db_store():
	if request.method=="POST":
		try:
			emailid=request.args.get('emailid')
			message=request.args.get('message')
			print("emailidl=",emailid)
			print("msg=",message)
			result= email_store_db(emailid,message)
			if result:
				return jsonify({"result":f"MESSAGE SENDED"})
			else:
				return jsonify({"result":f"MESSAGE SENDEDING ISSUE !"})



		except Exception as e:
			return jsonify({"result":f"{type(e).__name__}"})
	else:
		return "Invalid Method !"


@app.route('/emaildetails',methods=["GET"])

def get_emails():
	if request.method=='GET':
		try:
			result=email_data_db_allget()
			print("result: ",result)
			if result:
				return render_template("admin_user_msg.html",result=result)
			else:
				return jsonify({"result":f"ISSUE !"})
		except Exception as e:
			return jsonify({"result":f"{type(e).__name__}"})
	else:
		return "Invalid Method !"


# EMAIL DELETE FUNCTION
@app.route('/emaildelete/<int:id>',methods=["POST"])
def Delete_email(id):

	if request.method=='POST':
		try:
			document_id=int(id)
			result=email_del_by_id(document_id)
			print("result is : ",result)

			if result:
				#"DELETED"
				return jsonify({"result":result})
			else:
				#"UN DELETED"
				return jsonify({"result":str(result)})


			
		except Exception as e:
			result=f"ERROR {type(e)}"
			return jsonify({"result":str(result)})
	else:
		return jsonify("INVALID METHOD")


# This for redirect email to a person.
@app.route('/compose_email/<emailid>')
def compose_email(emailid):
    # Add your logic here to retrieve additional data or perform any necessary processing
    subject = "Subject of the email"
    body = "Body of the email"

    # Redirect to the Gmail compose URL with the pre-filled data
    return redirect(f"https://mail.google.com/mail/?view=cm&fs=1&to={emailid}&su={subject}&body={body}")


"""
@app.route('/upddocsnxt',methods=['GET','POST'])
def Update_next_docs():
	dtype=request.json.get('dtype')
	dno=request.json.get('dno')
	#return dtype
	if request.method=='POST'or 'GET':
		data=get_document_detailsx(str(dtype),int(dno))
		return jsonify(data)
	else:
		return "NOt available"
"""

@app.route('/upddocsnxt',methods=['GET','POST'])
def Update_next_docs():
	if request.method == 'POST':
		dtype = request.json.get('dtype')
		dno = request.json.get('dno')
		print(dtype,dno)
		print(True)
		data = get_document_detailsx(str(dtype), int(dno))
		print(data)
		return jsonify(data)
	else:
		return "Not available"


if __name__=='__main__':
	create_documents_table()
	app.run(debug=True)




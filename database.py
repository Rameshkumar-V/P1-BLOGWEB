from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime as dt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rameshkumar@localhost/login'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Documents(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    dname = db.Column(db.String(200), unique=False) #document name
    ddata = db.Column(db.LargeBinary(length=(2**32)-1))  # Use LONGBLOB type for large binary data
    dudate = db.Column(db.String(10)) #document uploaded date
    dtype = db.Column(db.String(20)) #document type publication or document
    #dimage=db.Column(db.LargeBinary(length=(2**32)-1)) #store image

    def __init__(self, dname, ddata, dtype):
        self.dname = dname
        self.ddata = ddata #for text definition
        self.dudate = str(dt.date.today())
        self.dtype = dtype # for doc or publication
        #self.dimage=dimage # img as bin 

    def __repr__(self):
        return f"DOCUMENT NAME: {self.dname} DOCUMENT DATE: {self.dudate} DOCUMENT TYPE: {self.dtype}"




def create_documents_table():
    try:
        with app.app_context():
            db.create_all()
            print("DATABASE CREATED SUCCESSFULLY")
    except Exception as e:
        print("error on db creation : ",e)
        pass
        #print("DATABASE PROBLEMED NOW:", type(e).__name__, e)

def add_document(dname,ddata,dtype):
    #dimage=dimage,
    try:
        document_class=Documents(dname=dname,ddata=ddata,dtype=dtype)
        db.session.add(document_class)
        db.session.commit()
        #print("DOCUMENT UPLOADED")
        return "Document Uploaded Successfully."
    except Exception as e:
        #print("ERROR ON ADD DOCUMENT",e,type(e))
        db.session.rollback()

        return f"DOCUMENT ERROR FACED , ERROR IS : {type(e)} eror on : {e}."

# for get by id 
def get_document(document_id):
    try:
        document=Documents.query.get(document_id)
        print("document")


        if document:
            
            documents={"ddata":document.ddata,"dname":document.dname}
            return documents
            
        else:
            return False
    except Exception as e:
        return e


def delete_document(document_id):
    try:
        document = Documents.query.get(document_id)
        #print('DOCUMENT IS : ',document)
        

        if document:
            db.session.delete(document)
            db.session.commit()
            #print("DELETED THE DOCUMENT")
            return "Document Deleted Successfully."
        else:
            return "Document not found."

    except Exception as e:
        #print("ERROR ON DELETE DOCUMENT")
        db.session.rollback()
        return f"DOCUMENT ERROR FACED, ERROR TYPE: {type(e)}, ERROR: {e}."



# get documents by document type for pdf download page
def get_document_details(document_type):
    try:
        documents = Documents.query.filter_by(dtype=document_type).all()

        if documents:
            # Create a list to store the details of each document
            document_details = []

            
            for document in documents:
                # Append a dictionary with required details to the list
                document_details.append({
                    'document_id': document.id,
                    'document_name': document.dname
                })

            return document_details
        else:
            print(f"No documents found for type: {document_type}")
            return None

    except Exception as e:
        #print("ERROR ON GET DOCUMENT DETAILS")
        return f"DOCUMENT ERROR FACED, ERROR TYPE: {type(e)}, ERROR: {e}."
def get_document_detailsx(document_type, document_id):
    try:
        # Assuming Documents is your SQLAlchemy model
        documents = Documents.query.filter_by(dtype=document_type).order_by(Documents.id).offset(document_id).limit(2).all()

        if documents:
            # Create a list to store the details of each document
            document_details = []

            for document in documents:
                # Append a dictionary with required details to the list
                document_details.append({
                    'document_id': document.id,
                    'document_name': document.dname
                })

            return document_details
        else:
            print(f"No documents found for type: {document_type}")
            return None

    except Exception as e:
        # Handle exceptions gracefully
        return f"DOCUMENT ERROR FACED, ERROR TYPE: {type(e)}, ERROR: {e}."


# for delete page details getting function
def get_document_details_all():
    try:
        documents = Documents.query.all()

        if documents:
            # Create a list to store the details of each document
            document_details = []
            
            for document in documents:
                # Append a dictionary with required details to the list
                document_details.append({
                    'document_id': document.id,
                    'document_name': document.dname
                })

            return document_details
        else:
            #print(f"No documents found for type: {document_type}")
            return None

    except Exception as e:
        #print("ERROR ON GET DOCUMENT DETAILS")
        return f"DOCUMENT ERROR FACED, ERROR TYPE: {type(e)}, ERROR: {e}."




class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    emailid = db.Column(db.String(30))
    message = db.Column(db.String(1000))

    def __init__(self, emailid, message):
        self.emailid = emailid
        self.message = message

    def __repr__(self):
        return f"{self.emailid} {self.message}"



# STORING A EMAIL PAGES DATAS IN THIS FUNCTION.

def email_store_db(emailid,message):
    try:
        if emailid and message:
            data=Email(emailid=emailid,message=message)
            db.session.add(data)
            db.session.commit()
            return 1
        else:
            return 0
    except Exception as e:
        return f"{type(e).__name__}"

def email_data_db_allget():
    try:
        documents = Email.query.all()
        if documents:
            # Create a list to store the details of each document
            document_details = []
            
            for document in documents:
                # Append a dictionary with required details to the list
                document_details.append({
                    'id': document.id,
                    'emailid': document.emailid,
                    'message': document.message
                })
            return document_details
        else:
            return 8  # This might be a placeholder, adjust it accordingly
    except Exception as e:
        return f"{type(e).__name__}"


def email_del_by_id(id):
    try:
        document = Email.query.get(id)
        #print('DOCUMENT IS : ',document)
        

        if document:
            db.session.delete(document)
            db.session.commit()
            #print("DELETED THE DOCUMENT")
            return "Email Deleted Successfully."
        else:
            return "Email not found."

    except Exception as e:
        #print("ERROR ON DELETE DEmailOCUMENT")
        db.session.rollback()
        return f"Email ERROR FACED, ERROR TYPE: {type(e)}, ERROR: {e}."








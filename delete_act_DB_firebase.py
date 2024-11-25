# delete_functions.py
import firebase_admin
from firebase_admin import credentials, auth
from pymongo import MongoClient

# Firebase setup
# cred = credentials.Certificate('/Users/divyac/Documents/Required_files/conva-ai-stage-firebase-adminsdk-g9mru-0339b9ffc3.json')   #stage
# cred = credentials.Certificate('/Users/divyac/Documents/Required_files/conva-ai-prod-firebase-adminsdk-c8waj-ee0f94b2b7.json')   #prod
# cred = credentials.Certificate('/slang-remote/conva-ai-dev-firebase-adminsdk-vprzs-e8216e066c.json') #dev
# cred = credentials.Certificate('/slang-remote/slang-omni-dev-firebase-adminsdk-e8jqa-500860f5dc.json') #local

# MongoDB setup
# mongo_uri = 'mongodb+srv://slanglabs_stage:ScnvPrL1Ib4Jh4FH@omni-stage-db.glmwhqv.mongodb.net/'   #stage
# mongo_uri = 'mongodb+srv://slanglabs_prod:pvNBhUJk0RxSGQ1W@omni-prod-db.p2alx.mongodb.net/'   #prod
# mongo_uri = 'mongodb+srv://slanglabs_dev:h7pzS6HTISH7fmh8@omni-dev-db.bbdkvrr.mongodb.net' #dev
# mongo_uri = 'mongodb://localhost:27017/?directConnection=true' #local 

def delete_firebase_user_by_email(email, cred_path):
    cred = credentials.Certificate(cred_path)
    try:
        firebase_admin.initialize_app(cred)
        user = auth.get_user_by_email(email)
        uid = user.uid
        # print("user id: ", uid)
        auth.delete_user(uid)
        return 1
    except firebase_admin.auth.UserNotFoundError:
        print(f'User with email: {email} not found')
        return 0
    except Exception as e:
        print(f'Error deleting user with email: {email}', e)
        return 0

def delete_mongo_user(user_id, mongo_uri):
    """
    Delete a user from a specific MongoDB collection based on the user ID.
    
    :param user_id: The unique identifier of the user to delete.
    :param collection_name: The name of the collection from which to delete the user.
    """
    client = MongoClient(mongo_uri)
    db = client['omni']
    collection_name = 'user_metadata'
    collection = db[collection_name]
    result = collection.delete_one({'org_id': user_id})
    if result.deleted_count > 0:
        return 1
    else:
        print('User not found')
        return 0


# delete_firebase_user_by_email("divya36@slanglabs.in", "/Users/divyac/Documents/Required_files/slang-omni-dev-firebase-adminsdk-e8jqa-267a919814.json")
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import firebase_admin
from firebase_admin import credentials, auth, firestore

# Inițializare Firebase
cred = credentials.Certificate('./serviceAccountKey.json')  # Descarcă din Firebase Console
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
CORS(app)  # Permite cereri cross-origin


@app.route('/api/users', methods=['POST'])
def create_user():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No bearer token provided'}), 401

    id_token = auth_header.split('Bearer ')[1]
    try:
        # Add clock tolerance parameter (5 seconds)
        decoded_token = auth.verify_id_token(id_token, check_revoked=True, clock_skew_seconds=5)
        uid = decoded_token['uid']
        email = decoded_token.get('email') or request.json.get('email')

        # Save to Firestore
        db.collection('users').document(uid).set({
            'email': email,
            'createdAt': firestore.SERVER_TIMESTAMP
        })
        return jsonify({'success': True}), 201
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        return jsonify({'error': str(e)}), 401

@app.route('/api/auth/login', methods=['POST'])
def log_login():
    # Verify token and get uid
    id_token = request.headers.get('Authorization', '').split('Bearer ')[1]
    # Add clock tolerance parameter (5 seconds)
    decoded_token = auth.verify_id_token(id_token, check_revoked=True, clock_skew_seconds=5)
    uid = decoded_token['uid']

    # Update last login time
    db.collection('users').document(uid).update({
        'lastLogin': firestore.SERVER_TIMESTAMP
    })

    return jsonify({'success': True})


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    # Verifică token-ul de autentificare
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No bearer token provided'}), 401

    id_token = auth_header.split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Obține task-urile utilizatorului
        tasks_ref = db.collection('tasks')

        tasks = []
        for doc in tasks_ref.stream():
            task_dict = doc.to_dict()
            task_dict['id'] = doc.id
            tasks.append(task_dict)

        return jsonify({'tasks': tasks}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/member_of', methods=['GET'])
def get_memeber_of():
    # Verifică token-ul de autentificare
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No bearer token provided'}), 401

    id_token = auth_header.split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Obține task-urile utilizatorului
        my_task_ref = db.collection('task_members').where('userId', '==', uid)

        my_tasks = []
        for doc in my_task_ref.stream():
            task_dict = doc.to_dict()
            task_dict['id'] = doc.id
            my_tasks.append(task_dict)

        return jsonify({'my_tasks': my_tasks}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/tasks', methods=['POST'])
def create_task():
    id_token = request.headers.get('Authorization', '').split('Bearer ')[1]
    data = request.json

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        task_ref = db.collection('tasks').document()
        task_ref.set({
            'title': data['title'],
            'description': data.get('description', ''),
            'status': 'active',
            'ownerId': uid,
            'createdAt': firestore.SERVER_TIMESTAMP,
        })

        return jsonify({
            'id': task_ref.id,
            'title': data.get('title'),
            'description': data.get('description', ''),
            'status': 'active',
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/join', methods=['POST'])
def join_task():
    id_token = request.headers.get('Authorization', '').split('Bearer ')[1]
    data = request.json
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        task_member_ref = db.collection('task_members').document()
        task_member_ref.set({
            'userId': uid,
            'status': 'pending',
            'taskId': data['taskId']
        })

        return jsonify({
            'status': 'pending',
            'taskId': data['taskId']
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 401

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
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
        tasks_ref = db.collection('tasks').where('userId', '==', uid)

        tasks = []
        for doc in tasks_ref.stream():
            task_dict = doc.to_dict()
            task_dict['id'] = doc.id
            tasks.append(task_dict)

        return jsonify({'tasks': tasks}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/tasks', methods=['POST'])
def create_task():
    # Verifică token-ul de autentificare
    id_token = request.headers.get('Authorization', '').split('Bearer ')[1]
    data = request.json

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Creare task nou
        task_ref = db.collection('tasks').document()
        task_ref.set({
            'title': data.get('title'),
            'completed': False,
            'userId': uid,
            'createdAt': firestore.SERVER_TIMESTAMP
        })

        return jsonify({
            'id': task_ref.id,
            'title': data.get('title'),
            'completed': False
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Verify authentication
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No bearer token provided'}), 401

    try:
        # Verify token
        id_token = auth_header.split('Bearer ')[1]
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Get the task document
        task_ref = db.collection('tasks').document(task_id)
        task = task_ref.get()

        # Check if task exists and belongs to user
        if not task.exists:
            return jsonify({'error': 'Task not found'}), 404
        if task.to_dict().get('userId') != uid:
            return jsonify({'error': 'Unauthorized to delete this task'}), 403

        # Delete the task
        task_ref.delete()
        return jsonify({'success': True}), 200

    except ValueError as e:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
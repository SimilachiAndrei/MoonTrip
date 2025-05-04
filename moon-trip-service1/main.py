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


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        # Creare utilizator în Firebase Auth
        user = auth.create_user(
            email=email,
            password=password
        )

        # Salvare utilizator în Firestore
        db.collection('users').document(user.uid).set({
            'email': email,
            'createdAt': firestore.SERVER_TIMESTAMP
        })

        return jsonify({'success': True, 'uid': user.uid}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    # Verifică token-ul de autentificare
    id_token = request.headers.get('Authorization', '').split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Obține task-urile utilizatorului
        tasks_ref = db.collection('tasks').where('userId', '==', uid)
        tasks = [doc.to_dict() | {'id': doc.id} for doc in tasks_ref.stream()]

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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
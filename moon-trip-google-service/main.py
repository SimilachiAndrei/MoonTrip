from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime

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

@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    # Verify authentication token
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No bearer token provided'}), 401

    id_token = auth_header.split('Bearer ')[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Get the task document
        task_ref = db.collection('tasks').document(task_id)
        task_doc = task_ref.get()

        if not task_doc.exists:
            return jsonify({'error': 'Task not found'}), 404

        task_data = task_doc.to_dict()
        task_data['id'] = task_doc.id

        # Get mini-tasks for this task
        mini_tasks_ref = db.collection('tasks').document(task_id).collection('mini_tasks')
        mini_tasks = []
        for doc in mini_tasks_ref.stream():
            mini_task = doc.to_dict()
            mini_task['id'] = doc.id
            mini_tasks.append(mini_task)

        return jsonify({
            'task': task_data,
            'miniTasks': mini_tasks
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/tasks/<task_id>/mini-tasks', methods=['POST'])
def create_mini_task(task_id):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No bearer token provided'}), 401

    id_token = auth_header.split('Bearer ')[1]
    data = request.json

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Verify task exists
        task_ref = db.collection('tasks').document(task_id)
        task = task_ref.get()
        if not task.exists:
            return jsonify({'error': 'Task not found'}), 404

        # Create mini-task with SERVER_TIMESTAMP for storage
        mini_task_ref = task_ref.collection('mini_tasks').document()
        mini_task_data = {
            'title': data['title'],
            'description': data.get('description', ''),
            'status': data.get('status', 'To Do'),
            'createdBy': uid,
            'createdAt': firestore.SERVER_TIMESTAMP
        }
        mini_task_ref.set(mini_task_data)

        # Return the created mini-task with current timestamp for response
        response_data = {
            'id': mini_task_ref.id,
            'title': data['title'],
            'description': data.get('description', ''),
            'status': data.get('status', 'To Do'),
            'createdBy': uid,
            'createdAt': datetime.now().isoformat()
        }
        return jsonify(response_data), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/tasks/<task_id>/mini-tasks/<mini_task_id>', methods=['PATCH'])
def update_mini_task(task_id, mini_task_id):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No bearer token provided'}), 401

    id_token = auth_header.split('Bearer ')[1]
    data = request.json

    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Update mini-task
        mini_task_ref = db.collection('tasks').document(task_id).collection('mini_tasks').document(mini_task_id)
        mini_task = mini_task_ref.get()
        
        if not mini_task.exists:
            return jsonify({'error': 'Mini-task not found'}), 404

        update_data = {}
        if 'status' in data:
            update_data['status'] = data['status']
        if 'title' in data:
            update_data['title'] = data['title']
        if 'description' in data:
            update_data['description'] = data['description']
        
        update_data['updatedAt'] = firestore.SERVER_TIMESTAMP
        update_data['updatedBy'] = uid
        
        mini_task_ref.update(update_data)

        return jsonify({'success': True}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 401

@app.route('/api/tasks/<task_id>/mini-tasks/<mini_task_id>', methods=['DELETE'])
def delete_mini_task(task_id, mini_task_id):
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Methods'] = 'DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        return response

    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No bearer token provided'}), 401

    id_token = auth_header.split('Bearer ')[1]

    try:
        # Verify the token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Verify task exists
        task_ref = db.collection('tasks').document(task_id)
        task = task_ref.get()
        if not task.exists:
            return jsonify({'error': 'Task not found'}), 404

        # Get mini-task reference
        mini_task_ref = task_ref.collection('mini_tasks').document(mini_task_id)
        mini_task = mini_task_ref.get()

        if not mini_task.exists:
            return jsonify({'error': 'Mini-task not found'}), 404

        # Delete the mini-task
        mini_task_ref.delete()

        response = jsonify({'success': True})
        return response, 200

    except Exception as e:
        print(f"Error deleting mini-task: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Methods'] = 'DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
        return response

    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No bearer token provided'}), 401

    id_token = auth_header.split('Bearer ')[1]

    try:
        # Verify the token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Get task reference
        task_ref = db.collection('tasks').document(task_id)
        task = task_ref.get()

        if not task.exists:
            return jsonify({'error': 'Task not found'}), 404

        # Verify ownership
        task_data = task.to_dict()
        if task_data.get('ownerId') != uid:
            return jsonify({'error': 'Not authorized to delete this task'}), 403

        # Delete all mini-tasks first
        mini_tasks_ref = task_ref.collection('mini_tasks')
        batch = db.batch()
        for mini_task in mini_tasks_ref.stream():
            batch.delete(mini_task.reference)
        batch.commit()

        # Delete task memberships
        memberships_query = db.collection('task_members').where('taskId', '==', task_id)
        batch = db.batch()
        for membership in memberships_query.stream():
            batch.delete(membership.reference)
        batch.commit()

        # Delete the task itself
        task_ref.delete()

        response = jsonify({'success': True})
        return response, 200

    except Exception as e:
        print(f"Error deleting task: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>/pending-users', methods=['GET'])
def get_pending_users(task_id):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No bearer token provided'}), 401

    id_token = auth_header.split('Bearer ')[1]

    try:
        # Verify the token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Verify task exists and user is owner
        task_ref = db.collection('tasks').document(task_id)
        task = task_ref.get()
        if not task.exists:
            return jsonify({'error': 'Task not found'}), 404

        task_data = task.to_dict()
        if task_data.get('ownerId') != uid:
            return jsonify({'error': 'Not authorized to view pending users'}), 403

        # Get pending memberships
        memberships_query = db.collection('task_members').where('taskId', '==', task_id).where('status', '==', 'pending')
        pending_users = []
        
        for membership in memberships_query.stream():
            membership_data = membership.to_dict()
            user_id = membership_data.get('userId')
            if user_id:
                try:
                    user = auth.get_user(user_id)
                    pending_users.append({
                        'id': user_id,
                        'email': user.email,
                        'membershipId': membership.id
                    })
                except:
                    continue

        return jsonify({'pendingUsers': pending_users}), 200

    except Exception as e:
        print(f"Error getting pending users: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<task_id>/user-action', methods=['POST'])
def handle_user_action(task_id):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'error': 'No bearer token provided'}), 401

    id_token = auth_header.split('Bearer ')[1]
    data = request.json

    if not data or 'userId' not in data or 'action' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    if data['action'] not in ['accept', 'reject']:
        return jsonify({'error': 'Invalid action'}), 400

    try:
        # Verify the token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']

        # Verify task exists and user is owner
        task_ref = db.collection('tasks').document(task_id)
        task = task_ref.get()
        if not task.exists:
            return jsonify({'error': 'Task not found'}), 404

        task_data = task.to_dict()
        if task_data.get('ownerId') != uid:
            return jsonify({'error': 'Not authorized to manage users'}), 403

        # Find the membership
        memberships_query = db.collection('task_members').where('taskId', '==', task_id).where('userId', '==', data['userId'])
        memberships = list(memberships_query.stream())
        
        if not memberships:
            return jsonify({'error': 'Membership not found'}), 404

        membership_ref = memberships[0].reference

        if data['action'] == 'accept':
            membership_ref.update({
                'status': 'accepted',
                'updatedAt': firestore.SERVER_TIMESTAMP,
                'updatedBy': uid
            })
        else:  # reject
            membership_ref.delete()

        return jsonify({'success': True}), 200

    except Exception as e:
        print(f"Error handling user action: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
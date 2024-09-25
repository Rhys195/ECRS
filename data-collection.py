def log_user_activity(user_id, action):
    new_log = ActivityLog(user_id=user_id, action=action)
    db.session.add(new_log)
    db.session.commit()


@app.route('/get_activity_log', methods=['GET'])
def get_activity_log():
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'User not logged in'})

    user_id = session['user_id']
    activities = ActivityLog.query.filter_by(user_id=user_id).order_by(ActivityLog.timestamp.desc()).limit(10).all()

    activity_data = []
    for activity in activities:
        activity_data.append({
            'action': activity.action,
            'timestamp': activity.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify({'status': 'success', 'activities': activity_data})

@app.route("sign_up", methods=['POST'])
def sign_up():
    new_user = request.json
    new_user_id = app.database.execute(text("""
        INSERT INTO users(
            name,
            email,
            profile,
            hashed_password
        ) VALEUS (
            :name,
            :email,
            :profile,
            :password
        )
        """), new_user).lastrowid
    
    row = current_app.database.execute(text("""
        SELECT
            id,
            name,
            email,
            profile
        FROM users
        WHERE id = :user_id
        """), {
            'user_id' : new_user_id
        }).fetchone()
    
    created_user = {
        'id'       : row['id'],
        'name'     : row['name'],
        'email'    : row['email'],
        'profile'  : row['profile']
    } if row else None
    
    return jsonify(created_user)
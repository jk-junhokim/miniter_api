# test_endpoints.py

import config
import pytest
import json
import bcrypt

from sqlalchemy import create_engine, text
from app import create_app

database = create_engine(config.test_config['DB_URL'], encoding='utf-8', max_overflow = 0)

@pytest.fixture
def api():
    app = create_app(config.test_config)
    # app.config['TESTING'] = True # Not sure if I should put this here..
    api = app.test_client()
    
    return api


def setup_function():
    ## create a test user
    hashed_password = bcrypt.hashpw('testpassword'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    # hashed_password = hashed_password.decode('utf-8')
    
    
    # TypeError: Unicode-objects must be encoded before hashing
    # ValueError Invalid salt: password must be decoded
    # before being initially stored in the database or it raises a ValueError during "checkpw"
    
    new_users = [
        {
            'id' : 1,
            'name' : 'junho',
            'email' : 'junho@gmail.com',
            'profile' : 'user one test profile',
            'hashed_password' : hashed_password
        }, {
            'id' : 2,
            'name' : 'kevin',
            'email' : 'kevin@gmail.com',
            'profile' : 'user two test profile',
            'hashed_password' : hashed_password
        }
    ]
    
    database.execute(text("""
            INSERT INTO users (
                id,
                name,
                email,
                profile,
                hashed_password
            ) VALUES (
                :id,
                :name,
                :email,
                :profile,
                hashed_password
            )
            """), new_users)
    
    ## create tweet by user 2
    database.execute(text("""
            INSERT INTO tweets (
                user_id,
                tweet
            ) VALUES (
                2,
                "This is PyTest!"
            )
            """))

    
def teardown_function():
    database.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    database.execute(text("TRUNCATE users"))
    database.execute(text("TRUNCATE tweets"))
    database.execute(text("TRUNCATE users_follow_list"))
    database.execute(text("SET FOREIGN_KEY_CHECKS=1"))

##### PASSED #####
"""
def test_ping(api):
    response = api.get("/ping")
    
    assert b'pong' in response.data # response.data is byte type
"""


def test_login(api):
    # password = bcrypt.hashpw(b"test_password", bcrypt.gensalt())
    # password = password.decode('utf-8')
    response = api.post('/login',
                       data = json.dumps({'email' : 'junho@gmail.com',
                                         'password' :  'testpassword'}),
                       content_type = 'application/json'
                       )
    response_json = json.loads(response.data)
    
    assert b"access_token" in response.data
    
    # response_json = json.loads(response.data) # there is no need to decode this
    # access_token = response_json['access_token']
    
    # assert response.status_code == 401
    
    # response_json = json.loads(response.data)
    # if "access_token" in response_json:
    #     access_token = response_json['access_token']
    # else:
    #     access_token = None
    
    # assert access_token 
    # assert "access_token" in response.data
    
    # response_json = json.loads(response.data.decode('utf-8')) # change byte to string type
    # response_json = json.loads(response.data['access_token']) # can handle utf-8 encoded data?
    # access_token = response_json['access_token'] # this variable is byte type
    
    # assert access_token in response.data




"""
def test_unauthorized(api):
    # unauthorized user (without access token) should get 401 error
    response = api.post('/tweet',
                       data = json.dumps({'tweet' : "Hello World"}),
                       content_type = 'application/json'
                       )
    
    assert response.status_code == 401
    
    response = api.post('/follow',
                       data = json.dumps({'follow' : 2}),
                       content_type = 'application/json'
                       )
    
    assert response.status_code == 401
    
    response = api.post('/unfollow',
                       data = json.dumps({'unfollow' : 2}),
                       content_type = 'application/json'
                       )
    
    assert response.status_code == 401
""" 


"""
def test_tweet(api):    
    ## login
    response = api.post('/login',
                        data = json.dumps({'email':'junho@gmail.com',
                                          'password':'testpassword'}),
                       content_type = 'application/json'
                       )
    
    # response_json = json.loads(response.data.decode('utf-8'))
    response_json = json.loads(response.data)
    access_token = response_json['access_token'] # should be string type...
    
    ## tweet
    response = api.post('/tweet',
                       data = json.dumps({'tweet' : "This is PyTest!"}),
                       content_type = 'application/json',
                       headers = {'Authorization' : access_token}
                       )
    
    assert response.status_code == 200
    
    ## check tweet
    response = api.get(f'/timeline/1')
    tweets = json.loads(response.data.decode('utf-8'))
    
    assert response.status_code == 200
    assert tweets == {
        'user_id' : 1,
        'timeline' : [
            {
                'user_id' : 1,
                'tweet' : "This is PyTest!"
            }
        ]
    }
"""


"""    
def test_follow(api):
    ## login
    response = api.post('/login',
                       data = json.dumps({'email':'junho@gmail.com',
                                         'password':'testpassword'}),
                       content_type = 'application/json'
                       )
    response_json = json.loads(response.data.decode('utf-8'))
    access_token = response_json['access_token']
    
    ## check user 1 tweets are empty
    response = api.get(f'/timeline/1')
    tweets = json.loads(response.data.decode('utf-8'))
    
    assert response.status_code == 200
    assert tweets == {
        'user_id' : 1,
        'timeline' : [ ]
    }
    
    ## follow user id = 2
    response = api.post('/follow',
                       data = json.dumps({'id' : 1, 'follow' : 2}),
                       content_type = 'application/json',
                       headers = {'Authorization' : access_token}
                       )
    assert response.status_code == 200
    
    ## check if user 1's tweets include user 2's tweets
    response  = api.get(f'/timeline/1')
    tweets = json.loads(response.data.decode('utf-8'))
    
    assert response.status_code == 200
    assert tweets == {
        'user_id' : 1,
        'timeline' : [
            {
                'user_id' : 2,
                'tweet' : "This is PyTest!"
            }
        ]
    }
"""
    

"""
def test_unfollow(api):
    ## login
    response = api.post('/login',
                       data = json.dumps({'email':'junho@gmail.com',
                                         'password':'testpassword'}),
                       content_type = 'application/json'
                       )
    response_json = json.loads(response.data.decode('utf-8'))
    access_token = response_json['access_token']

    ## follow user 2
    response = api.post('/follow',
                       data = json.dumps({'id' : 1, 'follow' : 2}),
                       content_type = 'application/json',
                       headers = {'Authorization' : access_token}
                       )

    assert response.status_code == 200

    ## check if user 1 follows user 2
    response = api.get('/timeline/1')
    tweets = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert tweets == {
        'user_id' : 1,
        'timeline' : [
            {
                'user_id' : 2,
                'tweet' : "This is PyTest!"
            }
        ]
    }

    ## unfollow user 2
    response = api.post('/unfollow',
                       data = json.dumps({'id' : 1, 'unfollow' : 2}),
                       content_type = 'application/json',
                       headers = {'Authorization' : access_token}
                       )

    assert response.status_code == 200

    ## check if user 2 is no longer on user 1's timeline
    response = api.get(f'/timeline/1')
    tweets = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert tweets == {
        'user_id' : 1,
        'tweets' : [ ]
    }
"""
        
        
        
# index.py is equal to main.py in replit
# print("Hello Python")

from app import *
# from app_book_ver import *


app = create_app()
app.run(host='0.0.0.0', port=5000, debug=True)


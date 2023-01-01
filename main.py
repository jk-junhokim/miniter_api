from app import *
# from app_book_ver import *

from examples import endpoint_setup

app = create_app()
app.run(host='0.0.0.0', port=5000, debug=True)


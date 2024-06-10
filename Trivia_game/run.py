import os
from yourapp import create_app

os.environ['FLASK_APP'] = 'run.py'

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

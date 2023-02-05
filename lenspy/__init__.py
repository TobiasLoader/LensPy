# Change working directory to root of LensPy repo.
# That way opening graphql files & imports is consistent and work as expected (eg. from GraphQlClient.py)
# Same behaviour when running:
# --> /LensPy/test.py | by navigating to LensPy and > python3 testpy
# --> /LensPy/examples/flask-with-lenspy/app.py | by navigating to flask-with-lenspy and > flask run

import os
os.chdir(os.path.dirname(os.path.dirname(__file__)))

# print(os.getcwd())
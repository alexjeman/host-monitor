from apps import create_app

from dotenv import load_dotenv
load_dotenv(verbose=True)

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', ssl_context='adhoc', debug=True)

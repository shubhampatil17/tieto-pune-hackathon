from main import app
import uuid
import thread_settings

if __name__=='__main__':
    thread_settings.setup_bot_thread()
    app.secret_key = str(uuid.uuid4())
    app.run(host='0.0.0.0', debug=True)

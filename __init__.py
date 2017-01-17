from main import *
import uuid
from ml_model import train_machine_learning_models
from database_operations import create_population_dataset
# import thread_settings

if __name__=='__main__':
    # thread_settings.setup_bot_thread()
    train_machine_learning_models()
    create_population_dataset()
    app.secret_key = str(uuid.uuid4())
    app.run(host='0.0.0.0', debug=True, use_reloader = False)
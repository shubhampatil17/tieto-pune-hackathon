# from main import *
import uuid
from ml_model import train_machine_learning_models
from database_operations import create_population_dataset
from premium_calculator import calculate_premium_for_trip
from datetime import datetime
# import thread_settings

trip_plan_dummy = {
    'trip_schedule' : [
        {
            'destination': 'oxford',
            'start_date': datetime(2017, 1, 20)
        },
        {
            'destination': 'cambridge',
            'start_date': datetime(2017, 1, 21)
        },
        {
            'destination': 'perth',
            'start_date': datetime(2017, 1, 23)
        },
        {
            'start_date': datetime(2017, 1, 24) #return
        }
    ],

    'age': 25,
    'marital_status': 'married',
    'trip_cost': 20000,
}


if __name__=='__main__':
    # thread_settings.setup_bot_thread()
    train_machine_learning_models()
    create_population_dataset()
    calculate_premium_for_trip(trip_plan_dummy)
    # app.secret_key = str(uuid.uuid4())
    # app.run(host='0.0.0.0', debug=True, use_reloader = False)
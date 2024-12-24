#from track_performance.email_tasks import app as task_app
from track_performance.email_check_in import app as check_in_app
import subprocess

if __name__ == '__main__':
    #task_app.run(host='0.0.0.0', port=5000, debug=True)
    check_in_app.run(host='0.0.0.0', port=5001, debug=True)

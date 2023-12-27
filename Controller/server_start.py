import subprocess
import time
import os
# List of tuples containing folder and app script
apps = [
    ("User", "user.py", "5000"),
    ("Client", "client.py", "5001"),
    
]

# Start Flask servers in separate processes
processes = []
for folder, app, port in apps:
    folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),folder)
    print(folder_path)
    app_path = os.path.join(folder_path, app)
    cmd = 'start cmd /k "conda activate engage && flask --app {} --debug run -h localhost -p {}"'.format(app,port)

    #flask --app example_app.py --debug run

    process = subprocess.Popen(cmd, shell=True, cwd=folder_path)
    processes.append(process)
    time.sleep(2)  # Add a delay to ensure each server starts before the next one

try:
    # Keep the main process alive to allow servers to run
    while True:
        pass
except KeyboardInterrupt:
    # Terminate all subprocesses on keyboard interrupt
    for process in processes:
        process.terminate()

import subprocess
import logging

def install():
    try:
        venv_activate_script = r'virt\Scripts\activate'
        command = f'python -m venv virt && {venv_activate_script} && pip install -r requirements.txt'
        # Execute the command in a single subprocess call
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, text=True)
        print(result.stdout)
        print("Installation Complete")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred: {e}")
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    install()

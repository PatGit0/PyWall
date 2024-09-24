import subprocess
import os

gen_family="inet"

def run_nft_command(command):
    _script_path = os.path.join(os.getcwd(), "scripts", "run_nft_commands.sh")
    try:
        result=subprocess.run(["sudo", _script_path] + command , check=True, stdout=subprocess.PIPE)
        return (result.stdout.decode())

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {' '.join(command)}")
        print(e)
def copy_stdout_nft_command(command, file):
    _script_path = os.path.join(os.getcwd(), "scripts", "run_nft_commands.sh")
    try:
        result=subprocess.run(["sudo", _script_path] + command , check=True, stdout=subprocess.PIPE)
        print(f"Salida de result: "+result.stdout.decode())
        with open(file, 'w') as f:
            f.write(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {' '.join(command)}")
        print(e)

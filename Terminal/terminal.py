import subprocess
from concurrent.futures import ThreadPoolExecutor

def ejecutar_comando(comando):
    try:
        subprocess.run(comando, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar '{comando}': {e}")

comandos = ["roscore", "rosrun turtlesim turtlesim_node"]

with ThreadPoolExecutor() as executor:
    resultados = list(executor.map(ejecutar_comando, comandos))

# Los comandos se ejecutarán en paralelo

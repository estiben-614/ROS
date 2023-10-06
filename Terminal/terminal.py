import subprocess

# Comando que deseas ejecutar en la terminal (por ejemplo, abrir una terminal)

#Comando para Abrir terminal
#comando = "gnome-terminal"  # Cambia esto según tu terminal y sistema operativo

#Comando para crear carpeta
comando = "mkdir pruebita"

#Comando para correr ROSCORE
comando = "roscore"
# Ejecuta el comando
subprocess.call(comando, shell=True)


# Otra forma de levantar roscore
#subprocess.run(["roscore"])


# Correr script con python terminal.py
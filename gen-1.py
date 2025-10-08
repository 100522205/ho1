#!/usr/bin/env python3
import os
import sys
import re

# --- Comprobación de argumentos ---
if len(sys.argv) != 3:
    print("Uso: ./gen-1.py <fichero-entrada> <fichero-salida>")
    sys.exit(1)

entrada = sys.argv[1]
salida = sys.argv[2]

# --- Lectura del fichero de entrada ---
# Formato esperado:
# n m
# kd kp
# d1 d2 ... dm
# p1 p2 ... pm

with open(entrada, "r") as f:
    lineas = [line.strip() for line in f.readlines() if line.strip()]

n, m = map(int, lineas[0].split())
kd, kp = map(int, lineas[1].split())
distancias = list(map(int, lineas[2].split()))
pasajeros = list(map(int, lineas[3].split()))

# --- Generación del fichero .dat ---
with open(salida, "w") as f:
    f.write("data;\n\n")

    # Conjuntos
    f.write("set BUSES   := " + " ".join([f"{i+1:02d}" for i in range(m)]) + ";\n")
    # Se vería así: set BUSES := 01 02 03 ... 0m;
    f.write("set FRANJAS := " + " ".join([f"{i+1:02d}" for i in range(n)]) + ";\n\n")
    # Se vería así: set FRANJAS := 01 02 03 ... 0n;

    # Parámetros

    f.write(f"param kd := {kd};\n")
    f.write(f"param kp := {kp};\n\n")

    # param Distancia :=
    # 01 d1
    # 02 d2
    # ...
    # 0m dm
    # ;
    f.write("param Distancia :=\n")
    for i in range(m):
        f.write(f"{i+1:02d} {distancias[i]}\n")
    f.write(";\n\n")

    # param Pasajeros :=
    # 01 p1
    # 02 p2
    # ...
    # 0m pm
    # ;
    f.write("param Pasajeros :=\n")
    for i in range(m):
        f.write(f"{i+1:02d} {pasajeros[i]}\n")
    f.write(";\n\n")

    f.write("end;\n")

print(f"Fichero de datos generado correctamente: {salida}")

# --- Ejecución del modelo con GLPK ---
# Se asume que glpsol está en el PATH del sistema
comando = f'glpsol -m parte-2-1.mod -d "{salida}" -o output.txt'
print(f"Ejecutando: {comando}\n")
os.system(comando)
print("\n")

# Ahora mostramos en pantalla el contenido que se pide en el enunciado
with open("output.txt", "r") as f:
    output = f.readlines()

asignados = []
no_asignados = []
for linea in output:
    if "Objective" in linea:
        objetivo = linea.strip()
    if "Rows" in linea:
        variables = "Nº variables de decisión o " + linea.strip()
    if "Columns" in linea:
        restricciones = "Nº restricciones o " + linea.strip()
    # Buscar variables asignadas: +++ x[i, j]  *  1  ++++
    # ...
    # Buscar variables no asignadas: +++ y[i] * 1 +++
    # ...

print(objetivo + "\n")
print(variables + "\n")
print(restricciones + "\n")
print("Buses asignados a franjas horarias:\n")
# ...

# Como usar gen-1.py desde terminal de VSCode: Camino a python.exe/python.exe camino a gen-1.py/gen-1.py datos.in data_model.dat
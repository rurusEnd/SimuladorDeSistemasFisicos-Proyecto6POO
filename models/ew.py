from collections import deque

estudiantes = ["Ana", "Luis", "Pedro", "Rosa", "Carlos"]

documentos = []
documentos.append("Constancia de matricula")
documentos.append("Solicitud de carne")
documentos.append("Ficha socioeconómica")

cola_atencion = deque(["Ana", "Luis", "Pedro"])

print(" --- ESTADO INICIAL --- ")
print("Estudiantes registrados (Lista):", estudiantes)
print("Documentos en mesa (Pila):", documentos)
print("Estudiantes en espera (Cola):", list(cola_atencion))

doc_revisado = documentos.pop()
estudiante_atendido = cola_atencion.popleft() # Atiende al primer estudiante de la fila
cola_atencion.append("Rosa")

print("\n --- DESPUÉS DE OPERACIONES --- ")
print("Documento revisado (pop):", doc_revisado)
print("Documentos restantes en pila:", documentos)
print("Estudiante atendido (popleft):", estudiante_atendido)

print("Cola actualizada:", list(cola_atencion))

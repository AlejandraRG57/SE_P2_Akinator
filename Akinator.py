import pickle
import tkinter as tk
from tkinter import simpledialog, messagebox

class Nodo:
    def __init__(self, pregunta=None, personaje=None):
        self.pregunta = pregunta
        self.personaje = personaje
        self.si = None
        self.no = None

class AdivinaQuien:
    def __init__(self, archivo='personajes.b'):
        self.archivo = archivo
        self.raiz = None
        self.cargar_datos()
        
        # Configuración de la ventana principal de Tkinter
        self.root = tk.Tk()
        self.root.title("Adivina Quién")
        self.root.geometry("400x200")
        
        # Widgets de interfaz
        self.pregunta_label = tk.Label(self.root, text="", wraplength=300)
        self.pregunta_label.pack(pady=20)
        self.si_button = tk.Button(self.root, text="Sí", command=self.responder_si)
        self.no_button = tk.Button(self.root, text="No", command=self.responder_no)
        self.si_button.pack(side=tk.LEFT, padx=20)
        self.no_button.pack(side=tk.RIGHT, padx=20)

        # Nodo actual para el juego
        self.nodo_actual = self.raiz
        self.mostrar_pregunta()

    def cargar_datos(self):
        try:
            with open(self.archivo, 'rb') as f:
                self.raiz = pickle.load(f)
            print("Datos cargados exitosamente.")
        except FileNotFoundError:
            self.raiz = Nodo("¿Es mujer?")
            nodo_pelo_pelirojo = Nodo("¿Tiene el pelo pelirojo?")
            nodo_gafas = Nodo("¿Usa gafas?")
            nodo_personaje1 = Nodo(personaje="Skye")
            nodo_personaje2 = Nodo(personaje="Chamber")
            nodo_personaje3 = Nodo(personaje="Phoenix")
            nodo_personaje4 = Nodo(personaje="Sage")

            self.raiz.si = nodo_pelo_pelirojo
            self.raiz.no = nodo_gafas

            nodo_pelo_pelirojo.si = nodo_personaje1
            nodo_pelo_pelirojo.no = nodo_personaje4

            nodo_gafas.si = nodo_personaje2
            nodo_gafas.no = nodo_personaje3

            print("Archivo no encontrado, creando un árbol inicial con preguntas básicas.")

    def guardar_datos(self):
        with open(self.archivo, 'wb') as f:
            pickle.dump(self.raiz, f)
        print("Datos guardados exitosamente.")

    def mostrar_pregunta(self):
        if self.nodo_actual.personaje:
            self.pregunta_label.config(text=f"¿El personaje es {self.nodo_actual.personaje}?")
        else:
            self.pregunta_label.config(text=self.nodo_actual.pregunta)

    def responder_si(self):
        if self.nodo_actual.personaje:
            messagebox.showinfo("Resultado", "¡He adivinado el personaje!")
            self.root.quit()
        else:
            self.nodo_actual = self.nodo_actual.si
            self.mostrar_pregunta()

    def responder_no(self):
        if self.nodo_actual.personaje:
            self.aprender_nuevo_personaje(self.nodo_actual)
        else:
            self.nodo_actual = self.nodo_actual.no
            self.mostrar_pregunta()

    def aprender_nuevo_personaje(self, nodo_incorrecto):
        nombre_nuevo = simpledialog.askstring("Nuevo personaje", "No conozco este personaje. ¿Cuál es su nombre?")
        nueva_pregunta = simpledialog.askstring("Nueva pregunta", f"¿Qué pregunta distinguiría a {nombre_nuevo} de {nodo_incorrecto.personaje}?")
        respuesta_nuevo = messagebox.askyesno("Nueva pregunta", f"Si la respuesta a '{nueva_pregunta}' es 'sí', ¿el personaje es {nombre_nuevo}?")

        nuevo_personaje = Nodo(personaje=nombre_nuevo)
        nueva_pregunta_nodo = Nodo(pregunta=nueva_pregunta)
        
        if respuesta_nuevo:
            nueva_pregunta_nodo.si = nuevo_personaje
            nueva_pregunta_nodo.no = nodo_incorrecto
        else:
            nueva_pregunta_nodo.si = nodo_incorrecto
            nueva_pregunta_nodo.no = nuevo_personaje

        if self.raiz == nodo_incorrecto:
            self.raiz = nueva_pregunta_nodo
        else:
            self.reemplazar_nodo(self.raiz, nodo_incorrecto, nueva_pregunta_nodo)

        self.guardar_datos()
        messagebox.showinfo("Información", "Nuevo personaje y pregunta añadidos exitosamente.")
        self.root.quit()

    def reemplazar_nodo(self, nodo_actual, nodo_incorrecto, nodo_nuevo):
        if nodo_actual.si == nodo_incorrecto:
            nodo_actual.si = nodo_nuevo
        elif nodo_actual.no == nodo_incorrecto:
            nodo_actual.no = nodo_nuevo
        else:
            if nodo_actual.si:
                self.reemplazar_nodo(nodo_actual.si, nodo_incorrecto, nodo_nuevo)
            if nodo_actual.no:
                self.reemplazar_nodo(nodo_actual.no, nodo_incorrecto, nodo_nuevo)

    def iniciar_juego(self):
        self.root.mainloop()

# Ejemplo de uso
juego = AdivinaQuien()
juego.iniciar_juego()

import sqlite3
import customtkinter as ctk
from tkinter import messagebox
def run():
        

    # Configurar apariencia
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Crear o conectar a la base de datos
    conn = sqlite3.connect("mi_base.db")
    cursor = conn.cursor()

    # Crear tabla de ejemplo
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER NOT NULL
    )
    """)
    conn.commit()

    # Insertar datos de ejemplo si está vacío
    cursor.execute("SELECT COUNT(*) FROM personas")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO personas (nombre, edad) VALUES (?, ?)", [
            ("Juan", 30),
            ("María", 25),
            ("Luis", 40)
        ])
        conn.commit()


    class App(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("Editor de SQLite con CustomTkinter")
            self.geometry("600x400")

            self.records_listbox = ctk.CTkTextbox(self, width=580, height=200)
            self.records_listbox.pack(pady=10)

            self.load_data()

            self.id_entry = ctk.CTkEntry(self, placeholder_text="ID")
            self.id_entry.pack(pady=5)

            self.name_entry = ctk.CTkEntry(self, placeholder_text="Nombre")
            self.name_entry.pack(pady=5)

            self.age_entry = ctk.CTkEntry(self, placeholder_text="Edad")
            self.age_entry.pack(pady=5)

            self.update_button = ctk.CTkButton(self, text="Actualizar", command=self.update_record)
            self.update_button.pack(pady=10)

        def load_data(self):
            self.records_listbox.delete("1.0", ctk.END)
            cursor.execute("SELECT * FROM personas")
            rows = cursor.fetchall()
            for row in rows:
                self.records_listbox.insert(ctk.END, f"ID: {row[0]} | Nombre: {row[1]} | Edad: {row[2]}\n")

        def update_record(self):
            try:
                id_val = int(self.id_entry.get())
                name_val = self.name_entry.get()
                age_val = int(self.age_entry.get())
                cursor.execute("UPDATE personas SET nombre = ?, edad = ? WHERE id = ?", (name_val, age_val, id_val))
                conn.commit()
                self.load_data()
                messagebox.showinfo("Éxito", "Registro actualizado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar: {e}")


    if __name__ == "__main__":
        app = App()
        app.mainloop()

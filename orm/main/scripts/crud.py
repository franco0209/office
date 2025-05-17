import customtkinter as ctk

from main.models import Empresa

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class EmpresaCRUDApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Empresas")
        self.geometry("900x550")
        self.resizable(False, False)

        self.configure(bg="#2a2d2e")

        # ====== Layout con Tabs (futuro: más modelos) ======
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=20)
        self.empresa_tab = self.tabs.add("Empresas")

        self.crear_interfaz_empresa()

    def crear_interfaz_empresa(self):
        frame = ctk.CTkFrame(self.empresa_tab)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        # ------- Formulario -------
        form = ctk.CTkFrame(frame, width=300)
        form.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(form, text="CRUD de Empresa", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 20))

        self.entry_key = ctk.CTkEntry(form, placeholder_text="Clave única")
        self.entry_key.pack(pady=10, fill="x", padx=10)

        self.entry_nombre = ctk.CTkEntry(form, placeholder_text="Nombre de la empresa")
        self.entry_nombre.pack(pady=10, fill="x", padx=10)

        self.entry_tipo = ctk.CTkEntry(form, placeholder_text="Tipo de ticket")
        self.entry_tipo.pack(pady=10, fill="x", padx=10)

        self.label_feedback = ctk.CTkLabel(form, text="", text_color="white")
        self.label_feedback.pack(pady=5)

        # Botones
        self.btn_add = ctk.CTkButton(form, text="Agregar", command=self.agregar_empresa)
        self.btn_add.pack(pady=(15, 5), fill="x", padx=20)

        self.btn_update = ctk.CTkButton(form, text="Actualizar", command=self.actualizar_empresa)
        self.btn_update.pack(pady=5, fill="x", padx=20)

        self.btn_delete = ctk.CTkButton(form, text="Eliminar", command=self.eliminar_empresa)
        self.btn_delete.pack(pady=5, fill="x", padx=20)

        self.btn_clear = ctk.CTkButton(form, text="Limpiar campos", command=self.limpiar_formulario)
        self.btn_clear.pack(pady=(10, 0), fill="x", padx=20)

        # ------- Listado de empresas -------
        lista_frame = ctk.CTkFrame(frame)
        lista_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(lista_frame, text="Empresas registradas", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)

        self.scroll_frame = ctk.CTkScrollableFrame(lista_frame, width=500, height=400)
        self.scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.mostrar_empresas()

    def limpiar_formulario(self):
        self.entry_key.delete(0, 'end')
        self.entry_nombre.delete(0, 'end')
        self.entry_tipo.delete(0, 'end')
        self.label_feedback.configure(text="Campos limpiados ✅", text_color="lightgreen")

    def mostrar_empresas(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        empresas = Empresa.objects.all().order_by("nombre")
        if empresas.exists():
            for emp in empresas:
                label = ctk.CTkLabel(self.scroll_frame, text=f"🟦 {emp.key} | {emp.nombre} | {emp.tipoTicket}",
                                     anchor="w", font=ctk.CTkFont(size=13))
                label.pack(fill="x", pady=2, padx=5)
        else:
            ctk.CTkLabel(self.scroll_frame, text="No hay empresas registradas.",
                         font=ctk.CTkFont(size=13)).pack(pady=10)

    def agregar_empresa(self):
        key = self.entry_key.get().strip()
        nombre = self.entry_nombre.get().strip()
        tipo = self.entry_tipo.get().strip()

        if not key or not nombre or not tipo:
            self.label_feedback.configure(text="❌ Todos los campos son obligatorios.", text_color="red")
            return

        try:
            Empresa.objects.create(key=key, nombre=nombre, tipoTicket=tipo)
            self.label_feedback.configure(text="✅ Empresa agregada exitosamente.", text_color="lightgreen")
            self.mostrar_empresas()
            self.limpiar_formulario()
        except Exception as e:
            self.label_feedback.configure(text=f"❌ Error al crear: {e}", text_color="red")

    def actualizar_empresa(self):
        key = self.entry_key.get().strip()
        nombre = self.entry_nombre.get().strip()
        tipo = self.entry_tipo.get().strip()

        try:
            emp = Empresa.objects.get(key=key)
            emp.nombre = nombre
            emp.tipoTicket = tipo
            emp.save()
            self.label_feedback.configure(text="✅ Empresa actualizada.", text_color="lightgreen")
            self.mostrar_empresas()
        except Empresa.DoesNotExist:
            self.label_feedback.configure(text="❌ Empresa no encontrada.", text_color="red")
        except Exception as e:
            self.label_feedback.configure(text=f"❌ Error: {e}", text_color="red")

    def eliminar_empresa(self):
        key = self.entry_key.get().strip()
        try:
            emp = Empresa.objects.get(key=key)
            emp.delete()
            self.label_feedback.configure(text="🗑️ Empresa eliminada.", text_color="orange")
            self.mostrar_empresas()
            self.limpiar_formulario()
        except Empresa.DoesNotExist:
            self.label_feedback.configure(text="❌ Empresa no encontrada.", text_color="red")
        except Exception as e:
            self.label_feedback.configure(text=f"❌ Error: {e}", text_color="red")


# ==== Método para ejecutar la aplicación ====
def run():
    app = EmpresaCRUDApp()
    app.mainloop()

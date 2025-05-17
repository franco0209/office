import customtkinter as ctk
from tkinter import messagebox
from main.models import Empresa
from django.core.exceptions import ValidationError

class EmpresaCRUDApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Empresas - Mejorado")
        self.geometry("1000x600")
        self.minsize(900, 550)
        
        # Configuración de tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Variables de estado
        self.empresa_seleccionada = None
        
        # Crear interfaz
        self._crear_widgets()
        self._configurar_layout()
        self.actualizar_lista_empresas()
        
    def _crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Panel de pestañas
        self.tabs = ctk.CTkTabview(self)
        self.empresa_tab = self.tabs.add("Empresas")
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.empresa_tab)
        
        # Panel de formulario
        self.form_frame = ctk.CTkFrame(self.main_frame, width=350)
        self._crear_formulario()
        
        # Panel de lista
        self.list_frame = ctk.CTkFrame(self.main_frame)
        self._crear_lista_empresas()
        
    def _configurar_layout(self):
        """Configura el layout de los widgets"""
        self.tabs.pack(fill="both", expand=True, padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.form_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.list_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
    def _crear_formulario(self):
        """Crea el formulario de empresa"""
        # Título
        ctk.CTkLabel(
            self.form_frame, 
            text="Datos de la Empresa", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(10, 20))
        
        # Campos del formulario
        self.form_fields = {}
        fields = [
            ("key", "Clave única", True),
            ("nombre", "Nombre de la empresa", True),
            ("tipoTicket", "Tipo de ticket", True),

        ]
        
        for field, placeholder, required in fields:
            frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            frame.pack(fill="x", padx=10, pady=5)
            
            label = ctk.CTkLabel(frame, text=f"{placeholder}{'*' if required else ''}:")
            label.pack(anchor="w")
            
            entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
            entry.pack(fill="x")
            
            self.form_fields[field] = entry
        
        # Feedback
        self.feedback_label = ctk.CTkLabel(
            self.form_frame, 
            text="", 
            text_color="gray",
            wraplength=300
        )
        self.feedback_label.pack(pady=10)
        
        # Botones
        btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        self.btn_add = ctk.CTkButton(
            btn_frame, 
            text="Agregar", 
            command=self.agregar_empresa,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.btn_add.pack(side="left", expand=True, padx=5)
        
        self.btn_update = ctk.CTkButton(
            btn_frame, 
            text="Actualizar", 
            command=self.actualizar_empresa,
            state="disabled"
        )
        self.btn_update.pack(side="left", expand=True, padx=5)
        
        self.btn_delete = ctk.CTkButton(
            btn_frame, 
            text="Eliminar", 
            command=self.eliminar_empresa,
            fg_color="red",
            hover_color="darkred",
            state="disabled"
        )
        self.btn_delete.pack(side="left", expand=True, padx=5)
        
        self.btn_clear = ctk.CTkButton(
            btn_frame, 
            text="Limpiar", 
            command=self.limpiar_formulario
        )
        self.btn_clear.pack(side="left", expand=True, padx=5)
        
    def _crear_lista_empresas(self):
        """Crea el panel de lista de empresas"""
        # Barra de búsqueda
        search_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Buscar empresas..."
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.search_entry.bind("<KeyRelease>", self.buscar_empresas)
        
        ctk.CTkButton(
            search_frame, 
            text="Buscar", 
            width=80,
            command=self.buscar_empresas
        ).pack(side="left")
        
        # Lista de empresas
        self.lista_empresas = ctk.CTkScrollableFrame(
            self.list_frame, 
            height=400
        )
        self.lista_empresas.pack(fill="both", expand=True, padx=10, pady=10)
        
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.empresa_seleccionada = None
        for entry in self.form_fields.values():
            entry.delete(0, 'end')
        
        self.btn_add.configure(state="normal")
        self.btn_update.configure(state="disabled")
        self.btn_delete.configure(state="disabled")
        self.mostrar_feedback("Formulario limpiado", "info")
        
    def mostrar_feedback(self, mensaje, tipo="info"):
        """Muestra mensajes de feedback al usuario"""
        colors = {
            "info": "gray",
            "success": "lightgreen",
            "error": "red",
            "warning": "orange"
        }
        self.feedback_label.configure(text=mensaje, text_color=colors.get(tipo, "gray"))
        
    def obtener_datos_formulario(self):
        """Obtiene y valida los datos del formulario"""
        datos = {}
        required_fields = ["key", "nombre", "tipoTicket"]
        
        for field, entry in self.form_fields.items():
            value = entry.get().strip()
            if field in required_fields and not value:
                raise ValueError(f"El campo '{field}' es obligatorio")
            datos[field] = value if value else None
        
        return datos
    
    def actualizar_lista_empresas(self, empresas=None):
        """Actualiza la lista de empresas mostrada"""
        # Limpiar lista actual
        for widget in self.lista_empresas.winfo_children():
            widget.destroy()
        
        # Obtener empresas si no se proporcionan
        if empresas is None:
            empresas = Empresa.objects.all().order_by("nombre")
        
        if not empresas.exists():
            ctk.CTkLabel(
                self.lista_empresas, 
                text="No hay empresas registradas.",
                font=ctk.CTkFont(size=13)
            ).pack(pady=20)
            return
        
        # Mostrar cada empresa
        for emp in empresas:
            frame = ctk.CTkFrame(self.lista_empresas, height=40)
            frame.pack(fill="x", pady=2, padx=5)
            
            # Mostrar información
            ctk.CTkLabel(
                frame, 
                text=f"{emp.key} - {emp.nombre}",
                anchor="w",
                font=ctk.CTkFont(size=13)
            ).pack(side="left", fill="x", expand=True, padx=10)
            
            # Botón para seleccionar
            ctk.CTkButton(
                frame, 
                text="Seleccionar", 
                width=80,
                command=lambda e=emp: self.cargar_empresa(e)
            ).pack(side="right", padx=5)
    
    def cargar_empresa(self, empresa):
        """Carga los datos de una empresa en el formulario"""
        self.empresa_seleccionada = empresa
        
        for field, entry in self.form_fields.items():
            value = getattr(empresa, field, "")
            entry.delete(0, 'end')
            entry.insert(0, str(value) if value else "")
        
        self.btn_add.configure(state="disabled")
        self.btn_update.configure(state="normal")
        self.btn_delete.configure(state="normal")
        self.mostrar_feedback(f"Cargada empresa: {empresa.nombre}", "info")
    
    def buscar_empresas(self, event=None):
        """Busca empresas según el texto ingresado"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            self.actualizar_lista_empresas()
            return
        
        empresas = Empresa.objects.filter(
            nombre__icontains=search_term
        ).order_by("nombre")
        
        self.actualizar_lista_empresas(empresas)
    
    def agregar_empresa(self):
        """Agrega una nueva empresa"""
        try:
            datos = self.obtener_datos_formulario()
            
            # Verificar si ya existe
            if Empresa.objects.filter(key=datos["key"]).exists():
                raise ValidationError("Ya existe una empresa con esta clave")
            
            # Crear nueva empresa
            Empresa.objects.create(**datos)
            
            self.mostrar_feedback("✅ Empresa agregada exitosamente", "success")
            self.limpiar_formulario()
            self.actualizar_lista_empresas()
            
        except Exception as e:
            self.mostrar_feedback(f"❌ Error: {str(e)}", "error")
    
    def actualizar_empresa(self):
        """Actualiza la empresa seleccionada"""
        if not self.empresa_seleccionada:
            self.mostrar_feedback("No hay empresa seleccionada", "error")
            return
            
        try:
            datos = self.obtener_datos_formulario()
            
            # Actualizar empresa
            for field, value in datos.items():
                setattr(self.empresa_seleccionada, field, value)
            
            self.empresa_seleccionada.save()
            
            self.mostrar_feedback("✅ Empresa actualizada exitosamente", "success")
            self.limpiar_formulario()
            self.actualizar_lista_empresas()
            
        except Exception as e:
            self.mostrar_feedback(f"❌ Error: {str(e)}", "error")
    
    def eliminar_empresa(self):
        """Elimina la empresa seleccionada"""
        if not self.empresa_seleccionada:
            self.mostrar_feedback("No hay empresa seleccionada", "error")
            return
            
        # Confirmación antes de eliminar
        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar la empresa {self.empresa_seleccionada.nombre}?"
        ):
            return
            
        try:
            nombre = self.empresa_seleccionada.nombre
            self.empresa_seleccionada.delete()
            
            self.mostrar_feedback(f"🗑️ Empresa '{nombre}' eliminada", "warning")
            self.limpiar_formulario()
            self.actualizar_lista_empresas()
            
        except Exception as e:
            self.mostrar_feedback(f"❌ Error al eliminar: {str(e)}", "error")

def run():
    app = EmpresaCRUDApp()
    app.mainloop()
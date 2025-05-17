import customtkinter as ctk
from tkinter import messagebox
from main.models import Empresa, Cuenta
from django.core.exceptions import ValidationError

class GestorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión Completa - Empresas y Cuentas")
        self.geometry("1100x650")
        self.minsize(1000, 600)
        
        # Configuración de tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Variables de estado
        self.empresa_seleccionada = None
        self.cuenta_seleccionada = None
        
        # Crear interfaz
        self._crear_widgets()
        self._configurar_layout()
        
        # Cargar datos iniciales
        self.actualizar_lista_empresas()
        self.actualizar_lista_cuentas()
        
    def _crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Panel de pestañas principales
        self.tabs = ctk.CTkTabview(self)
        self.empresa_tab = self.tabs.add("Empresas")
        self.cuenta_tab = self.tabs.add("Cuentas")
        
        # ========== Pestaña de Empresas ==========
        self.empresa_main_frame = ctk.CTkFrame(self.empresa_tab)
        self._crear_formulario_empresa()
        self._crear_lista_empresas()
        
        # ========== Pestaña de Cuentas ==========
        self.cuenta_main_frame = ctk.CTkFrame(self.cuenta_tab)
        self._crear_formulario_cuenta()
        self._crear_lista_cuentas()
        
    def _configurar_layout(self):
        """Configura el layout de los widgets"""
        self.tabs.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Layout pestaña Empresas
        self.empresa_main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.empresa_form_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.empresa_list_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Layout pestaña Cuentas
        self.cuenta_main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.cuenta_form_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.cuenta_list_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    
    # =============================================
    # SECCIÓN EMPRESAS
    # =============================================
    
    def _crear_formulario_empresa(self):
        """Crea el formulario de empresa"""
        self.empresa_form_frame = ctk.CTkFrame(self.empresa_main_frame, width=350)
        
        # Título
        ctk.CTkLabel(
            self.empresa_form_frame, 
            text="Datos de la Empresa", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(10, 20))
        
        # Campos del formulario
        self.empresa_fields = {}
        fields = [
            ("key", "Clave única", True),
            ("nombre", "Nombre de la empresa", True),
            ("tipoTicket", "Tipo de ticket", True),
            ("direccion", "Dirección", False),
            ("telefono", "Teléfono", False)
        ]
        
        for field, placeholder, required in fields:
            frame = ctk.CTkFrame(self.empresa_form_frame, fg_color="transparent")
            frame.pack(fill="x", padx=10, pady=5)
            
            label = ctk.CTkLabel(frame, text=f"{placeholder}{'*' if required else ''}:")
            label.pack(anchor="w")
            
            entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
            entry.pack(fill="x")
            
            self.empresa_fields[field] = entry
        
        # Feedback
        self.empresa_feedback = ctk.CTkLabel(
            self.empresa_form_frame, 
            text="", 
            text_color="gray",
            wraplength=300
        )
        self.empresa_feedback.pack(pady=10)
        
        # Botones
        btn_frame = ctk.CTkFrame(self.empresa_form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        self.empresa_btn_add = ctk.CTkButton(
            btn_frame, 
            text="Agregar", 
            command=self.agregar_empresa,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.empresa_btn_add.pack(side="left", expand=True, padx=5)
        
        self.empresa_btn_update = ctk.CTkButton(
            btn_frame, 
            text="Actualizar", 
            command=self.actualizar_empresa,
            state="disabled"
        )
        self.empresa_btn_update.pack(side="left", expand=True, padx=5)
        
        self.empresa_btn_delete = ctk.CTkButton(
            btn_frame, 
            text="Eliminar", 
            command=self.eliminar_empresa,
            fg_color="red",
            hover_color="darkred",
            state="disabled"
        )
        self.empresa_btn_delete.pack(side="left", expand=True, padx=5)
        
        self.empresa_btn_clear = ctk.CTkButton(
            btn_frame, 
            text="Limpiar", 
            command=lambda: self.limpiar_formulario('empresa')
        )
        self.empresa_btn_clear.pack(side="left", expand=True, padx=5)
    
    def _crear_lista_empresas(self):
        """Crea el panel de lista de empresas"""
        self.empresa_list_frame = ctk.CTkFrame(self.empresa_main_frame)
        
        # Barra de búsqueda
        search_frame = ctk.CTkFrame(self.empresa_list_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.empresa_search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Buscar empresas..."
        )
        self.empresa_search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.empresa_search_entry.bind("<KeyRelease>", self.buscar_empresas)
        
        ctk.CTkButton(
            search_frame, 
            text="Buscar", 
            width=80,
            command=self.buscar_empresas
        ).pack(side="left")
        
        # Lista de empresas
        self.empresa_lista = ctk.CTkScrollableFrame(
            self.empresa_list_frame, 
            height=400
        )
        self.empresa_lista.pack(fill="both", expand=True, padx=10, pady=10)
    
    # =============================================
    # SECCIÓN CUENTAS
    # =============================================
    
    def _crear_formulario_cuenta(self):
        """Crea el formulario de cuenta"""
        self.cuenta_form_frame = ctk.CTkFrame(self.cuenta_main_frame, width=350)
        
        # Título
        ctk.CTkLabel(
            self.cuenta_form_frame, 
            text="Datos de la Cuenta", 
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(10, 20))
        
        # Campos del formulario
        self.cuenta_fields = {}
        fields = [
            ("key", "Clave única", True),
            ("empresa", "Empresa", True),
            ("nombre", "Nombre de la cuenta", True),
            ("referencias", "Referencias", False)
        ]
        
        for field, placeholder, required in fields:
            frame = ctk.CTkFrame(self.cuenta_form_frame, fg_color="transparent")
            frame.pack(fill="x", padx=10, pady=5)
            
            label = ctk.CTkLabel(frame, text=f"{placeholder}{'*' if required else ''}:")
            label.pack(anchor="w")
            
            if field == "empresa":
                # Combobox para seleccionar empresa
                self.empresa_combobox = ctk.CTkComboBox(frame, state="readonly")
                self.empresa_combobox.pack(fill="x")
                self.cuenta_fields[field] = self.empresa_combobox
                self.actualizar_combobox_empresas()
            else:
                entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
                entry.pack(fill="x")
                self.cuenta_fields[field] = entry
        
        # Feedback
        self.cuenta_feedback = ctk.CTkLabel(
            self.cuenta_form_frame, 
            text="", 
            text_color="gray",
            wraplength=300
        )
        self.cuenta_feedback.pack(pady=10)
        
        # Botones
        btn_frame = ctk.CTkFrame(self.cuenta_form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        self.cuenta_btn_add = ctk.CTkButton(
            btn_frame, 
            text="Agregar", 
            command=self.agregar_cuenta,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.cuenta_btn_add.pack(side="left", expand=True, padx=5)
        
        self.cuenta_btn_update = ctk.CTkButton(
            btn_frame, 
            text="Actualizar", 
            command=self.actualizar_cuenta,
            state="disabled"
        )
        self.cuenta_btn_update.pack(side="left", expand=True, padx=5)
        
        self.cuenta_btn_delete = ctk.CTkButton(
            btn_frame, 
            text="Eliminar", 
            command=self.eliminar_cuenta,
            fg_color="red",
            hover_color="darkred",
            state="disabled"
        )
        self.cuenta_btn_delete.pack(side="left", expand=True, padx=5)
        
        self.cuenta_btn_clear = ctk.CTkButton(
            btn_frame, 
            text="Limpiar", 
            command=lambda: self.limpiar_formulario('cuenta')
        )
        self.cuenta_btn_clear.pack(side="left", expand=True, padx=5)
    
    def _crear_lista_cuentas(self):
        """Crea el panel de lista de cuentas"""
        self.cuenta_list_frame = ctk.CTkFrame(self.cuenta_main_frame)
        
        # Barra de búsqueda
        search_frame = ctk.CTkFrame(self.cuenta_list_frame, fg_color="transparent")
        search_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.cuenta_search_entry = ctk.CTkEntry(
            search_frame, 
            placeholder_text="Buscar cuentas..."
        )
        self.cuenta_search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.cuenta_search_entry.bind("<KeyRelease>", self.buscar_cuentas)
        
        ctk.CTkButton(
            search_frame, 
            text="Buscar", 
            width=80,
            command=self.buscar_cuentas
        ).pack(side="left")
        
        # Lista de cuentas
        self.cuenta_lista = ctk.CTkScrollableFrame(
            self.cuenta_list_frame, 
            height=400
        )
        self.cuenta_lista.pack(fill="both", expand=True, padx=10, pady=10)
    
    # =============================================
    # MÉTODOS COMPARTIDOS
    # =============================================
    
    def limpiar_formulario(self, tipo):
        """Limpia los campos del formulario especificado"""
        if tipo == 'empresa':
            self.empresa_seleccionada = None
            for entry in self.empresa_fields.values():
                entry.delete(0, 'end')
            
            self.empresa_btn_add.configure(state="normal")
            self.empresa_btn_update.configure(state="disabled")
            self.empresa_btn_delete.configure(state="disabled")
            self.mostrar_feedback("Formulario limpiado", "info", "empresa")
        
        elif tipo == 'cuenta':
            self.cuenta_seleccionada = None
            for entry in self.cuenta_fields.values():
                if isinstance(entry, ctk.CTkEntry):
                    entry.delete(0, 'end')
            
            self.cuenta_btn_add.configure(state="normal")
            self.cuenta_btn_update.configure(state="disabled")
            self.cuenta_btn_delete.configure(state="disabled")
            self.mostrar_feedback("Formulario limpiado", "info", "cuenta")
            self.actualizar_combobox_empresas()
    
    def mostrar_feedback(self, mensaje, tipo="info", seccion="empresa"):
        """Muestra mensajes de feedback al usuario"""
        colors = {
            "info": "gray",
            "success": "lightgreen",
            "error": "red",
            "warning": "orange"
        }
        
        if seccion == "empresa":
            self.empresa_feedback.configure(text=mensaje, text_color=colors.get(tipo, "gray"))
        else:
            self.cuenta_feedback.configure(text=mensaje, text_color=colors.get(tipo, "gray"))
    
    def actualizar_combobox_empresas(self):
        """Actualiza el combobox de empresas con datos actuales"""
        empresas = Empresa.objects.all().order_by("nombre")
        values = [f"{emp.key} - {emp.nombre}" for emp in empresas]
        self.empresa_combobox.configure(values=values)
        if values:
            self.empresa_combobox.set(values[0])
    
    def obtener_empresa_desde_combobox(self):
        """Obtiene la empresa seleccionada en el combobox"""
        seleccion = self.empresa_combobox.get()
        if not seleccion:
            return None
        
        key = seleccion.split(" - ")[0]
        try:
            return Empresa.objects.get(key=key)
        except Empresa.DoesNotExist:
            return None
    
    # =============================================
    # MÉTODOS PARA EMPRESAS
    # =============================================
    
    def obtener_datos_empresa(self):
        """Obtiene y valida los datos del formulario de empresa"""
        datos = {}
        required_fields = ["key", "nombre", "tipoTicket"]
        
        for field, entry in self.empresa_fields.items():
            value = entry.get().strip()
            if field in required_fields and not value:
                raise ValueError(f"El campo '{field}' es obligatorio")
            datos[field] = value if value else None
        
        return datos
    
    def actualizar_lista_empresas(self, empresas=None):
        """Actualiza la lista de empresas mostrada"""
        # Limpiar lista actual
        for widget in self.empresa_lista.winfo_children():
            widget.destroy()
        
        # Obtener empresas si no se proporcionan
        if empresas is None:
            empresas = Empresa.objects.all().order_by("nombre")
        
        if not empresas.exists():
            ctk.CTkLabel(
                self.empresa_lista, 
                text="No hay empresas registradas.",
                font=ctk.CTkFont(size=13)
            ).pack(pady=20)
            return
        
        # Mostrar cada empresa
        for emp in empresas:
            frame = ctk.CTkFrame(self.empresa_lista, height=40)
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
        
        for field, entry in self.empresa_fields.items():
            value = getattr(empresa, field, "")
            entry.delete(0, 'end')
            entry.insert(0, str(value) if value else "")
        
        self.empresa_btn_add.configure(state="disabled")
        self.empresa_btn_update.configure(state="normal")
        self.empresa_btn_delete.configure(state="normal")
        self.mostrar_feedback(f"Cargada empresa: {empresa.nombre}", "info", "empresa")
        
        # Actualizar combobox en pestaña de cuentas
        self.actualizar_combobox_empresas()
    
    def buscar_empresas(self, event=None):
        """Busca empresas según el texto ingresado"""
        search_term = self.empresa_search_entry.get().strip()
        
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
            datos = self.obtener_datos_empresa()
            
            # Verificar si ya existe
            if Empresa.objects.filter(key=datos["key"]).exists():
                raise ValidationError("Ya existe una empresa con esta clave")
            
            # Crear nueva empresa
            Empresa.objects.create(**datos)
            
            self.mostrar_feedback("✅ Empresa agregada exitosamente", "success", "empresa")
            self.limpiar_formulario('empresa')
            self.actualizar_lista_empresas()
            self.actualizar_combobox_empresas()
            
        except Exception as e:
            self.mostrar_feedback(f"❌ Error: {str(e)}", "error", "empresa")
    
    def actualizar_empresa(self):
        """Actualiza la empresa seleccionada"""
        if not self.empresa_seleccionada:
            self.mostrar_feedback("No hay empresa seleccionada", "error", "empresa")
            return
            
        try:
            datos = self.obtener_datos_empresa()
            
            # Actualizar empresa
            for field, value in datos.items():
                setattr(self.empresa_seleccionada, field, value)
            
            self.empresa_seleccionada.save()
            
            self.mostrar_feedback("✅ Empresa actualizada exitosamente", "success", "empresa")
            self.limpiar_formulario('empresa')
            self.actualizar_lista_empresas()
            self.actualizar_combobox_empresas()
            
        except Exception as e:
            self.mostrar_feedback(f"❌ Error: {str(e)}", "error", "empresa")
    
    def eliminar_empresa(self):
        """Elimina la empresa seleccionada"""
        if not self.empresa_seleccionada:
            self.mostrar_feedback("No hay empresa seleccionada", "error", "empresa")
            return
            
        # Confirmación antes de eliminar
        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar la empresa {self.empresa_seleccionada.nombre}?\n\n"
            "¡Esta acción también eliminará todas sus cuentas relacionadas!"
        ):
            return
            
        try:
            nombre = self.empresa_seleccionada.nombre
            self.empresa_seleccionada.delete()
            
            self.mostrar_feedback(f"🗑️ Empresa '{nombre}' eliminada", "warning", "empresa")
            self.limpiar_formulario('empresa')
            self.actualizar_lista_empresas()
            self.actualizar_lista_cuentas()
            self.actualizar_combobox_empresas()
            
        except Exception as e:
            self.mostrar_feedback(f"❌ Error al eliminar: {str(e)}", "error", "empresa")
    
    # =============================================
    # MÉTODOS PARA CUENTAS
    # =============================================
    
    def obtener_datos_cuenta(self):
        """Obtiene y valida los datos del formulario de cuenta"""
        datos = {}
        required_fields = ["key", "nombre", "empresa"]
        
        for field, entry in self.cuenta_fields.items():
            if field == "empresa":
                empresa = self.obtener_empresa_desde_combobox()
                if not empresa:
                    raise ValueError("Debe seleccionar una empresa válida")
                datos["empresa"] = empresa
            else:
                value = entry.get().strip()
                if field in required_fields and not value:
                    raise ValueError(f"El campo '{field}' es obligatorio")
                datos[field] = value if value else None
        
        return datos
    
    def actualizar_lista_cuentas(self, cuentas=None):
        """Actualiza la lista de cuentas mostrada"""
        # Limpiar lista actual
        for widget in self.cuenta_lista.winfo_children():
            widget.destroy()
        
        # Obtener cuentas si no se proporcionan
        if cuentas is None:
            cuentas = Cuenta.objects.all().select_related('empresa').order_by("nombre")
        
        if not cuentas.exists():
            ctk.CTkLabel(
                self.cuenta_lista, 
                text="No hay cuentas registradas.",
                font=ctk.CTkFont(size=13)
            ).pack(pady=20)
            return
        
        # Mostrar cada cuenta
        for cuenta in cuentas:
            frame = ctk.CTkFrame(self.cuenta_lista, height=40)
            frame.pack(fill="x", pady=2, padx=5)
            
            # Mostrar información
            ctk.CTkLabel(
                frame, 
                text=f"{cuenta.key} - {cuenta.nombre} ({cuenta.empresa.nombre})",
                anchor="w",
                font=ctk.CTkFont(size=13)
            ).pack(side="left", fill="x", expand=True, padx=10)
            
            # Botón para seleccionar
            ctk.CTkButton(
                frame, 
                text="Seleccionar", 
                width=80,
                command=lambda c=cuenta: self.cargar_cuenta(c)
            ).pack(side="right", padx=5)
    
    def cargar_cuenta(self, cuenta):
        """Carga los datos de una cuenta en el formulario"""
        self.cuenta_seleccionada = cuenta
        
        for field, entry in self.cuenta_fields.items():
            if field == "empresa":
                # Buscar el índice de la empresa en el combobox
                empresas = Empresa.objects.all().order_by("nombre")
                values = [f"{emp.key} - {emp.nombre}" for emp in empresas]
                try:
                    index = next(i for i, emp in enumerate(empresas) if emp.id == cuenta.empresa.id)
                    self.empresa_combobox.set(values[index])
                except StopIteration:
                    pass
            else:
                value = getattr(cuenta, field, "")
                entry.delete(0, 'end')
                entry.insert(0, str(value) if value else "")
        
        self.cuenta_btn_add.configure(state="disabled")
        self.cuenta_btn_update.configure(state="normal")
        self.cuenta_btn_delete.configure(state="normal")
        self.mostrar_feedback(f"Cargada cuenta: {cuenta.nombre}", "info", "cuenta")
    
    def buscar_cuentas(self, event=None):
        """Busca cuentas según el texto ingresado"""
        search_term = self.cuenta_search_entry.get().strip()
        
        if not search_term:
            self.actualizar_lista_cuentas()
            return
        
        cuentas = Cuenta.objects.filter(
            nombre__icontains=search_term
        ).select_related('empresa').order_by("nombre")
        
        self.actualizar_lista_cuentas(cuentas)
    
    def agregar_cuenta(self):
        """Agrega una nueva cuenta"""
        try:
            datos = self.obtener_datos_cuenta()
            
            # Verificar si ya existe
            if Cuenta.objects.filter(key=datos["key"]).exists():
                raise ValidationError("Ya existe una cuenta con esta clave")
            
            # Crear nueva cuenta
            Cuenta.objects.create(**datos)
            
            self.mostrar_feedback("✅ Cuenta agregada exitosamente", "success", "cuenta")
            self.limpiar_formulario('cuenta')
            self.actualizar_lista_cuentas()
            
        except Exception as e:
            self.mostrar_feedback(f"❌ Error: {str(e)}", "error", "cuenta")
    
    def actualizar_cuenta(self):
        """Actualiza la cuenta seleccionada"""
        if not self.cuenta_seleccionada:
            self.mostrar_feedback("No hay cuenta seleccionada", "error", "cuenta")
            return
            
        try:
            datos = self.obtener_datos_cuenta()
            
            # Actualizar cuenta
            for field, value in datos.items():
                setattr(self.cuenta_seleccionada, field, value)
            
            self.cuenta_seleccionada.save()
            
            self.mostrar_feedback("✅ Cuenta actualizada exitosamente", "success", "cuenta")
            self.limpiar_formulario('cuenta')
            self.actualizar_lista_cuentas()
            
        except Exception as e:
            self.mostrar_feedback(f"❌ Error: {str(e)}", "error", "cuenta")
    
    def eliminar_cuenta(self):
        """Elimina la cuenta seleccionada"""
        if not self.cuenta_seleccionada:
            self.mostrar_feedback("No hay cuenta seleccionada", "error", "cuenta")
            return
            
        # Confirmación antes de eliminar
        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de eliminar la cuenta {self.cuenta_seleccionada.nombre}?"
        ):
            return
            
        try:
            nombre = self.cuenta_seleccionada.nombre
            self.cuenta_seleccionada.delete()
            
            self.mostrar_feedback(f"🗑️ Cuenta '{nombre}' eliminada", "warning", "cuenta")
            self.limpiar_formulario('cuenta')
            self.actualizar_lista_cuentas()
            
        except Exception as e:
            self.mostrar_feedback(f"❌ Error al eliminar: {str(e)}", "error", "cuenta")

def run():
    app = GestorApp()
    app.mainloop()
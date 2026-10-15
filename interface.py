import math
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from inspection_circuit import InspectionCircuit
from sector import RunwaySector


class AeroCycleApp(tk.Tk):
    """Professional Spanish-language presentation layer for AeroCycle."""

    COLORS = {
        "background": "#0B1220",
        "panel": "#172338",
        "surface": "#21314A",
        "cyan": "#38BDF8",
        "green": "#22C55E",
        "amber": "#F59E0B",
        "red": "#EF4444",
        "text": "#F8FAFC",
        "muted": "#94A3B8",
        "line": "#334966",
    }
    STATUS_LABELS = {
        "PENDING": "Pendiente",
        "INSPECTED": "Inspeccionado",
        "REVIEW": "Revisión",
    }
    PRIORITY_LABELS = {"HIGH": "Alta", "MEDIUM": "Media", "LOW": "Baja"}

    def __init__(self):
        super().__init__()
        self.title("AeroCycle | Centro de Control")
        self.geometry("1200x720")
        self.minsize(1100, 680)
        self.configure(bg=self.COLORS["background"])
        self.circuit = InspectionCircuit()
        self.views = {}
        self.cards = {}
        self.entries = {}
        self.log_box = None
        self.traversal_label = None
        self._build_style()
        self._build_shell()
        self.show_view("control")
        self.refresh()

    def _build_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", background=self.COLORS["panel"],
                        foreground=self.COLORS["text"], font=("Segoe UI", 10))
        style.configure("TFrame", background=self.COLORS["panel"])
        style.configure("Panel.TFrame", background=self.COLORS["panel"])
        style.configure("Surface.TFrame", background=self.COLORS["surface"])
        style.configure("TLabel", background=self.COLORS["panel"],
                        foreground=self.COLORS["text"])
        style.configure("Muted.TLabel", background=self.COLORS["panel"],
                        foreground=self.COLORS["muted"])
        style.configure("Title.TLabel", background=self.COLORS["background"],
                        foreground=self.COLORS["text"], font=("Segoe UI", 22, "bold"))
        style.configure("Subtitle.TLabel", background=self.COLORS["background"],
                        foreground=self.COLORS["muted"], font=("Segoe UI", 10))
        style.configure("ViewTitle.TLabel", background=self.COLORS["panel"],
                        foreground=self.COLORS["text"], font=("Segoe UI", 17, "bold"))
        style.configure("Section.TLabel", background=self.COLORS["panel"],
                        foreground=self.COLORS["cyan"], font=("Segoe UI", 10, "bold"))
        style.configure("CardTitle.TLabel", background=self.COLORS["surface"],
                        foreground=self.COLORS["muted"], font=("Segoe UI", 9, "bold"))
        style.configure("CardValue.TLabel", background=self.COLORS["surface"],
                        foreground=self.COLORS["text"], font=("Segoe UI", 16, "bold"))
        style.configure("TButton", padding=(10, 7), background=self.COLORS["surface"],
                        foreground=self.COLORS["text"], borderwidth=0)
        style.map("TButton", background=[("active", self.COLORS["cyan"])],
                  foreground=[("active", self.COLORS["background"])])
        style.configure("Primary.TButton", background="#075985",
                        foreground=self.COLORS["text"])
        style.configure("Danger.TButton", background="#7F1D1D",
                        foreground=self.COLORS["text"])
        style.configure("TEntry", fieldbackground=self.COLORS["surface"],
                        foreground=self.COLORS["text"], insertcolor=self.COLORS["text"])
        style.configure("TCombobox", fieldbackground=self.COLORS["surface"],
                        foreground=self.COLORS["text"])
        style.configure("Treeview", background=self.COLORS["surface"],
                        fieldbackground=self.COLORS["surface"], foreground=self.COLORS["text"],
                        rowheight=29)
        style.configure("Treeview.Heading", background="#0F1B2E",
                        foreground=self.COLORS["cyan"], font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", "#075985")])

    def _build_shell(self):
        sidebar = tk.Frame(self, bg="#0F1B2E", width=218)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="AeroCycle", bg="#0F1B2E", fg=self.COLORS["cyan"],
                 font=("Segoe UI", 22, "bold")).pack(anchor="w", padx=22, pady=(28, 0))
        tk.Label(sidebar, text="CONTROL AEROPORTUARIO", bg="#0F1B2E",
                 fg=self.COLORS["muted"], font=("Segoe UI", 8, "bold")).pack(
                     anchor="w", padx=23, pady=(0, 34))
        self.nav_buttons = {}
        navigation = (("control", "Centro de control"), ("management", "Gestión de sectores"),
                      ("structure", "Estructura de datos"))
        for view_name, label in navigation:
            button = tk.Button(sidebar, text=label, anchor="w", relief="flat",
                               borderwidth=0, padx=22, pady=13, cursor="hand2",
                               bg="#0F1B2E", fg=self.COLORS["muted"],
                               activebackground=self.COLORS["surface"],
                               activeforeground=self.COLORS["text"],
                               font=("Segoe UI", 10, "bold"),
                               command=lambda name=view_name: self.show_view(name))
            button.pack(fill="x")
            self.nav_buttons[view_name] = button
        tk.Label(sidebar, text="SIMULACIÓN ACADÉMICA", bg="#0F1B2E",
                 fg=self.COLORS["muted"], font=("Segoe UI", 8)).pack(
                     side="bottom", anchor="w", padx=22, pady=22)

        self.main = ttk.Frame(self, style="Panel.TFrame", padding=(28, 24))
        self.main.pack(side="left", fill="both", expand=True)
        header = ttk.Frame(self.main)
        header.pack(fill="x", pady=(0, 18))
        header_left = ttk.Frame(header)
        header_left.pack(side="left")
        ttk.Label(header_left, text="AeroCycle", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header_left, text="Centro de Control de Inspecciones Aeroportuarias",
                  style="Subtitle.TLabel").pack(anchor="w")
        self.state_label = tk.Label(header, text="MODO SIMULACIÓN", bg="#164E63",
                                    fg=self.COLORS["cyan"], padx=12, pady=6,
                                    font=("Segoe UI", 9, "bold"))
        self.state_label.pack(side="right", anchor="n")
        self.view_host = ttk.Frame(self.main)
        self.view_host.pack(fill="both", expand=True)
        self._build_views()
        self._build_activity()

    def _build_views(self):
        self.views["control"] = ttk.Frame(self.view_host, style="Panel.TFrame")
        self.views["management"] = ttk.Frame(self.view_host, style="Panel.TFrame")
        self.views["structure"] = ttk.Frame(self.view_host, style="Panel.TFrame")
        self._build_control_view()
        self._build_management_view()
        self._build_structure_view()

    def _build_dashboard(self, parent):
        dashboard = ttk.Frame(parent)
        dashboard.pack(fill="x", pady=(0, 18))
        labels = (("SECTORES REGISTRADOS", "total"), ("SECTOR ACTUAL", "current"),
                  ("INSPECCIONES COMPLETADAS", "inspected"), ("SECTORES PENDIENTES", "pending"),
                  ("PROGRESO DE LA RONDA", "progress"), ("INSPECCIONES ACUMULADAS", "inspections"))
        for title, key in labels:
            card = ttk.Frame(dashboard, style="Surface.TFrame", padding=(12, 10))
            card.pack(side="left", fill="both", expand=True, padx=(0, 7))
            ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor="w")
            value = ttk.Label(card, text="0", style="CardValue.TLabel")
            value.pack(anchor="w", pady=(4, 0))
            self.cards[key] = value

    def _build_control_view(self):
        view = self.views["control"]
        self._build_dashboard(view)
        ttk.Label(view, text="Centro de control", style="ViewTitle.TLabel").pack(anchor="w")
        ttk.Label(view, text="Circuito de inspección aeroportuaria",
                  style="Muted.TLabel").pack(anchor="w", pady=(2, 8))
        self.canvas = tk.Canvas(view, bg=self.COLORS["background"],
                                highlightthickness=1, highlightbackground=self.COLORS["line"])
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _event: self.draw_map())
        controls = ttk.Frame(view)
        controls.pack(fill="x", pady=(12, 0))
        for label, command in (("Sector anterior", self.previous),
                               ("Sector siguiente", self.next),
                               ("Marcar como inspeccionado", self.mark_inspected),
                               ("Iniciar ronda", self.start_round),
                               ("Finalizar ronda", self.complete_round),
                               ("Reiniciar ronda", self.start_round)):
            ttk.Button(controls, text=label, command=command).pack(
                side="left", padx=(0, 7))

    def _build_management_view(self):
        view = self.views["management"]
        ttk.Label(view, text="Gestión de sectores", style="ViewTitle.TLabel").pack(anchor="w")
        ttk.Label(view, text="Administra los elementos del circuito sin modificar sus enlaces.",
                  style="Muted.TLabel").pack(anchor="w", pady=(2, 14))
        top = ttk.Frame(view)
        top.pack(fill="x")
        form = ttk.Frame(top, style="Surface.TFrame", padding=14)
        form.pack(side="left", fill="y", padx=(0, 14))
        fields = (("Identificador", "id"), ("Nombre del sector", "name"),
                  ("Tipo de sector", "type"), ("Prioridad", "priority"),
                  ("Posición", "position"), ("Observaciones", "observations"))
        for row, (label, key) in enumerate(fields):
            ttk.Label(form, text=label).grid(row=row, column=0, sticky="w", pady=5, padx=(0, 12))
            if key == "priority":
                widget = ttk.Combobox(form, values=("Alta", "Media", "Baja"),
                                      state="readonly", width=20)
            elif key == "type":
                widget = ttk.Combobox(form, values=("Pista", "Calle de rodaje", "Plataforma"),
                                      width=20)
            else:
                widget = ttk.Entry(form, width=23)
            widget.grid(row=row, column=1, sticky="ew", pady=5)
            self.entries[key] = widget
        actions = ttk.Frame(form)
        actions.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        action_buttons = (("Agregar al inicio", self.add_start), ("Agregar al final", self.add_end),
                          ("Insertar en posición", self.insert_position), ("Buscar sector", self.find),
                          ("Actualizar sector", self.update), ("Eliminar sector", self.delete),
                          ("Limpiar formulario", self.clear_form), ("Cargar aeropuerto demo", self.load_demo))
        for index, (label, command) in enumerate(action_buttons):
            ttk.Button(actions, text=label, command=command).grid(
                row=index // 2, column=index % 2, sticky="ew", padx=3, pady=3)
        actions.columnconfigure(0, weight=1)
        actions.columnconfigure(1, weight=1)
        table_frame = ttk.Frame(top)
        table_frame.pack(side="left", fill="both", expand=True)
        columns = ("id", "name", "type", "priority", "status", "prev", "next")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        headings = ("ID", "Sector", "Tipo", "Prioridad", "Estado", "Anterior", "Siguiente")
        widths = (75, 145, 110, 75, 110, 75, 75)
        for column, heading, width in zip(columns, headings, widths):
            self.table.heading(column, text=heading)
            self.table.column(column, width=width, anchor="w")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.table.bind("<<TreeviewSelect>>", self.select_table_row)

    def _build_structure_view(self):
        view = self.views["structure"]
        ttk.Label(view, text="Visualización de la Lista Circular Doble",
                  style="ViewTitle.TLabel").pack(anchor="w")
        ttk.Label(view, text="Evidencia visual de los enlaces next y prev.",
                  style="Muted.TLabel").pack(anchor="w", pady=(2, 14))
        content = ttk.Frame(view)
        content.pack(fill="both", expand=True)
        self.structure_canvas = tk.Canvas(content, bg=self.COLORS["background"],
                                          highlightthickness=1,
                                          highlightbackground=self.COLORS["line"])
        self.structure_canvas.pack(fill="both", expand=True, pady=(0, 12))
        self.structure_canvas.bind("<Configure>", lambda _event: self.draw_structure())
        bottom = ttk.Frame(view)
        bottom.pack(fill="x")
        self.inspector_label = ttk.Label(bottom, text="", justify="left")
        self.inspector_label.pack(side="left", fill="x", expand=True)
        actions = ttk.Frame(bottom)
        actions.pack(side="right")
        ttk.Button(actions, text="Recorrer hacia adelante",
                   command=lambda: self.show_traversal(True)).pack(side="left", padx=3)
        ttk.Button(actions, text="Recorrer hacia atrás",
                   command=lambda: self.show_traversal(False)).pack(side="left", padx=3)
        ttk.Button(actions, text="Verificar integridad",
                   command=self.verify_integrity).pack(side="left", padx=3)
        self.traversal_label = ttk.Label(view, text="Recorrido: -", style="Muted.TLabel")
        self.traversal_label.pack(anchor="w", pady=(10, 0))

    def _build_activity(self):
        activity = tk.Frame(self, bg="#0F1B2E", height=118)
        activity.pack(side="bottom", fill="x")
        activity.pack_propagate(False)
        tk.Label(activity, text="REGISTRO DE OPERACIONES", bg="#0F1B2E",
                 fg=self.COLORS["cyan"], font=("Segoe UI", 9, "bold")).pack(
                     anchor="w", padx=20, pady=(10, 3))
        self.log_box = ScrolledText(activity, height=3, state="disabled",
                                    bg="#0F1B2E", fg=self.COLORS["muted"],
                                    insertbackground=self.COLORS["text"],
                                    relief="flat", borderwidth=0, font=("Consolas", 9))
        self.log_box.pack(fill="both", expand=True, padx=20, pady=(0, 8))

    def show_view(self, view_name):
        for view in self.views.values():
            view.pack_forget()
        self.views[view_name].pack(fill="both", expand=True)
        for name, button in self.nav_buttons.items():
            button.configure(bg=self.COLORS["surface"] if name == view_name else "#0F1B2E",
                             fg=self.COLORS["text"] if name == view_name else self.COLORS["muted"])
        self.refresh()

    def _entry(self, key):
        value = self.entries[key].get().strip()
        return value

    def _new_sector(self):
        values = (self._entry("id"), self._entry("name"), self._entry("type"),
                  self._entry("priority"))
        if not all(values):
            raise ValueError("Completa identificador, nombre, tipo y prioridad.")
        type_values = {"Pista": "RUNWAY", "Calle de rodaje": "TAXIWAY", "Plataforma": "APRON"}
        priority_values = {"Alta": "HIGH", "Media": "MEDIUM", "Baja": "LOW"}
        sector = RunwaySector(values[0], values[1], type_values.get(values[2], values[2]),
                              priority_values.get(values[3], values[3]))
        sector.observations = self._entry("observations")
        return sector

    def _operation(self, action):
        try:
            if not self.circuit.validate_integrity():
                raise ValueError("La integridad circular es inválida; operación bloqueada.")
            action()
            self.refresh()
        except (ValueError, KeyError, TypeError) as error:
            messagebox.showerror("Operación rechazada", str(error))

    def add_start(self):
        self._operation(lambda: (self.circuit.insert_at_beginning(self._new_sector()),
                                 self.log("Sector registrado correctamente al inicio.")))

    def add_end(self):
        self._operation(lambda: (self.circuit.insert_at_end(self._new_sector()),
                                 self.log("Sector registrado correctamente al final.")))

    def insert_position(self):
        def action():
            try:
                position = int(self._entry("position"))
            except ValueError as error:
                raise ValueError("La posición debe ser un número entero.") from error
            self.circuit.insert_at_position(self._new_sector(), position)
            self.log(f"Sector insertado en la posición {position}.")
        self._operation(action)

    def update(self):
        def action():
            if not self._entry("id"):
                raise ValueError("Indica el identificador del sector.")
            type_values = {"Pista": "RUNWAY", "Calle de rodaje": "TAXIWAY", "Plataforma": "APRON"}
            priority_values = {"Alta": "HIGH", "Media": "MEDIUM", "Baja": "LOW"}
            self.circuit.update_sector(
                self._entry("id"), name=self._entry("name") or None,
                sector_type=type_values.get(self._entry("type"), self._entry("type")) or None,
                priority=priority_values.get(self._entry("priority"), self._entry("priority")) or None,
                observations=self._entry("observations") or None)
            self.log("Sector actualizado correctamente.")
        self._operation(action)

    def delete(self):
        def action():
            sector_id = self._entry("id")
            if not sector_id:
                raise ValueError("Indica el identificador del sector.")
            if not messagebox.askyesno("Confirmar eliminación",
                                       f"¿Eliminar el sector {sector_id}?"):
                return
            self.circuit.delete_sector(sector_id)
            self.log(f"Sector {sector_id} eliminado correctamente.")
        self._operation(action)

    def find(self):
        def action():
            sector = self.circuit.move_to_sector(self._entry("id"))
            self.log(f"Navegación al sector {sector.sector_id}.")
            self.show_view("control")
        self._operation(action)

    def clear_form(self):
        for widget in self.entries.values():
            widget.set("") if isinstance(widget, ttk.Combobox) else widget.delete(0, tk.END)

    def select_table_row(self, _event):
        selected = self.table.selection()
        if not selected:
            return
        values = self.table.item(selected[0], "values")
        self.entries["id"].delete(0, tk.END)
        self.entries["id"].insert(0, values[0])
        self.entries["name"].delete(0, tk.END)
        self.entries["name"].insert(0, values[1])
        self.entries["type"].set({"RUNWAY": "Pista", "TAXIWAY": "Calle de rodaje",
                                  "APRON": "Plataforma"}.get(values[2], values[2]))
        self.entries["priority"].set(self.PRIORITY_LABELS.get(values[3], values[3]))
        sector = self.circuit.find_sector(values[0])
        self.entries["observations"].delete(0, tk.END)
        self.entries["observations"].insert(0, sector.observations if sector else "")

    def next(self):
        self._operation(lambda: (self.circuit.move_next(), self.log("Navegación al siguiente sector.")))

    def previous(self):
        self._operation(lambda: (self.circuit.move_previous(), self.log("Navegación al sector anterior.")))

    def mark_inspected(self):
        self._operation(lambda: (self.circuit.mark_inspected(),
                                 self.log("Sector marcado como inspeccionado.")))

    def start_round(self):
        self._operation(lambda: (self.circuit.start_inspection_round(),
                                 self.log("Ronda de inspección iniciada o reiniciada.")))

    def complete_round(self):
        def action():
            if not self.circuit.complete_round():
                raise ValueError("Todos los sectores deben estar inspeccionados para finalizar.")
            self.log("Ronda de inspección finalizada.")
        self._operation(action)

    def load_demo(self):
        def action():
            if self.circuit.length:
                raise ValueError("El aeropuerto demo solo puede cargarse en un circuito vacío.")
            demo = (("RWY-01", "Pista principal", "RUNWAY", "HIGH"),
                    ("TWY-A", "Calle Alfa", "TAXIWAY", "MEDIUM"),
                    ("APR-N", "Plataforma norte", "APRON", "LOW"),
                    ("RWY-02", "Pista secundaria", "RUNWAY", "HIGH"),
                    ("TWY-B", "Calle Bravo", "TAXIWAY", "MEDIUM"),
                    ("APR-S", "Plataforma sur", "APRON", "LOW"))
            for values in demo:
                self.circuit.insert_at_end(RunwaySector(*values))
            self.log("Aeropuerto de demostración cargado correctamente.")
        self._operation(action)

    def verify_integrity(self):
        if self.circuit.validate_integrity():
            self.log("Circuito validado correctamente: integridad circular VÁLIDA.")
            messagebox.showinfo("Verificación", "La integridad circular es VÁLIDA.")
        else:
            self.log("ERROR: la integridad circular es INVÁLIDA.")
            messagebox.showerror("Verificación", "La integridad circular es INVÁLIDA.")

    def show_traversal(self, forward):
        sectors = self.circuit.traverse_forward() if forward else self.circuit.traverse_backward()
        direction = "hacia adelante" if forward else "hacia atrás"
        result = " ⇄ ".join(sector.sector_id for sector in sectors) or "Circuito vacío"
        self.traversal_label.configure(text=f"Recorrido {direction}: {result}")
        self.log(f"Recorrido {direction} completado.")

    def log(self, message):
        if self.log_box is None:
            return
        stamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert(tk.END, f"[{stamp}] {message}\n")
        self.log_box.see(tk.END)
        self.log_box.configure(state="disabled")

    def refresh(self):
        inspected = self.circuit.count_status("INSPECTED")
        self.cards["total"].configure(text=str(self.circuit.length))
        self.cards["current"].configure(text=self.circuit.current.sector_id
                                        if self.circuit.current else "—")
        self.cards["inspected"].configure(text=str(inspected))
        self.cards["pending"].configure(text=str(self.circuit.count_status("PENDING")))
        self.cards["progress"].configure(text=f"{inspected}/{self.circuit.length}")
        self.cards["inspections"].configure(text=str(self.circuit.total_inspections()))
        state = "VACÍO" if not self.circuit.length else (
            "INSPECCIÓN EN CURSO" if self.circuit.round_active else "CIRCUITO ACTIVO")
        self.state_label.configure(text=f"MODO SIMULACIÓN · {state}")
        self._refresh_table()
        self._refresh_inspector()
        self.draw_map()
        self.draw_structure()

    def _refresh_table(self):
        if not hasattr(self, "table"):
            return
        for item in self.table.get_children():
            self.table.delete(item)
        for sector in self.circuit.traverse_forward():
            self.table.insert("", "end", values=(
                sector.sector_id, sector.name, sector.sector_type,
                self.PRIORITY_LABELS.get(sector.priority, sector.priority),
                self.STATUS_LABELS.get(sector.status, sector.status),
                sector.prev.sector_id, sector.next.sector_id))

    def _refresh_inspector(self):
        current = self.circuit.current
        head = self.circuit.head.sector_id if self.circuit.head else "—"
        tail = self.circuit.tail.sector_id if self.circuit.tail else "—"
        previous = current.prev.sector_id if current else "—"
        following = current.next.sector_id if current else "—"
        validity = "VÁLIDA" if self.circuit.validate_integrity() else "INVÁLIDA"
        text = (f"CABEZA: {head}    COLA: {tail}    ACTUAL: {current.sector_id if current else '—'}\n"
                f"LONGITUD: {self.circuit.length}    ANTERIOR: {previous}    SIGUIENTE: {following}\n"
                f"Último.siguiente → Primero    |    Primero.anterior → Último\n"
                f"INTEGRIDAD CIRCULAR: {validity}")
        self.inspector_label.configure(text=text)

    def _node_color(self, sector):
        if sector is self.circuit.current:
            return self.COLORS["cyan"]
        if sector.status == "INSPECTED":
            return self.COLORS["green"]
        if sector.observations:
            return self.COLORS["red"]
        return self.COLORS["amber"]

    def draw_map(self):
        if not hasattr(self, "canvas"):
            return
        self.canvas.delete("all")
        sectors = self.circuit.traverse_forward()
        if not sectors:
            self.canvas.create_text(400, 120, text="Carga el aeropuerto demo o agrega un sector",
                                    fill=self.COLORS["muted"], font=("Segoe UI", 13))
            return
        width = max(self.canvas.winfo_width(), 600)
        height = max(self.canvas.winfo_height(), 230)
        center_x, center_y = width / 2, height / 2
        radius = min(width * 0.31, height * 0.34)
        self.canvas.create_oval(center_x - radius, center_y - radius,
                                center_x + radius, center_y + radius,
                                outline="#29435E", dash=(4, 6), width=2)
        positions = []
        for index, sector in enumerate(sectors):
            angle = 2 * math.pi * index / len(sectors) - math.pi / 2
            positions.append((center_x + radius * math.cos(angle),
                              center_y + radius * math.sin(angle)))
        for index, (x, y) in enumerate(positions):
            nx, ny = positions[(index + 1) % len(positions)]
            self.canvas.create_line(x, y, nx, ny, fill="#4B6B87", width=2, arrow=tk.LAST)
            self.canvas.create_line(nx, ny, x, y, fill="#253D56", width=1, arrow=tk.LAST)
        for sector, (x, y) in zip(sectors, positions):
            color = self._node_color(sector)
            self.canvas.create_oval(x - 58, y - 31, x + 58, y + 31,
                                    fill=self.COLORS["surface"], outline=color, width=3)
            self.canvas.create_text(x, y - 8, text=sector.sector_id,
                                    fill=self.COLORS["text"], font=("Segoe UI", 10, "bold"))
            self.canvas.create_text(x, y + 10, text=self.STATUS_LABELS[sector.status],
                                    fill=color, font=("Segoe UI", 8))
            self.canvas.create_text(x, y + 47, text=sector.name,
                                    fill=self.COLORS["muted"], font=("Segoe UI", 9))

    def draw_structure(self):
        if not hasattr(self, "structure_canvas"):
            return
        self.structure_canvas.delete("all")
        sectors = self.circuit.traverse_forward()
        if not sectors:
            self.structure_canvas.create_text(400, 100, text="La estructura está vacía",
                                              fill=self.COLORS["muted"],
                                              font=("Segoe UI", 14))
            return
        width = max(self.structure_canvas.winfo_width(), 650)
        center_y = max(self.structure_canvas.winfo_height(), 190) / 2
        gap = min(150, (width - 100) / len(sectors))
        start = (width - gap * (len(sectors) - 1)) / 2
        positions = [(start + index * gap, center_y) for index in range(len(sectors))]
        for index, (x, y) in enumerate(positions):
            nx, ny = positions[(index + 1) % len(positions)]
            self.structure_canvas.create_line(x + 55, y - 8, nx - 55, ny - 8,
                                              fill=self.COLORS["cyan"], width=2, arrow=tk.LAST)
            self.structure_canvas.create_line(nx - 55, y + 8, x + 55, y + 8,
                                              fill=self.COLORS["green"], width=2, arrow=tk.LAST)
        for sector, (x, y) in zip(sectors, positions):
            color = self._node_color(sector)
            self.structure_canvas.create_rectangle(x - 55, y - 30, x + 55, y + 30,
                                                   fill=self.COLORS["surface"],
                                                   outline=color, width=3)
            self.structure_canvas.create_text(x, y, text=sector.sector_id,
                                              fill=self.COLORS["text"],
                                              font=("Segoe UI", 10, "bold"))

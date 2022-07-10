from tkinter import Tk, Label, Button, Entry, Frame, messagebox, Menu, StringVar
from tkinter.ttk import Combobox, Style, LabelFrame
from PIL import ImageTk, Image

from libpsicro_1 import Psicro1
from libpsicro_2 import Psicro2
from libpsicro_3 import Psicro3
from libpsicro_4 import Psicro4
from libpsicro_5 import Psicro5

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Carta Psicrometrica')
        self.geometry('650x430')
        self.iconbitmap("icoforpsicro.ico")
        self.style = Style(self)
        style = Style()
        style.theme_use('clam')
        style.configure("Combobox", fieldbackground="orange", background="white")
        self.option_add("*TCombobox*Listbox*Background", 'LightBlue3')
        self.unidades = ["(°C )", "( % )", "(Kgw/KgA)", "(m^3/KgA)", "(Kg/m^3)", "( °C )", "(KJ/KgA)", "( °C )"]
        self.opciones = ["TBS ", "HR ", "Habs ", "v ", "rho ", "Tpr ", "Entalpía ", "TBH "]
        self.opciones2 = ["TBS ", "Entalpía "]
        self.opciones3 = ["HR ", "Habs ", "Entalpía ", "TBH "]
        self.MenusVar()
        self.FrameDatosCalculos()
        self.muestraImagen()

    def MenusVar(self):
        self.barraMenu = Menu(self)
        self.menuArchivo = Menu(self.barraMenu, tearoff=0, activebackground="aquamarine2", activeforeground="black", bg="LightSkyBlue3", fg="DodgerBlue4")
        self.menuArchivo.add_command(label="Otros")
        self.menuArchivo.add_command(label="Unidades")
        self.menuArchivo.add_separator()
        self.menuArchivo.add_command(label="Salir", command=self.destroy)
        self.barraMenu.add_cascade(label="Archivo", menu=self.menuArchivo)
        self.config(menu=self.barraMenu)

    def FrameDatosCalculos(self):
        self.datosFrame = LabelFrame(self, text="Datos", cursor="pencil")
        self.datosFrame.place(x=10, y=1, width=200, height=170)
        Label(self.datosFrame, text="Hsnm (m)", bg="red").place(x=10, y=10, width=100, height=30)
        self.box_value = StringVar()
        self.box_value2 = StringVar()
        self.cmbOpciones = Combobox(self.datosFrame, width="10", values=self.opciones2, state="readonly", justify="center", textvariable=self.box_value)
        self.cmbOpciones.place(x=10, y=45, width=100, height=30)
        self.cmbOpciones2 = Combobox(self.datosFrame, width="10", values=self.opciones3, state="readonly", justify="center", textvariable=self.box_value2)
        self.cmbOpciones2.place(x=10, y=80, width=100, height=30)
        self.cmbOpciones.current(0)
        self.cmbOpciones2.current(1)
        self.entryDato0 = Entry(self.datosFrame, bg="papaya whip")
        self.entryDato1 = Entry(self.datosFrame, bg="papaya whip")
        self.entryDato2 = Entry(self.datosFrame, bg="papaya whip")
        self.tbnCalcula = Button(self.datosFrame, text="Calcular", bg="#008080", fg="#fff", command=self.fCalcular)
        self.entryDato0.place(x=110, y=12, width=80, height=25)
        self.entryDato1.place(x=110, y=47, width=80, height=25)
        self.entryDato2.place(x=110, y=80, width=80, height=25)
        self.tbnCalcula.place(x=30, y=115, width=140, height=25)
        self.FrameResultados()

    def fCalcular(self):
        if len(self.entryDato0.get()) == 0 or len(self.entryDato1.get()) == 0 or len(self.entryDato2.get()) == 0:
            pass
        else:
            self.H = float(self.entryDato0.get()) or 10
            self.varX1 = float(self.entryDato1.get()) or 30
            self.varX2 = float(self.entryDato2.get()) or 30
            strX1 = self.box_value.get()
            strX2 = self.box_value2.get()
            if strX1 == 'TBS ' and strX2 == 'HR ':
                self.fCalcular1()
            elif strX1 == 'TBS ' and strX2 == 'TBH ':
                self.fCalcular2()
            elif strX1 == 'TBS ' and strX2 == 'Habs ':
                self.fCalcular3()
            elif strX1 == 'Entalpía ' and strX2 == 'Habs ':
                self.fCalcular4()
            elif strX1 == 'TBS ' and strX2 == 'Entalpía ':
                self.fCalcular5()

    def Inserta(self, b, c, d, e, f, g):
        self.entryRes1.insert(0, round(b, 7))
        self.entryRes2.insert(0, round(c, 7))
        self.entryRes3.insert(0, round(d, 7))
        self.entryRes4.insert(0, round(e, 7))
        self.entryRes5.insert(0, round(f, 7))
        self.entryRes6.insert(0, round(g, 7))

    def fCalcular1(self):
        a1 = Psicro1(self.varX1, self.varX2, self.H)
        b = a1.absolute_humidity_tdb_f_h()
        c = a1.specific_volume_tdb_f_h()
        d = a1.density_tdb_f_h()
        e = a1.dew_point_tdb_f_h()
        f = a1.enthalpy_tdb_f_h()
        g = a1.wet_bulb_temperature_tdb_f_h()
        print(a1)  # con el metodo sobrecargado str
        print("Habs: {:.4f}, v: {:.4f}, Rho: {:.4f}".format(b, c, d))
        print("Tpr: {:.4f}, Ent: {:.4f}, Twb:{:.4f} ".format(e, f, g))
        self.FrameResultados()
        self.Inserta(b, c, d, e, f, g)

    def fCalcular2(self):
        a2 = Psicro2(self.varX1, self.varX2, self.H)
        b = a2.absolute_humidity_tdb_twb_h()
        c = a2.specific_volume_tdb_twb_h()
        d = a2.density_tdb_twb_h()
        e = a2.dew_point_tdb_twb_h()
        f = a2.enthalpy_tdb_twb_h()
        g = a2.relative_humidity_tdb_twb_h()
        print(a2)  # con el metodo sobrecargado str
        print("Habs: {:.4f}, v: {:.4f}, Rho {:.4f}".format(b, c, d))
        print("Tpr: {:.4f}, Ent: {:.4f}, HR:{:.4f} ".format(e, f, g))
        self.FrameResultados()
        self.Inserta(b, c, d, e, f, g)

    def fCalcular3(self):
        """
        Realiza los cálculos para la opción TBS y Habs.
        """
        a3 = Psicro3(self.varX1, self.varX2, self.H)
        b = a3.relative_humidity_tdb_x_h()
        c = a3.specific_volume_tdb_x_h()
        d = a3.density_tdb_x_h()
        e = a3.dew_point_x_h()
        f = a3.enthalpy_tdb_x_h()
        g = a3.wet_bulb_temperature_tdb_x_h()
        print(a3)
        print("Habs: {:.4f}, v: {:.4f}, Rho: {:.4f}".format(b, c, d))
        print("Tpr: {:.4f}, Ent: {:.4f}, Twb:{:.4f} ".format(e, f, g))
        self.FrameResultados()
        self.Inserta(b, c, d, e, f, g)

    def fCalcular4(self):
        a4 = Psicro4(self.varX1, self.varX2, self.H)
        b = a4.dry_bulb_temperature_ent_x(self.varX1, self.varX2)
        c = a4.relative_humidity_ent_x_h()
        d = a4.specific_volume_ent_x_h()
        e = a4.density_ent_x_h()
        f = a4.dew_point_x_h()
        g = a4.wet_bulb_temperature_ent_x_h()
        print(a4)  # con el metodo sobrecargado str
        print("Tbs: {:.4f}, HR: {:.4f}, v: {:.4f}".format(b, c, d))
        print("Rho: {:.4f}, Tdp: {:.4f}, Twb:{:.4f} ".format(e, f, g))
        self.FrameResultados()
        self.Inserta(b, c, d, e, f, g)

    def fCalcular5(self):
        a5 = Psicro5(self.varX1, self.varX2, self.H)
        b = a5.absolute_humidity_tdb_ent()
        c = a5.specific_volume_tdb_ent_h()
        d = a5.wet_bulb_temperature_tdb_ent_h()
        e = a5.density_tdb_ent_h()
        f = a5.dew_point_tdb_ent_h()
        g = a5.relative_humidity_tdb_ent_h()
        print(a5)  # con el metodo sobrecargado str
        print("Habs: {:.4f}, v: {:.4f}, Tbh: {:.4f}".format(b, c, d))
        print("Rho: {:.4f}, Tdp: {:.4f}, HR:{:.4f} ".format(e, f, g))
        self.FrameResultados()
        self.Inserta(b, c, d, e, f, g)

    def Comprueba(self):
        opciones3 = ["Habs "]

        if self.box_value.get() == 'Entalpía ' or self.box_value.get() == self.box_value2.get():
            print("Seleccioanste entalpiaa")
            self.cmbOpciones2 = Combobox(self.datosFrame, width="10", values=opciones3, state="readonly", justify="center", textvariable=self.box_value2)
            self.cmbOpciones2.place(x=10, y=80, width=100, height=30)
            self.cmbOpciones2.current(0)

        # acción de botón
        def callback(eventObject):
            self.FrameResultados()
        self.cmbOpciones.bind("<<ComboboxSelected>>", callback)  # de los 2 solo uso el mismo metodo
        self.cmbOpciones2.bind("<<ComboboxSelected>>", callback)

    def FrameResultados(self):
        self.Comprueba()
        resultFrame = LabelFrame(self, text='Resultados')
        resultFrame.place(x=10, y=175, width=200, height=245)
        divi = Frame(resultFrame, bg="red")
        divi.place(x=0, y=0, width=105, height=220)
        divi2 = Frame(resultFrame, bg="blue")
        divi2.place(x=100, y=0, width=95, height=220)
        self.entryRes1 = Entry(resultFrame, bg="papaya whip")
        self.entryRes2 = Entry(resultFrame, bg="papaya whip")
        self.entryRes3 = Entry(resultFrame, bg="papaya whip")
        self.entryRes4 = Entry(resultFrame, bg="papaya whip")
        self.entryRes5 = Entry(resultFrame, bg="papaya whip")
        self.entryRes6 = Entry(resultFrame, bg="papaya whip")
        self.entryRes1.place(x=110, y=2, width=80, height=25)
        self.entryRes2.place(x=110, y=36, width=80, height=25)
        self.entryRes3.place(x=110, y=70, width=80, height=25)
        self.entryRes4.place(x=110, y=108, width=80, height=25)
        self.entryRes5.place(x=110, y=146, width=80, height=25)
        self.entryRes6.place(x=110, y=185, width=80, height=25)

        if self.box_value.get() == 'TBS ':
            self.opciones3 = ["HR ", "Habs ", "Entalpía ", "TBH "]
            self.cmbOpciones2 = Combobox(self.datosFrame, width="10", values=self.opciones3, state="readonly", justify="center", textvariable=self.box_value2)
            self.cmbOpciones2.place(x=10, y=80, width=100, height=30)

        for opciones1 in self.opciones:
            if self.box_value.get() == opciones1 or self.box_value2.get() == opciones1:
                continue
            caja = Frame(divi, bg="#FBE5D6")  # frame para cada var
            caja.pack(expand=True, fill='both')
            rb = Label(caja, text=opciones1 + self.unidades[self.opciones.index(opciones1)])  # Asi llamar a otras unidades
            rb.grid(padx=2, pady=0, ipadx=0, ipady=0, sticky='w')

    def muestraImagen(self):
        ventana2 = Frame(self, width=405, height=355, bg="slategray")  # al final borra este color
        ventana2.place(x=230, y=0)
        image = Image.open('carta.png')
        tk_image = ImageTk.PhotoImage(image)
        Label(ventana2, image=tk_image).place(x=50, y=40, width=314, height=236)
        ventana2.mainloop()

if __name__ == "__main__":
    app = App()
    app.mainloop()

import numpy as np
from tkinter import messagebox
from libpsicro_1 import Psicro1
from libpsicro_2 import Psicro2

class Psicro5(Psicro1):
    def __init__(self, tdb=1, ent=1, H=1):
        self.tdb = tdb
        self.ent = ent
        self.H = H
        self.Patm = self.calculate_atmospheric_pressure(H)

    def __str__(self):
        return "{" + str(self.ent) + "-" + str(self.ent) + "-" + str(self.H) + "}"

    def absolute_humidity_tdb_ent(self):
        return (self.ent - self.tdb) / (2501 + 1.805 * self.tdb)

    def specific_volume_tdb_ent_h(self):
        twb = self.wet_bulb_temperature_tdb_ent_h()
        v1 = Psicro2(self.tdb, twb, self.H)
        return v1.specific_volume_tdb_twb_h()

    def density_tdb_ent_h(self):
        x = self.absolute_humidity_tdb_ent()
        v = self.specific_volume_tdb_ent_h()
        return (1 / v) * (1 + x)

    def dew_point_tdb_ent_h(self):
        twb = self.wet_bulb_temperature_tdb_ent_h()
        tdp1 = Psicro2(self.tdb, twb, self.H)
        return tdp1.dew_point_tdb_twb_h()

    def wet_bulb_temperature_tdb_ent_h(self):
        tdb_max = 96
        h_max = 5350
        x = (self.ent - self.tdb) / (2501 + 1.805 * self.tdb)
        if self.tdb > tdb_max or self.H > h_max:
            messagebox.showinfo(title="Condiciones de entrada", message="No puede haber datos\nmayores a tdbMax:96\nHMax:5350")
            exit()
        return super().interacc_for_wbt(x, self.Patm, self.tdb)

    def relative_humidity_tdb_ent_h(self):
        twb = self.wet_bulb_temperature_tdb_ent_h()
        f1 = Psicro2(self.tdb, twb, self.H)
        return f1.relative_humidity_tdb_twb_h()

def main():
    tdb = 37.8
    f = 31.5
    twb = 23.88
    H = 10
    x = 0.0129
    ent = 71.05
    a = Psicro5(tdb, ent, H)
    b = a.absolute_humidity_tdb_ent()
    c = a.specific_volume_tdb_ent_h()
    d = a.wet_bulb_temperature_tdb_ent_h()
    e = a.density_tdb_ent_h()
    f = a.dew_point_tdb_ent_h()
    g = a.relative_humidity_tdb_ent_h()

    print(a)
    print("Habs: {:.4f}, v: {:.4f}, Tbh: {:.4f}".format(b, c, d))
    print("Rho: {:.4f}, Tdp: {:.4f}, HR:{:.4f} ".format(e, f, g))

if __name__ == "__main__":
    main()

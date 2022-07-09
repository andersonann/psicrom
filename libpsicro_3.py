import numpy as np
from tkinter import messagebox
from libpsicro_1 import Psicro1
from libpsicro_2 import Psicro2

class Psicro3(Psicro1):
    def __init__(self, tdb=1, x=1, H=1):
        self.tdb = tdb
        self.x = x
        self.H = H
        self.Patm = self.calculate_atmospheric_pressure(H)
        self.psat = self.saturated_vapor_pressure_t(tdb)

    def __str__(self):
        return "{" + str(self.tdb) + "-" + str(self.x) + "-" + str(self.H) + "}"

    def specific_volume_tdb_x_h(self):
        twb = self.wet_bulb_temperature_tdb_x_h()
        v1 = Psicro2(self.tdb, twb, self.H)
        return v1.specific_volume_tdb_twb_h()

    def density_tdb_x_h(self):
        twb = self.wet_bulb_temperature_tdb_x_h()
        d1 = Psicro2(self.tdb, twb, self.H)
        return d1.density_tdb_twb_h()

    def dew_point_x_h(self):
        patm = ((44331.514 - self.H) / 11880.516) ** (1 / 0.1902632) / 1000
        pvap = self.x * patm / (0.62198 + self.x) * 100 * 1000
        if pvap <= 0:
            return float('inf')
        return -35.97 - 1.8726 * np.log(pvap) + 1.1689 * (np.log(pvap)) ** 2

    def enthalpy_tdb_x_h(self):
        return self.tdb + self.x * (2501 + 1.805 * self.tdb)

    def wet_bulb_temperature_tdb_x_h(self):
        tdb_max = 96
        h_max = 5350
        if self.tdb > tdb_max or self.H > h_max:
            messagebox.showinfo(title="Condiciones de entrada", message="No puede haber datos\nmayores a tdbMax:96\nHMax:5350")
            exit()
        return super().interacc_for_wbt(self.x, self.Patm, self.tdb)

    def relative_humidity_tdb_x_h(self):
        psat = super().saturated_vapor_pressure_t(self.tdb) * 1e-5
        return (self.Patm / psat) * (self.x / (0.62198 + self.x)) * 100

def main():
    tdb = 37.8
    f = 31.5
    twb = 23.88
    H = 10
    x = 0.0129
    a = Psicro3(tdb, x, H)
    b = a.wet_bulb_temperature_tdb_x_h()
    c = a.specific_volume_tdb_x_h()
    d = a.density_tdb_x_h()
    e = a.dew_point_x_h()
    f = a.enthalpy_tdb_x_h()
    g = a.relative_humidity_tdb_x_h()

    print(a)
    print("TBH:{:.4f} v: {:.4f}, Rho {:.4f}".format(b, c, d))
    print("Tpr: {:.4f}, Ent: {:.4f}, HR:{:.4f} ".format(e, f, g))

if __name__ == "__main__":
    main()

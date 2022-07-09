import numpy as np
from tkinter import messagebox
from libpsicro_1 import Psicro1
from libpsicro_2 import Psicro2

class Psicro4(Psicro1):
    def __init__(self, ent=1, x=1, H=1):
        self.ent = ent
        self.x = x
        self.H = H
        self.Patm = self.calculate_atmospheric_pressure(H)
        self.tdb = self.dry_bulb_temperature_ent_x(ent, x)
        self.psat = self.saturated_vapor_pressure_t(self.tdb)

    def __str__(self):
        return "{" + str(self.ent) + "-" + str(self.x) + "-" + str(self.H) + "}"

    def specific_volume_ent_x_h(self):
        twb = self.wet_bulb_temperature_ent_x_h()
        v1 = Psicro2(self.tdb, twb, self.H)
        return v1.specific_volume_tdb_twb_h()

    def density_ent_x_h(self):
        v = self.specific_volume_ent_x_h()
        return (1 / v) * (1 + self.x)

    def dew_point_x_h(self):
        patm = ((44331.514 - self.H) / 11880.516) ** (1 / 0.1902632) / 1000
        pvap = self.x * patm / (0.62198 + self.x) * 100 * 1000
        if pvap <= 0:
            return float('inf')
        return -35.97 - 1.8726 * np.log(pvap) + 1.1689 * (np.log(pvap)) ** 2

    def relative_humidity_ent_x_h(self):
        psat = super().saturated_vapor_pressure_t(self.tdb) * 1e-5
        return (self.Patm / psat) * (self.x / (0.62198 + self.x)) * 100

    def dry_bulb_temperature_ent_x(self, ent, x):
        return (ent - x * 2501) / (1.805 * x + 1)

    def wet_bulb_temperature_ent_x_h(self):
        tdb_max = 96
        h_max = 5350
        tdb = self.dry_bulb_temperature_ent_x(self.ent, self.x)
        if tdb > tdb_max or self.H > h_max:
            messagebox.showinfo(title="Condiciones de entrada", message="No puede haber datos\nmayores a tdbMax:96\nHMax:5350")
            exit()
        return super().interacc_for_wbt(self.x, self.Patm, tdb)

def main():
    tdb = 37.8
    f = 31.5
    twb = 23.88
    H = 10
    x = 0.0129
    ent = 71.05
    a = Psicro4(ent, x, H)
    b = a.dry_bulb_temperature_ent_x(ent, x)
    c = a.relative_humidity_ent_x_h()
    d = a.specific_volume_ent_x_h()
    e = a.density_ent_x_h()
    f = a.dew_point_x_h()
    g = a.wet_bulb_temperature_ent_x_h()

    print(a)
    print("Tbs: {:.4f}, HR: {:.4f}, v: {:.4f}".format(b, c, d))
    print("Rho: {:.4f}, Tdp: {:.4f}, Twb:{:.4f} ".format(e, f, g))

if __name__ == "__main__":
    main()

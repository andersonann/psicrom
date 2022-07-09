import numpy as np
from tkinter import messagebox
from libpsicro_1 import Psicro1

class Psicro2(Psicro1):
    def __init__(self, tdb=1, twb=1, H=1):
        self.twb = twb
        super().__init__(tdb, f=0, H=H)
        self.psat_twb = self.saturated_vapor_pressure_t(twb)
        self.f = self.relative_humidity_tdb_twb_h()

    def __str__(self):
        return f"{self.tdb}-{self.twb}-{self.H}"

    def absolute_humidity_tdb_twb_h(self):
        patm = self.patm
        psat_wb = self.psat_twb * 1e-5
        xsat_wb = 0.62198 * psat_wb / (patm - psat_wb)
        x = ((2501 - 2.381 * self.twb) * xsat_wb - (self.tdb - self.twb)) / (2501 + 1.805 * self.tdb - 4.186 * self.twb)
        return x

    def specific_volume_tdb_twb_h(self):
        tdb_k = self.tdb + 273.15
        r_gen = 8314.41
        mm_air = 28.9645
        r_air = r_gen / mm_air
        patm_pa = self.patm * 100 * 1000
        x = self.absolute_humidity_tdb_twb_h()
        return r_air * tdb_k / patm_pa * (1 + 1.6078 * x)

    def density_tdb_twb_h(self):
        x = self.absolute_humidity_tdb_twb_h()
        v = self.specific_volume_tdb_twb_h()
        return (1 / v) * (1 + x)

    def dew_point_tdb_twb_h(self):
        patm = ((44331.514 - self.H) / 11880.516) ** (1 / 0.1902632) / 1000
        x = self.absolute_humidity_tdb_twb_h()
        pvap = x * patm / (0.62198 + x) * 100 * 1000
        if pvap <= 0:
            return float('inf')
        return -35.97 - 1.8726 * np.log(pvap) + 1.1689 * (np.log(pvap)) ** 2

    def enthalpy_tdb_twb_h(self):
        x = self.absolute_humidity_tdb_twb_h()
        return self.tdb + x * (2501 + 1.805 * self.tdb)

    def relative_humidity_tdb_twb_h(self):
        patm = 1.01325 * (1 - 0.0000225577 * self.H) ** 5.25588
        x = self.absolute_humidity_tdb_twb_h()
        pvap = x * patm / (0.62198 + x)
        pair = patm - pvap
        psat = super().saturated_vapor_pressure_t(self.tdb) * 1e-5
        f = (x / 0.62198) * (pair / psat)
        return f * 100

# resultados para
def main():
    tdb = 37.8
    twb = 23.88
    h = 10
    ai = Psicro1(tdb, 31.5, h)
    g = ai.wet_bulb_temperature_tdb_f_h()
    print(f"TDW: {g:.4f} valor calculado")

    a = Psicro2(tdb, twb, h)
    b = a.absolute_humidity_tdb_twb_h()
    c = a.specific_volume_tdb_twb_h()
    d = a.density_tdb_twb_h()
    e = a.dew_point_tdb_twb_h()
    f = a.enthalpy_tdb_twb_h()
    g = a.relative_humidity_tdb_twb_h()

    print(a)
    print(f"Habs: {b:.4f}, v: {c:.4f}, Rho {d:.4f}")
    print(f"Tpr: {e:.4f}, Ent: {f:.4f}, HR:{g:.4f}")

if __name__ == "__main__":
    main()

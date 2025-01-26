from modules.powder_element import PowderElement

class WetSand(PowderElement):
    def __init__(self, name="wet_sand", colors=["#997B5B", "#997B5B"], gravity=3, dispersion=1, inertial_resistance=0.7):
        super().__init__(name, colors, gravity, dispersion, inertial_resistance)
from modules.powder_element import PowderElement

class Sand(PowderElement):
    def __init__(self, name="sand", colors=["#f6d7b0", "#f2d2a9", "#eccca2"], gravity=2, dispersion=1, inertial_resistance=0.3):
        super().__init__(name, colors, gravity, dispersion, inertial_resistance)
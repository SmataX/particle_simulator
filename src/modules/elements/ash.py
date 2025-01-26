from modules.powder_element import PowderElement

class Ash(PowderElement):
    def __init__(self, name="ash", colors=["#868683", "#B4B4B4"], gravity=1, dispersion=3, inertial_resistance=0.05):
        super().__init__(name, colors, gravity, dispersion, inertial_resistance)
import hklpy2
from ad_hoc_diffractometer import register_geometry_file

geometry_name = register_geometry_file("cdi-geometry.yml")

cdi = hklpy2.creator(name="cdi", geometry=register_geometry_file("cdi-geometry.yml"), solver="ad_hoc")

# configure geometry
cdi.add_sample("silicon", a=hklpy2.SI_LATTICE_PARAMETER)
cdi.beam.wavelength.put(1.239842) # 10 keV wavelength (Angstroms)

cdi.core.mode = "fixed_alpha"


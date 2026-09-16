# %% [markdown]
# ## CDI custom geometry (`cdi-geometry.yml`) with fixed `alpha`
# 
# Load the declarative `ad_hoc` geometry, select the `fixed_alpha` mode, set the
# substrate `surface_normal`, and try a `forward()` calculation. `alpha` is the
# `incidence` reference constraint (angle between the incident beam and the
# substrate surface).
# 

# %%
import hklpy2
from ad_hoc_diffractometer import register_geometry_file

# Register the declarative geometry (re-reads the file on each creator call).
geom_name = register_geometry_file("cdi-geometry.yml")
geom_name


# %%
cdi = hklpy2.creator(name="cdi", geometry=geom_name, solver="ad_hoc")
cdi.add_sample("silicon", a=hklpy2.SI_LATTICE_PARAMETER)
cdi.beam.wavelength.put(1.54)  # Angstroms - Cu K-alpha

cdi.core.mode = "fixed_alpha"
print("real axes  :", cdi.core.solver.real_axis_names)
print("pseudo axes:", cdi.core.solver.pseudo_axis_names)
print("mode       :", cdi.core.mode)


# %% [markdown]
# ### Orient the crystal (`calc_UB` from two measured Bragg peaks)
# 
# `add_sample(...)` only sets the **lattice** (the `B` matrix). To know *how the
# crystal is mounted* in the lab, the model needs the orientation matrix `U`,
# which comes from **two** measured reflections (workflow step 4).
# 
# Replace the angle dicts below with your real baseline peaks — the placeholder
# values here are NOT physically meaningful.
# 

# %%
# Two measured Bragg peaks: (h, k, l) paired with the motor angles where the
# peak was found. REPLACE these placeholder angles with your real baseline peaks.
r1 = cdi.add_reflection(
    (1, 0, 0),
    dict(mu=0, omega1=-145.451, chi=0, omega2=0, chi2=0, gamma1=0, delta1=69.0966, phi=0),
)
r2 = cdi.add_reflection(
    (0, 1, 0),
    dict(mu=0, omega1=-145.451, chi=90, omega2=0, chi2=0, gamma1=0, delta1=69.0966, phi=90),
)

cdi.core.calc_UB(r1, r2)
cdi.sample.UB


# %%
# The `incidence` (alpha) constraint is measured relative to the substrate
# surface, so the geometry needs to know the surface normal (Miller indices).
cdi.core.solver._geom.surface_normal = (0, 0, 1)

# alpha is a reference-constraint scalar: retune it without editing the YAML.
cdi.core.solver.update_mode_constraints("fixed_alpha", incidence=5.0)  # degrees
cdi.core.solver._geom.surface_normal


# %%
# forward(): reciprocal (h, k, l) -> motor angles, holding alpha = 5 deg.
pos = cdi.forward(1, 0, 2)
reals = {k: round(getattr(pos, k), 3) for k in cdi.core.solver.real_axis_names}
incidence = cdi.core.solver.incidence_angle(reals)
print("forward(1, 0, 2):", reals)
print("incidence (alpha):", round(incidence, 3))

# Sanity check: does inverse() of those angles return (1, 0, 2)?
print("inverse round-trip:", cdi.inverse(pos))


# %%


# %%

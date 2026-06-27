import numpy as np
import streamlit as st

st.set_page_config(
    page_title="Parker Spiral Length Calculator",
    page_icon="☀️",
    layout="centered"
)

# -----------------------------
# Constants
# -----------------------------
AU_km = 1.495978707e8      # 1 AU in km
R_sun_km = 695700.0        # Solar radius in km


def calc_spiral_length(solar_wind_speed, radial_distance, rotation_period=25.38):
    """
    Calculate Parker spiral length from the solar surface to radial_distance.

    Parameters
    ----------
    solar_wind_speed : float
        Solar wind speed in km/s.
    radial_distance : float
        Heliocentric radial distance in AU.
    rotation_period : float
        Solar rotation period in days.

    Returns
    -------
    L_AU : float
        Parker spiral length in AU.
    """

    omega = 2 * np.pi / (rotation_period * 24 * 3600)  # rad/s

    r = radial_distance * AU_km
    dr = r - R_sun_km

    if dr < 0:
        return np.nan

    x = (omega / solar_wind_speed) * dr

    L_km = 0.5 * (solar_wind_speed / omega) * (
        x * np.sqrt(x**2 + 1) + np.log(x + np.sqrt(x**2 + 1))
    )

    return L_km / AU_km


# -----------------------------
# App layout
# -----------------------------
st.title("☀️ Parker Spiral Length Calculator")

st.write(
    "Calculate the Parker spiral magnetic-field-line length from the "
    "solar surface to a selected heliocentric radial distance."
)

st.latex(r"""
L =
\frac{1}{2}\frac{V_{sw}}{\Omega}
\left[
x\sqrt{x^2+1}
+
\ln\left(x+\sqrt{x^2+1}\right)
\right]
""")

st.latex(r"""
x = \frac{\Omega}{V_{sw}}(r-r_S)
""")

st.sidebar.header("Inputs")

solar_wind_speed = st.sidebar.number_input(
    "Solar wind speed, Vsw [km/s]",
    min_value=100.0,
    max_value=1200.0,
    value=400.0,
    step=10.0,
)

radial_distance = st.sidebar.number_input(
    "Radial distance, R [AU]",
    min_value=0.01,
    max_value=10.0,
    value=1.0,
    step=0.01,
)

rotation_period = st.sidebar.number_input(
    "Solar rotation period [days]",
    min_value=20.0,
    max_value=35.0,
    value=25.38,
    step=0.01,
)

L = calc_spiral_length(
    solar_wind_speed=solar_wind_speed,
    radial_distance=radial_distance,
    rotation_period=rotation_period,
)

st.subheader("Result")

st.metric("Parker spiral length", f"{L:.4f} AU")

st.write(
    f"For **Vsw = {solar_wind_speed:.1f} km/s** and "
    f"**R = {radial_distance:.2f} AU**, the Parker spiral length is "
    f"approximately **{L:.4f} AU**."
)

st.subheader("Quick reference at 1 AU")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "250 km/s",
        f"{calc_spiral_length(250, 1.0, rotation_period):.3f} AU"
    )

with col2:
    st.metric(
        "400 km/s",
        f"{calc_spiral_length(400, 1.0, rotation_period):.3f} AU"
    )

with col3:
    st.metric(
        "600 km/s",
        f"{calc_spiral_length(600, 1.0, rotation_period):.3f} AU"
    )

st.caption(
    "Formula uses the Parker spiral length from the solar surface, "
    "with r$_\odot$ = 695700 km."
)

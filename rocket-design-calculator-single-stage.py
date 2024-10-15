import math

def get_float_input(prompt, default):
    """
    Utility function to get float input from the user with a default value.
    """
    try:
        inp = input(f"{prompt} [{default}]: ")
        return float(inp) if inp.strip() != "" else default
    except ValueError:
        print("Invalid input. Using default value.")
        return default

def calculate_orbital_velocity(orbit_altitude):
    """
    Calculate the circular orbital velocity for a given orbit altitude.
    """
    G = 6.67430e-11  # Gravitational constant, m^3 kg^-1 s^-2
    M = 5.972e24     # Mass of Earth, kg
    R_E = 6371000    # Radius of Earth, m

    R = R_E + orbit_altitude  # Orbital radius, m
    v_orbital = math.sqrt(G * M / R)  # m/s
    return v_orbital

def calculate_rotational_boost(latitude_deg):
    """
    Calculate the Earth's rotational velocity boost at a given latitude.
    """
    omega = 2 * math.pi / 86400  # Earth's angular velocity, rad/s
    R_E = 6371000  # Earth's radius at equator, m
    latitude_rad = math.radians(latitude_deg)

    v_rotation = omega * R_E * math.cos(latitude_rad)  # m/s
    return v_rotation

def calculate_mass_ratio(delta_v, specific_impulse):
    """
    Calculate the mass ratio using the Tsiolkovsky rocket equation.
    """
    g0 = 9.81  # Standard gravity, m/s^2
    ve = specific_impulse * g0  # Effective exhaust velocity, m/s

    mass_ratio = math.exp(delta_v / ve)
    return mass_ratio, ve

def calculate_total_mass(m_payload, mass_ratio, structural_fraction):
    """
    Calculate the total initial mass of the rocket considering payload, structure, and fuel.
    """
    denominator = 1 - mass_ratio * structural_fraction
    if denominator <= 0:
        return None  # This signals that the structural fraction is too high.
    m0 = (mass_ratio * m_payload) / denominator
    m_structure = structural_fraction * m0
    m_fuel = m0 - m_structure - m_payload

    return m0, m_structure, m_fuel

def find_max_structural_fraction(mass_ratio):
    """
    Automatically calculate the maximum allowable structural fraction based on the mass ratio.
    """
    return 1 / mass_ratio

def main():
    print("=== Rocket Design Calculator ===\n")

    # Default parameters
    default_payload = 1.0  # kg
    default_specific_impulse = 350.0  # seconds
    default_launch_latitude = 45.0  # degrees
    default_orbit_altitude = 200000.0  # meters (200 km)
    default_structural_fraction = 0.10  # 10%
    default_delta_v_budget = 9.5e3  # delta-v budget (m/s)

    print("Enter the following parameters or press Enter to use default values.\n")

    payload_mass = get_float_input("Payload mass (kg)", default_payload)
    specific_impulse = get_float_input("Specific Impulse (s)", default_specific_impulse)
    launch_latitude = get_float_input("Launch Latitude (degrees)", default_launch_latitude)
    orbit_altitude = get_float_input("Orbit Altitude (meters)", default_orbit_altitude)
    structural_fraction = get_float_input("Structural Mass Fraction (0-1)", default_structural_fraction)

    # Selecting delta-v budget within the given range
    while True:
        delta_v_budget = get_float_input("Delta-v Budget (km/s) between 9.3 and 10.0", default_delta_v_budget / 1000)
        if 9.3 <= delta_v_budget <= 10.0:
            delta_v_budget *= 1000  # Convert to m/s
            break
        else:
            print("Please enter a delta-v budget between 9.3 and 10.0 km/s.")

    print("\n=== Calculations ===\n")

    # Step 1: Calculate orbital velocity
    v_orbital = calculate_orbital_velocity(orbit_altitude)
    print(f"1. Orbital Velocity: {v_orbital:.2f} m/s")

    # Step 2: Calculate Earth's rotational boost
    v_rotation = calculate_rotational_boost(launch_latitude)
    print(f"2. Earth's Rotational Boost at {launch_latitude}° Latitude: {v_rotation:.2f} m/s")

    # Step 3: Use user-selected delta-v budget directly
    print(f"3. Selected Delta-v Budget: {delta_v_budget:.2f} m/s")

    # Step 4: Calculate mass ratio and exhaust velocity
    mass_ratio, ve = calculate_mass_ratio(delta_v_budget, specific_impulse)
    print(f"4. Tsiolkovsky Mass Ratio: {mass_ratio:.2f}")
    print(f"   Effective Exhaust Velocity (ve): {ve:.2f} m/s")

    # Step 5: Calculate total mass, structural mass, and fuel mass
    total_mass_result = calculate_total_mass(payload_mass, mass_ratio, structural_fraction)

    # If the structural fraction is too high and results in a negative denominator, find the maximum allowable fraction.
    if total_mass_result is None:
        print(f"\nWarning: Structural fraction of {structural_fraction} is too high for this configuration.")
        max_structural_fraction = find_max_structural_fraction(mass_ratio)
        print(f"Automatically adjusting to the maximum possible structural fraction: {max_structural_fraction:.4f}")
        structural_fraction = max_structural_fraction
        total_mass_result = calculate_total_mass(payload_mass, mass_ratio, structural_fraction)

        # If it's still invalid, handle the NoneType case.
        if total_mass_result is None:
            print("\nError: Even after adjustment, the structural fraction is too high for the given configuration.")
            return

    # Extract mass results
    m0, m_structure, m_fuel = total_mass_result
    print(f"5. Total Initial Mass (m0): {m0:.2f} kg")
    print(f"   Structural Mass (m_structure): {m_structure:.2f} kg")
    print(f"   Fuel Mass (m_fuel): {m_fuel:.2f} kg")

    print("\n=== Summary ===")
    print(f"Payload Mass: {payload_mass:.2f} kg")
    print(f"Structural Mass: {m_structure:.2f} kg")
    print(f"Fuel Mass: {m_fuel:.2f} kg")
    print(f"Total Initial Mass: {m0:.2f} kg")
    print(f"Delta-v Budget: {delta_v_budget:.2f} m/s")
    print(f"Mass Ratio: {mass_ratio:.2f}")
    print(f"Effective Exhaust Velocity (ve): {ve:.2f} m/s")
    print(f"Orbital Velocity: {v_orbital:.2f} m/s")
    print(f"Earth's Rotational Boost: {v_rotation:.2f} m/s")

    print("\n=== Notes ===")
    print(f"- Original Structural Fraction entered: {default_structural_fraction}.")
    print(f"- Adjusted Structural Fraction (if needed): {structural_fraction:.4f}")
    print("- Ensure that the structural mass fraction is realistic (typically between 5% to 20%).")
    print("- This calculator assumes a single-stage rocket. Multi-stage designs can optimize the mass ratio further.")

if __name__ == "__main__":
    main()

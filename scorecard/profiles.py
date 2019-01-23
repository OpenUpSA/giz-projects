def get_profile(geo):
    population_density = None
    if geo.square_kms and geo.population:
        population_density = geo.population / geo.square_kms

    profile = {
        'total_population': geo.population,
        'population_density': population_density,
    }
    return profile

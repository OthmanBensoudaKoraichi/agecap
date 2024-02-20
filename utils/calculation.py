import datetime


# Function to find the age group from an age
def find_age_group(age, primes_df):
    """Find the corresponding age group for a given age."""
    for age_group in primes_df["age"]:
        start, end = map(int, age_group.split("-"))
        if start <= age <= end:
            return age_group
    return None


def calculate_age(dob):
    today = datetime.date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

# Function to calculate each premium
def calculate_family_premiums(family_dobs, primes_df, coefficients_df):
    family_premiums = []

    for dob in family_dobs:
        age = calculate_age(dob)
        age_group = find_age_group(age, primes_df)

        if age_group:
            premium_row = primes_df[primes_df["age"] == age_group].iloc[0]
            premiums = {
                "age": age,
                "age_group": age_group,
                "premiums": {
                    "Annuel": {},
                    "Semestriel": {},
                    "Trimestriel": {},
                    "Mensuel": {},
                },
            }

            for column in primes_df.columns[1:-1]:  # Skipping 'age' and 'deces'
                annual_premium = premium_row[column]
                premiums["premiums"]["Annuel"][column] = annual_premium
                premiums["premiums"]["Semestriel"][column] = (
                    annual_premium * coefficients_df[column].iloc[0]
                )
                premiums["premiums"]["Trimestriel"][column] = (
                    annual_premium * coefficients_df[column].iloc[1]
                )
                premiums["premiums"]["Mensuel"][column] = (
                    annual_premium * coefficients_df[column].iloc[2]
                )

            family_premiums.append(premiums)

    return family_premiums


#  Function to sum the calculated premiums
def sum_family_premiums(family_premiums):
    total_premiums = {"Annuel": {}, "Semestriel": {}, "Trimestriel": {}, "Mensuel": {}}

    # Sum premiums for each frequency and rate across all family members
    for member in family_premiums:
        for freq, rates in member["premiums"].items():
            for rate, premium in rates.items():
                if rate not in total_premiums[freq]:
                    total_premiums[freq][rate] = 0
                total_premiums[freq][rate] += premium

    # Round the totals after summation
    for freq in total_premiums:
        for rate in total_premiums[freq]:
            total_premiums[freq][rate] = int(total_premiums[freq][rate])

    return total_premiums

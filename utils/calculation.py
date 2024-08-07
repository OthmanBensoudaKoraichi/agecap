import datetime


# Function to find the age group from an age
def find_age_group(age, relation, primes_df):
    """Find the corresponding age group for a given age and relation."""
    # Map form relation types to dataset relation types
    if relation.lower() == "enfant":
        age_relation = "enfant"
    else:
        age_relation = "adulte"

    for index, row in primes_df.iterrows():
        age_group = row["age"]
        row_relation = row["relation"]
        start, end = map(int, age_group.split("-"))
        if start <= age <= end and row_relation == age_relation:
            return age_group
    return None

def calculate_age(dob):
    today = datetime.date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age

# Function to calculate each premium
def calculate_family_premiums(family_dobs, relation_types, primes_df, coefficients_df):
    family_premiums = []
    first_dob = True  # Flag to check if it's the first dob

    for dob, relation in zip(family_dobs, relation_types):
        age = calculate_age(dob)
        age_group = find_age_group(age, relation, primes_df)

        if age_group:
            premium_row = primes_df[(primes_df["age"] == age_group) & (primes_df["relation"] == relation)].iloc[0]
            deces_premium = premium_row['deces'] if first_dob else 0  # 'deces' for first dob only

            premiums = {
                "age": age,
                "age_group": age_group,
                "relation": relation,
                "premiums": {
                    "Annuel": {},
                    "Semestriel": {},
                    "Trimestriel": {},
                    "Mensuel": {},
                },
            }

            for column in primes_df.columns[2:-1]:  # Skipping 'age', 'relation', and 'deces'
                annual_premium = premium_row[column] + deces_premium  # Add 'deces' to annual premium
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

            first_dob = False  # Set flag to False after processing the first dob

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

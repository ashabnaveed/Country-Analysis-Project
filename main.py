# design_project.py
# ENDG 233 F24
# Ashab Naveed and Nawfal Cheema
# 441
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.
# Remember to include docstrings and comments throughout your code.

import numpy as np 
import matplotlib.pyplot as plt
from user_csv import read_csv, write_csv

#COMPLETED FXNS 

def invalid_input(): 
    """
    """
    print("\n" + "-" * 70) # Prints a new line and 70 dashes
    print("Invalid input. Try again.\n") 

def no_records(country):
    """
    Prints a string if there is no countries.

    Arguments:
        country -- The name of the country (or region/subregion)

    Returns:
        N/A
    
    """
    print(f"\nThere are no records available for {country}.") # Prints no records for the parameter country

def exit_message():
    """
    """
    print("=" * 70) # Prints 70 equal signs
    print("\nThank you for using the program.") 

def load_csv_data():
    """
    Loads the CSV data into numpy arrays

    Arguments:
        None

    Returns:
        Numpy array of each 2D list.
    """

    # consider adding a seperate variable for headers? 

    # Creates a numpy array for each 2D list to be used in subsequent analysis. Does not include the header row.
    threatened_species = np.array(read_csv('Threatened_Species.csv', include_header=True)[1:]) 
    population_data = np.array(read_csv('Population_Data.csv', include_header=True)[1:])
    country_data = np.array(read_csv('Country_Data.csv', include_header=True)[1:])

    population_headers = read_csv("Population_Data.csv", include_header=True)[0] # Get the header only of the population data

    # Return all loaded data for further use in the analysis program
    return threatened_species, population_data, country_data, population_headers

def get_country(countries):
    """
    Prompts the user to enter a country, region, or sub-region for analysis and validates the input

    Arguments:
        countries -- The name of the country/subregion/region 

    Returns:
        country -- The valid country, region, or sub-region entered by the user.
                    Returns "0" if the user opts to quit
    """

    while True: 
        # Prompts user to input a country, region, or subregion
        country = input("\nEnter the country, UN region, or UN sub-region you want to analyze or type 0 to quit: ").strip()

        # If the user enters "0", exit that function and return "0"
        if country == "0":
            return country
        else:
            valid_input = False # Initialize the input to be invalid

            # Iterate through the list of countries, regions, sub-regions to validate the input
            for i in countries:
                if (country.lower() == i[0].lower() or country.lower() == i[1].lower() or country.lower() == i[2].lower()):
                    valid_input = True
                    break 
            if valid_input:
                return country
            else: 
                invalid_input()

def print_options():
    """
    Displays the menu options and returns the user's choice.

    Arguments:
        None
    
    Returns:
        choice -- The user's menu selection as an integer
    """

    print("\nSelect an option:\n1. Analyze Population Change and Density\n2. Analyze Threatened Species Density and Sepcies-to-Population Ratio\n3. Find Year with Highest Change in Population\n0. Return to country selection")
    choice = input("Enter your choice: ").strip()

    if choice.isdigit():
        return int(choice)
    else:
        return -1 # Flag for invalid input

def get_countries_list(country_input, country_data):
    """
    Returns a list of countries that match the country_input and the input type.

    Arguments:
        country_input -- The country, UN region, or UN subregion inputted by the user.
        country_data -- Numpy array of country data.

    Returns:
        matching_countries -- List of matching country names.
        input_type -- 'Country', 'Region', or 'Subregion'
    """
    
    # Initialize a list to link the matching countries
    matching_countries = []
    input_type = None
    is_country = False # Flags for valid inputs, initialized to be false
    is_region = False
    is_subregion = False

    for row in country_data:
        country_name = row[0]
        if country_input.lower() == country_name.lower():
            matching_countries.append(country_name)
            is_country = True
            break

    if is_country:
        input_type = 'Country'
        return matching_countries, input_type

    for row in country_data:
        country_name = row[0]
        un_region = row[1]
        un_subregion = row[2]
        if country_input.lower() == un_region.lower():
            matching_countries.append(country_name)
            is_region = True
        elif country_input.lower() == un_subregion.lower():
            matching_countries.append(country_name)
            is_subregion = True

    if is_region:
        region_type = 'Region'
    elif is_subregion:
        input_type = 'Subregion'
    else:
        input_type = 'Unknown'
    return matching_countries, input_type

def get_available_years(population_headers):
    """
    Extracts the list of available years from population headers.

    Arguments:
        population_headers -- List of headers from the population data.

    Returns:
        years -- List of available years as integers 
    """

    years = [int(col.split()[0]) for col in population_headers[1:]]
    return years

def get_years(years_list):
    """
    Prompts the user to input start and end years for analysis.

    Arguments:
        years_list -- list of available years.

    Returns:
        start_year -- The starting year selected by the user.
        end_year -- The ending year selected by the user.
    """
    
    print("\nAvailable years:", years_list)
    while True:
        try:
            start_year = int(input("Enter the start year: "))
            end_year = int(input("Enter the end year: "))
            if start_year in years_list and end_year in years_list:
                if start_year != end_year and start_year < end_year:
                    return start_year, end_year
                else:
                    print("Start year and end year must be different or start year must be earlier than end year.")
            else:
                print("Years must be within the available range.")
        except ValueError:
            print("Invalid input. Enter integer years.")

def get_single_year(years_list, prompt="Enter the year: "):
    
    print("\nAvailable years: ", years_list)

    while True:
        try:
            selected_year = int(input(prompt))

            if selected_year in years_list:
                return selected_year
            else:
                print("The year must be in the available range")
        except ValueError:
            print("Invalid input, please enter an integer year.")
        
def print_table(headers, rows):

    col_width = [len(str(header)) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_width[i] = max(col_width[i], len(str(cell)))
    
    formatted_str = "| " + " | ".join("{:<" + str(width) + "}" for width in col_width) + " |"
    print("-" * (sum(col_width) + 3 * len(col_width) + 1))
    print(formatted_str.format(*headers))
    print("-" * (sum(col_width) + 3 * len(col_width) + 1))

    for i in rows:
        print(formatted_str.format(*i))

    print("-" * (sum(col_width) + 3 * len(col_width) + 1))

def analyze_population(matching_countries, population_data, country_data, population_headers, start_year, end_year, density_year, input_type, country_input):
    years = get_available_years(population_headers)
    total_population_start = 0
    total_population_end = 0
    total_population_density_year = 0
    total_area = 0
    country_results = []
    area = None

    try:
        start_index = years.index(start_year) + 1
        end_index = years.index(end_year) + 1
        density_year_index = years.index(density_year) + 1
    except ValueError:
        invalid_input()
        return None
    
    for country in matching_countries:
        pop_row = None

        for i in population_data:
            if i[0].lower() == country.lower():
                pop_row = i
                break
        if pop_row is None:
            if input_type == 'Country':
                print(f"No population data available for {country_input}.")
                return None
            else:
                continue
    
        for country_row in country_data:
            if country_row[0].lower() == country.lower():
                try:
                    area = float(country_row[3])
                except ValueError:
                    area = None
                break

        if area is None:
            if input_type ==  'Country':
                print(f"No valid area data available for {country_input}.")
                return None
            else: 
                continue
        
        try:
            pop_start = float(pop_row[start_index])
            pop_end = float(pop_row[end_index])
            pop_density = float(pop_row[density_year_index])
        except ValueError:
            if input_type == "Country":
                print(f"Population data missing for {country_input}")
                return None
            else:
                continue
        
        delta_population = pop_end - pop_start
        population_density = pop_density / area

        total_population_start += pop_start
        total_population_end += pop_end
        total_population_density_year += pop_density
        total_area += area

        country_results.append({
            'Country': country,
            f'Population {start_year}': pop_start,
            f'Population {end_year}': pop_end,
            'Change in Population': delta_population,
            f'Population Density {density_year}': population_density,
            'Area': area
        })

    if total_population_start == 0 or total_population_end == 0 or total_area == 0:
        print("Insufficient data to preform analysis")
        return None
    
    delta_population_total = total_population_end - total_population_start
    population_density_total = total_population_density_year / total_area

    print("\nPopulation Analysis:")

    if input_type != "Country":
        print(f'Total Population in {country_input} in {start_year}: {total_population_start:.0f}')
        print(f'Total Population in {country_input} in {end_year}: {total_population_end:.0f}')
        print(f'Change in Population in {country_input} from {start_year} to {end_year}: {delta_population_total:.0f}')
        print(f'Population Density in {country_input} in {density_year}: {population_density_total:.2f} per square km')
    else:
        print(f'Total Population in {start_year}: {total_population_start:.0f}')
        print(f'Total Population in {end_year}: {total_population_end:.0f}')
        print(f'Change in Population from {start_year} to {end_year}: {delta_population_total:.0f}')
        print(f'Population Density in {density_year}: {population_density_total:.2f} per square km')
        
    if len(country_results) > 1:
        print("\nDetailed Analysis Table")
        headers = ['Country', f'Population {start_year}', f'Population {end_year}', 'Change in Population', f'Population Density {density_year}']
        rows = []

        for results in country_results:
            row = [
            results['Country'],
            f"{results[f'Population {start_year}']:.0f}",
            f"{results[f'Population {end_year}']:.0f}",
            f"{results[f'Change in Population']:.0f}",
            f"{results[f'Population Density {density_year}']:.2f}"
            ]

            rows.append(row)

        print_table(headers, rows)
    
    visualize_population_analysis(country_results, years, start_year, end_year, density_year, input_type, population_data, country_input)

    return {
        'Start Year': start_year,
        'End Year': end_year,
        'Density Year': density_year,
        f'Total Population in {start_year}': total_population_start,
        f'Total Population in {end_year}': total_population_end,
        "Change in Population": delta_population_total,
        "Population Density": population_density_total
    }

def analyze_threatened_species(matching_countries, threatened_species, country_data, population_data, population_headers, population_year, input_type, country_input):
    """
    Analyzes the endagered/threatened species data for the given list of countries.

    Arguments: 
        matching_countres -- List of countries to analyze
        threatened_species -- Numpy array of endagered/threatened species data
        country_data -- Numpy array of population data.
        population_data -- Numpy array of population data.
        population_headers -- List of headers from the population data
        population_year -- The population year for analysis.
        input_type -- Type of the input('Country', 'Region', 'Subregion')
        country_input -- The user inputted country, region, or subregion
    
    Returns:
        result -- Dictionary containing analysis results.
    """
    years = get_available_years(population_headers)
    try:
        population_year_index = years.index(population_year) + 1
    except ValueError:
        print("Selected year is not in the data range.")
        return None
    
    total_species = 0
    total_area = 0
    total_population_year = 0

    country_results = []

    for country in matching_countries:
        species_row = None
        for row in threatened_species:
            if row[0].lower() == country.lower():
                species_row = row
                break

        if species_row is None:
            continue

        area = None
        for row in country_data:
            if row[0].lower() == country.lower():
                try:
                    area = float(row[3])
                except ValueError:
                    area = None
                break

        if area is None:
            continue

        pop_row = None
        for row in population_data:
            if row[0].lower() == country.lower():
                pop_row = row
                break
        if pop_row is None:
            continue
        pop_year = float(pop_row[population_year_index])

        mammals = float(species_row[1])
        birds = float(species_row[2])
        fish = float(species_row[3])
        plants = float(species_row[4])
        species_count = mammals + birds + fish + plants

        threatened_density = (species_count / area) * 1000
        species_to_population_ratio = species_count / pop_year

        total_species += species_count
        total_area += area
        total_population_year += pop_year

        country_results.append({
            'Country': country,
            'Total Species': species_count,
            'Area (Sq km)': area,
            f'Population {population_year}': pop_year,
            'Threatened Species Density': threatened_density,
            'Species to Population Ratio': species_to_population_ratio
        })

    if total_species == 0 or total_area == 0 or total_population_year == 0:
        print("Insuffiient data to perform analysis.")
        return None

    threatened_density_total = (total_species / total_population_year) * 1000

    species_to_population_ratio_total = total_species / total_population_year

    print("Threatened Species Analysis")

    if input_type != "Country":
        print(f'Threatened Density in {country_input}: {threatened_density_total:.6f} species per 1000 square km')
        print(f'Species to Population Ratio Density in {country_input} for {population_year}: {species_to_population_ratio_total:.10f} species per person')
    else: 
        print(f'Threatened Species Density: {threatened_density_total:.6f} species per 1000 square km')
        print(f'Species to Population Ratio Density for {population_year}: {species_to_population_ratio_total:.10f} species per person')

    if len(matching_countries) > 1:
        print("\nDetailed Country Data Table")
        headers = ['Country', "Total Species", "Area (Sq km)", f'Population {population_year}', "Threatened Species Density", "Species to Population Ratio"]
        rows = []

        for results in country_results:
            row = [
            results['Country'],
            f"{results[f'Total Species']:.0f}",
            f"{results[f'Area (Sq km)']:.0f}",
            f"{results[f'Population {population_year}']:.0f}",
            f"{results[f'Threatened Species Density']:.6f}",
            f"{results[f'Species to Population Ratio']:.10f}"
            ]

            rows.append(row)

        print_table(headers, rows)

    visualize_threatened_analysis(country_results, population_year, input_type, country_input)

    return{
        'Population Year': population_year,
        'Threatened Species Density': threatened_density_total,
        'Species to Population Ratio': species_to_population_ratio_total
    }

def year_with_highest_change(matching_countries, population_data, population_headers, input_type, country_input):
    """
    Finds years with highest absolute change in population for the given countries over all available years.

    Arguments:
        matching_countries -- List of countries to analyze.
        population_data -- Numpy array of population data.
        population_headers -- List of headers from the population data
        input_type -- Type of the input ('Country', 'Region', 'Subregion')
        country_input -- the user inputted country, region, or subregion

    Returns: 
        result -- Dictionary containing the years and changes in population
    """
    years = [int(col.split()[0]) for col in population_headers[1:]]
    years = years[::-1]
    num_years = len(years)
    total_populations = [0] * num_years

    country_yearly_changes = {country: [] for country in matching_countries}

    for country in matching_countries:
        pop_row = None
        for row in population_data:
            if row[0].lower() == country.lower():
                pop_row = row
                break 
        if pop_row is None:
            continue
            
        country_pops = []
        for i in range(num_years):
            try:
                pop = float(pop_row[len(pop_row) - i -1])
            except ValueError:
                pop = 0
            country_pops.append(pop)
            
        for i in range(num_years):
            total_populations[i] += country_pops[i]

        changes = []
        for i in range(len(country_pops) - 1):
            change = country_pops[i+1] - country_pops[i]
            changes.append({
                'start_year': years[i],
                'end_year': years[i+1],
                'change': change
                })
        country_yearly_changes[country] = changes
        
    population_changes = []
    for i in range(num_years - 1):
        change = total_populations[i+1] - total_populations[i]
        population_changes.append({
            'start_year': years[i],
            'end_year': years[i+1],
            'change': change
        })

    abs_changes = [abs(item['change']) for item in population_changes]
    max_abs_change = max(abs_changes)
    max_change_years = [item for item in population_changes if abs(item['change']) == max_abs_change]

    if input_type != 'Country':
        print(f"\nYear(s) with the Highest Change in Population in {country_input}")
    else:
        print("\nYear(s) with the Highest Change in Population")


    for item in max_change_years:
        change_type = "increase" if item['change'] >= 0 else "decrease"
        print(f"Between {item['start_year']} and {item['end_year']} with a {change_type} of {abs(item['change']):.0f} people")

    visualize_population_change(total_populations, years, population_changes, max_change_years, input_type, country_input)

    if len(matching_countries) == 1:
        country = matching_countries[0]
        changes = country_yearly_changes.get(country, [])
        abs_country_changes = [abs(item['change']) for item in changes]
        max_country_abs_change = max(abs_country_changes)
        max_country_change_years = []
        for item in changes:
            if abs(item['change']) == max_country_abs_change:
                max_country_change_years.append(item)
        print(f"\nFor {country}, the year(s) with the highest change in population:")
        for item in max_country_change_years:
            change_type = 'increase' if item['change'] >= 0 else "decrease"
            print(f"Between {item['start_year']} and {item['end_year']} with a {change_type} of {abs(item['change']):.0f} people")
        
    else:
        print("\nDetailed Country Data:")
        headers = ['Country', 'Start Year', 'End Year', 'Change in Population']
        rows = []
        for country in matching_countries:
            changes = country_yearly_changes.get(country, [])
            if changes:
                abs_changes = [abs(item['change']) for item in changes]
                max_country_abs_change = max(abs_changes)
                for item in changes: 
                    if abs(item['change']) == max_country_abs_change:
                        change_type = 'increase' if item['change'] >= 0 else 'decrease'
                        row =[
                            country,
                            item['start_year'],
                            item['end_year'],
                             f"{abs(item['change']):.0f} ({change_type})"
                        ]

            rows.append(row)
        print_table(headers, rows)

    result = {
        'Years with Highest Change in Population': ', '.join(f"{item['start_year']}-{['end_year']}" for item in max_change_years),
        'Highest Change in Population': max_abs_change
    }
    return result

# INCOMPLETE/ERRORS
      
def visualize_population_analysis(country_results, years, start_year, end_year, density_year, input_type, population_data, country_input):
    """
    Generates visualizations for population analysis.

    Arguments:
        country_results -- List of dictionaries with per-country results
        years -- List of available years
        start_year -- Starting year for analysis
        end_year -- Ending year for analysis
        density_year -- Year for population density calculation
        input_type -- Type of the input('Country', 'Region', 'Subregion')
        country_input -- The user inputted country, region, or subregion
        population_data -- Numpy array of population data
    """

    countries = [result['Country'] for result in country_results]
    densities = [result[f'Population Density {density_year}'] for result in country_results]
    
    selected_years = list(range(start_year, end_year +1))
    total_pops = []
    for year in selected_years:
        year_index = years.index(year) + 1
        year_total = 0
        for country in countries:
            pop_row = None
            for row in population_data:
                if row[0].lower() == country.lower():
                    pop_row = row
                    break
            if pop_row is not None:
                try: 
                    year_total += float(pop_row[year_index])
                except ValueError:
                    continue
        total_pops.append(year_total)

    changes = []
    change_years = []
    if len(total_pops) > 1:
        changes = [total_pops[i+1] - total_pops[i] for i in range(len(total_pops)-1)]
        change_years = [f"{selected_years[i]}-{selected_years[i+1]}" for i in range(len(selected_years)-1)]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (10, 10))

    ax1.bar(countries, densities, color = 'skyblue')
    if input_type != 'Country':
        ax1.set_title(f'Population Density in {country_input} in {density_year}')
    else:
        ax1.set_title(f'Population Density in {density_year}')
    ax1.set_xlabel('Country', fontsize = 12)
    ax1.set_ylabel('Population Density (people per Sq Km)', fontsize = 12)
    ax1.tick_params(axis = 'x', rotation = 90, labelsize = 8)

    ax2.plot(selected_years, total_pops, marker = 'o')
    if input_type != 'Country':
        ax2.set_title(f'Total Population in {country_input} by Year')
    else:
        ax2.set_title(f'Total Population by Year')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Total Population')
    ax2.grid(True)

    ax2.set_xticks(selected_years)
    ax2.set_xticklabels([str(year) for year in selected_years])

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.8)
    plt.savefig("final_plots/population_analysis.png", dpi = 300)
    print("Plot saved")
    plt.show()
    plt.close()

def visualize_population_change(total_populations, years, population_changes, max_change_years, input_type, country_input):
    """
    Generates visualizations for population change analysis

    Arguments:
        total_population -- List of total populations per year
        years -- List of years
        population_changes -- List of population changes between years
        max_change_years -- List of changes with the maximum absolute change
        input_type -- Type of the input('Country', 'Region', 'Subregion')
        country_input -- The user inputted country, region, or subregion
    """
    change_years = [f"{item['start_year']} - {item['end_year']}" for item in population_changes]
    changes = [item['change'] for item in population_changes]
    colours = ['red' if item in max_change_years else 'blue' for item in population_changes]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,6))

    ax1.plot(years, total_populations, marker='o')

    if input_type != 'Country':
        ax1.set_title(f'Total Population in {country_input} Over Years')
    else:
        ax1.set_title('Total Population Over Years')
    
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Total Population')
    ax1.grid(True)

    ax2.bar(change_years, changes, color=colours)

    if input_type != 'Country':
        ax2.set_title(f'Total Population in {country_input} Between Years')
    else: 
        ax1.set_title('Change in Population Between Years')
    
    ax2.set_xlabel('Year Range')
    ax2.set_ylabel('Change in Population')
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()

    plt.savefig("final_plots/population_change.png")
    print("Plot saved")
    plt.show()
    plt.close()

def visualize_threatened_analysis(country_results, population_year, input_type, country_input):
    """
    """
    countries = [result['Country'] for result in country_results]
    threatened_densities = [result['Threatened Species Density'] for result in country_results]

    plt.figure(figsize=(10, 6))
    plt.bar(countries, threatened_densities, color='green')

    if input_type != "Country":
        plt.title(f'Threatened Species Density in {country_input} ({population_year})')
    else:
        plt.title(f'Threatened Species Density per Country({population_year})')
    
    plt.xlabel('Country')
    plt.ylabel("Threatened Species Density (species per 1000 Sq km)")
    plt.xticks(rotation=90)
    plt.tight_layout()

    plt.savefig("final_plots/threatened_species.png")
    print("Plot saved")
    plt.show()
    plt.close()
 
def save_results_to_csv(results):
    headers = ["Analyis Type", "Country/Region"]
    all_keys = set()

    for result in results_to_save:
        analysis_data = result[2]
        all_keys.update(analysis_data.keys())
    
    headers.extend(sorted(all_keys))
    data_to_write = [headers]

    for result in results_to_save:
        analyis_type = result[0]
        country = result[1]
        analyis_data = result[2]
        row = [analyis_type, country]
        
        for key in sorted(all_keys):
            row.append(analyis_data.get(key, ''))
        
        data_to_write.append(row)
    
    write_csv('Analysis_Results.csv', data_to_write, overwrite=True)
    print("Saved results.")

# Main Program 

print("Started Population Analyis Progam")

threatened_species, population_data, country_data, population_headers = load_csv_data()
results_to_save = [] # for use once save results to csv is done

while True:
    country = get_country(country_data)
    if country == "0":
        exit_message()
        if results_to_save:
            save_results_to_csv(results_to_save)
        break

    matching_countries, input_type = get_countries_list(country, country_data)
    if not matching_countries:
        no_records(country)
        continue

    while True:
        choice = print_options()

        if choice == 1:
            years_list = get_available_years(population_headers)
            start_year, end_year = get_years(years_list)
            density_year = get_single_year(years_list, "Enter the year for the population density calculation: ")
            result = analyze_population(matching_countries, population_data, country_data, population_headers, start_year, end_year, density_year, input_type, country)
            if result is not None:
                results_to_save.append(["Population Analysis", country, result])
            break
        elif choice == 2:
            years_list = get_available_years(population_headers)
            threatened_year = get_single_year(years_list, "Enter the year for the density calculation: ")
            result = analyze_threatened_species(matching_countries, threatened_species, country_data, population_data, population_headers, threatened_year, input_type, country)
            if result is not None:
                results_to_save.append(["Threatened Species Analysis", country, result])
            break
        elif choice == 3:
            result = year_with_highest_change(matching_countries, population_data, population_headers, input_type, country)
            if result is not None:
                results_to_save.append(["Year with Highest Change in Population Analyis", country, result])
            break
        elif choice == 0:
            exit_message()
            break
        else:
            invalid_input()



        
            

  

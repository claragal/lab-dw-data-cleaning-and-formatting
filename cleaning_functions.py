import pandas as pd

def clean_column_names(df):
    """
    Standardize column names: replace 'ST' with 'state', 
    replace spaces with underscores, and convert to lowercase.
    """
    df.columns = (df.columns
                  .str.replace('ST', 'state', regex=False)
                  .str.replace(' ', '_')
                  .str.lower())
    return df


def clean_invalid_values(df):
    """
    Apply various cleaning transformations to the DataFrame:
    - Standardize gender values
    - Replace state abbreviations with full names
    - Standardize education values
    - Clean customer lifetime value column
    - Clean vehicle class column
    """
    # 1. Standardize gender
    df['gender'] = df['gender'].replace({
        'F': 'F',
        'M': 'M',
        'Female': 'F',
        'male': 'M',
        'Male': 'M',
        'Femal': 'F'
    })

    # 2. Replace state abbreviations
    state_name = {
        'AZ': 'Arizona',
        'Cali': 'California',
        'WA': 'Washington'
    }
    df['state'] = df['state'].replace(state_name)

    # 3. Standardize education
    df['education'] = df['education'].replace({'Bachelors': 'Bachelor'})

    # 4. Clean customer lifetime value
    df['customer_lifetime_value'] = df['customer_lifetime_value'].replace('%', '', regex=False).astype(float)

    # 5. Clean vehicle class
    df['vehicle_class'] = df['vehicle_class'].replace({
        'Sports Car': 'Luxury',
        'Luxury SUV': 'Luxury',
        'Luxury Car': 'Luxury'
    })
    
    return df


def formatting_data_types(df):
    """
    Ensure the correct data types for specific columns:
    - Convert 'customer_lifetime_value' to numeric
    - Extract and convert 'number_of_open_complaints'
    """
    # Convert 'customer_lifetime_value' to numeric
    df['customer_lifetime_value'] = pd.to_numeric(df['customer_lifetime_value'], errors='coerce')

    # Clean 'number_of_open_complaints' by taking the middle value
    df['number_of_open_complaints'] = df['number_of_open_complaints'].apply(
        lambda x: int(x.split('/')[1]) if isinstance(x, str) else x
    )
    
    return df


def fill_missing_values(df):
    """
    Fill missing values:
    - For numerical columns, fill with the median.
    """
    numerical_cols = df.select_dtypes(include=['float64', 'int']).columns
    df[numerical_cols] = df[numerical_cols].fillna(df[numerical_cols].median())
    
    return df


def convert_numeric_to_integers(df):
    """
    Convert all numeric columns to integers.
    """
    numerical_cols = df.select_dtypes(include=['float64', 'int']).columns
    df[numerical_cols] = df[numerical_cols].astype(int)
    
    return df


def main():
    """
    Main function to clean and format the dataset.
    """
    # Load the dataset (replace 'your_file.csv' with the actual file path)
    insurance_df = pd.read_csv('your_file.csv')
    
    # Apply cleaning and formatting steps
    insurance_df = clean_column_names(insurance_df)
    insurance_df = clean_invalid_values(insurance_df)
    insurance_df = formatting_data_types(insurance_df)
    insurance_df = fill_missing_values(insurance_df)
    insurance_df = convert_numeric_to_integers(insurance_df)

    # Save the cleaned dataframe to a new CSV file
    insurance_df.to_csv('cleaned_insurance_data.csv', index=False)

    print("Data cleaning and formatting complete. Cleaned file saved as 'cleaned_insurance_data.csv'.")
    
if __name__ == "__main__":
    main()



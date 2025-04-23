import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import *
import scipy.stats as stats

# 1. DATA LOADING AND INITIAL INSPECTION
def load_and_inspect_data(file_path):
    """Load data and perform initial inspection"""
    excel_file = pd.ExcelFile(file_path)
    
    # Load both data and questions sheets
    data_raw = pd.read_excel(excel_file, "2022-23 Survey of Albertans Dat")
    questions = pd.read_excel(excel_file, "Questions")
    
    # Basic inspection
    print(f"Data shape: {data_raw.shape}")
    print(f"Questions shape: {questions.shape}")
    
    # Check for missing values
    missing_vals = data_raw.isnull().sum()
    print("\nMissing values per column:")
    print(missing_vals[missing_vals > 0])
    
    # Check for duplicate records
    duplicates = data_raw.duplicated().sum()
    print(f"\nDuplicate records: {duplicates}")
    
    return data_raw, questions

# 2. DATA CLEANING AND PREPROCESSING
def clean_and_preprocess(data_raw, questions):
    """Clean and preprocess the survey data"""
    # Create renaming dictionary from questions sheet
    rename_dict = dict(zip(
        questions['Variable'],
        questions['Label'].str.split('--').str[1].str.strip()
    ))
    rename_dict.update({"sample_id": "sample_id"})
    
    # Rename columns
    data_renamed = data_raw.rename(columns=rename_dict)
    
    # Define NA values dictionary
    na_value_dict = {
        "(-7) Skipped": pd.NA,
        "(-9) Don't know": pd.NA,
        "(-8) Prefer not to say": pd.NA,
        "(-8) Prefer not to answer": pd.NA,
        "(0) Not selected": pd.NA
    }
    
    # Replace NA values
    data_cleaned = data_renamed.replace(na_value_dict)
    
    # Clean age categories
    age_mapping = {
        '(3) 25 to 34': '25 to 34',
        '(6) 55 to 64': '55 to 64',
        "(7) 65 or older": "65 or older",
        "(4) 35 to 44": "35 to 44",
        "(5) 45 to 54": "45 to 54",
        "(2) 18 to 24": "18 to 24"
    }
    data_cleaned.loc[:, "What age range do you fall into?"] = data_cleaned.loc[:, "What age range do you fall into?"].replace(age_mapping)
    
    # Clean volunteering hours
    hours_mapping = {
        "(0) 0": "0",
        "(1) 1": "1",
        "(2) 2": "2", 
        "(3) 3-5": "3-5",
        "(4) 6-10": "6-10",
        "(5) 11-20": "11-20",
        "(6) 21-40": "21-40",
        "(7) 40+": "40+"
    }
    
    hours_col = "[Bucketed] In the past 12 months, on average, about how many hours per month did you spend formally volunteering? [Do formal volunteering]"
    if hours_col in data_cleaned.columns:
        data_cleaned.loc[:, hours_col] = data_cleaned.loc[:, hours_col].replace(hours_mapping)
        
        # Create ordered categorical variable
        hours_order = ["0", "1", "2", "3-5", "6-10", "11-20", "21-40", "40+"]
        data_cleaned[hours_col] = pd.Categorical(
            data_cleaned[hours_col],
            categories=hours_order,
            ordered=True
        )
    
    # Create binary age group variable (seniors vs non-seniors)
    data_cleaned['is_senior'] = data_cleaned["What age range do you fall into?"].isin(["55 to 64", "65 or older"])
    
    return data_cleaned

# 3. DEMOGRAPHIC ANALYSIS
def analyze_demographics(data):
    """Analyze demographic characteristics of survey respondents"""
    print("Age distribution:")
    age_dist = data["What age range do you fall into?"].value_counts(dropna=False)
    print(age_dist)
    
    # Create age distribution plot
    plt.figure(figsize=(10, 6))
    sns.countplot(y=data["What age range do you fall into?"].dropna(), 
                  order=data["What age range do you fall into?"].value_counts().index)
    plt.title("Distribution of Respondents by Age Group")
    plt.xlabel("Count")
    plt.ylabel("Age Group")
    plt.tight_layout()
    plt.show()
    
    # Education level analysis
    edu_col = "What is the highest level of education you have completed?"
    if edu_col in data.columns:
        print("\nEducation distribution:")
        edu_dist = data[edu_col].value_counts(dropna=False)
        print(edu_dist)
    
    # Employment status analysis
    emp_col = "What is your employment status?"
    if emp_col in data.columns:
        print("\nEmployment status distribution:")
        emp_dist = data[emp_col].value_counts(dropna=False)
        print(emp_dist)

# 4. VOLUNTEERING BEHAVIOR ANALYSIS
def analyze_volunteering_behavior(data):
    """Analyze volunteering behavior patterns"""
    # Formal volunteering rate
    formal_col = "Formal volunteering : Which, if any, type(s) of volunteering have you done in the past 12 months?"
    if formal_col in data.columns:
        formal_rate = data[formal_col].value_counts(normalize=True) * 100
        print(f"Formal volunteering rate: {formal_rate.get('(1) Selected', 0):.1f}%")
    
    # Informal volunteering rate
    informal_col = "Informal volunteering : Which, if any, type(s) of volunteering have you done in the past 12 months?"
    if informal_col in data.columns:
        informal_rate = data[informal_col].value_counts(normalize=True) * 100
        print(f"Informal volunteering rate: {informal_rate.get('(1) Selected', 0):.1f}%")
    
    # No volunteering rate
    no_vol_col = "No volunteering : Which, if any, type(s) of volunteering have you done in the past 12 months?"
    if no_vol_col in data.columns:
        no_vol_rate = data[no_vol_col].value_counts(normalize=True) * 100
        print(f"No volunteering rate: {no_vol_rate.get('(1) Selected', 0):.1f}%")
    
    # Hours spent volunteering 
    hours_col = "[Bucketed] In the past 12 months, on average, about how many hours per month did you spend formally volunteering? [Do formal volunteering]"
    if hours_col in data.columns:
        # Drop respondents with no formal volunteering data
        vol_data = data.dropna(subset=[hours_col])
        
        # Hours distribution by age group
        plt.figure(figsize=(12, 8))
        cross_tab = pd.crosstab(
            index=vol_data[hours_col],
            columns=vol_data["What age range do you fall into?"],
            normalize='columns'
        ) * 100
        
        cross_tab.plot(kind='bar', stacked=False)
        plt.title("Distribution of Volunteer Hours by Age Group")
        plt.xlabel("Hours per Month")
        plt.ylabel("Percentage within Age Group (%)")
        plt.legend(title="Age Group")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
        # Statistical test: Is there a relationship between age and volunteering hours?
        # Create contingency table for chi-square test
        contingency = pd.crosstab(vol_data[hours_col], vol_data["is_senior"])
        chi2, p, dof, expected = stats.chi2_contingency(contingency)
        print(f"\nChi-square test for age vs. volunteering hours:")
        print(f"Chi2 value: {chi2:.2f}, p-value: {p:.4f}")
        if p < 0.05:
            print("There is a statistically significant relationship between age and volunteering hours.")
        else:
            print("No statistically significant relationship between age and volunteering hours.")

# 5. CHALLENGES ANALYSIS
def analyze_challenges(data):
    """Analyze challenges faced by volunteers, comparing seniors vs. non-seniors"""
    # Filter to relevant challenge columns
    challenge_cols = [col for col in data.columns if "challenges have you ever been faced with" in col]
    challenge_cols = [col for col in challenge_cols if "Other challenges" not in col and "None of the above" not in col and "I have never volunteered" not in col]
    
    # Remove the common text to make column names shorter
    short_names = [col.split(" : ")[0] for col in challenge_cols]
    
    # Calculate the percentage of respondents facing each challenge, by age group
    senior_challenges = {}
    non_senior_challenges = {}
    
    for i, col in enumerate(challenge_cols):
        # Get short name for the challenge
        short_name = short_names[i]
        
        # Calculate percentage for seniors
        senior_data = data[data["is_senior"]]
        if not senior_data.empty:
            senior_pct = (senior_data[col] == "(1) Selected").mean() * 100
            senior_challenges[short_name] = senior_pct
        
        # Calculate percentage for non-seniors
        non_senior_data = data[~data["is_senior"]]
        if not non_senior_data.empty:
            non_senior_pct = (non_senior_data[col] == "(1) Selected").mean() * 100
            non_senior_challenges[short_name] = non_senior_pct
    
    # Create DataFrame for plotting
    challenge_df = pd.DataFrame({
        'Challenge': list(senior_challenges.keys()),
        'Seniors (%)': list(senior_challenges.values()),
        'Non-Seniors (%)': list(non_senior_challenges.values())
    })
    
    # Sort by the difference between seniors and non-seniors
    challenge_df['Difference'] = challenge_df['Seniors (%)'] - challenge_df['Non-Seniors (%)']
    challenge_df = challenge_df.sort_values('Difference', ascending=False)
    
    # Create a horizontal bar chart for challenges
    plt.figure(figsize=(12, 10))
    
    # First create a barplot for non-seniors
    bar1 = plt.barh(challenge_df['Challenge'], challenge_df['Non-Seniors (%)'], 
                    color='skyblue', alpha=0.8, label='Non-Seniors')
    
    # Then create a barplot for seniors
    bar2 = plt.barh(challenge_df['Challenge'], challenge_df['Seniors (%)'], 
                    color='darkblue', alpha=0.6, label='Seniors')
    
    plt.xlabel('Percentage (%)')
    plt.title('Challenges Faced by Volunteers: Seniors vs. Non-Seniors')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.show()
    
    # Statistical test for each challenge: seniors vs. non-seniors
    print("\nStatistical comparison of challenges: Seniors vs. Non-Seniors")
    print("=" * 50)
    
    for i, col in enumerate(challenge_cols):
        # Get short name for the challenge
        short_name = short_names[i]
        
        # Create contingency table
        contingency = pd.crosstab(data[col] == "(1) Selected", data["is_senior"])
        
        # Chi-square test
        chi2, p, _, _ = stats.chi2_contingency(contingency)
        
        significance = "**" if p < 0.01 else "*" if p < 0.05 else ""
        print(f"{short_name}: χ²={chi2:.2f}, p={p:.4f} {significance}")

# 6. WHAT WOULD MAKE VOLUNTEERING MORE APPEALING ANALYSIS
def analyze_appeal_factors(data):
    """Analyze factors that would make volunteering more appealing"""
    # Filter to relevant 'appeal' columns
    appeal_cols = [col for col in data.columns if "make formal volunteering more appealing" in col]
    
    # Remove the common text to make column names shorter
    short_names = [col.split(" : ")[0] for col in appeal_cols]
    
    # Calculate the percentage of respondents who find each factor "very appealing" or "somewhat appealing"
    appeal_factors = []
    senior_appeal = []
    non_senior_appeal = []
    
    for i, col in enumerate(appeal_cols):
        # Get short name
        short_name = short_names[i]
        appeal_factors.append(short_name)
        
        # Overall appealing percentage
        appealing_responses = ["(1) Very appealing", "(2) Somewhat appealing"]
        overall_pct = data[col].isin(appealing_responses).mean() * 100
        
        # Senior appealing percentage
        senior_data = data[data["is_senior"]]
        if not senior_data.empty:
            senior_pct = senior_data[col].isin(appealing_responses).mean() * 100
            senior_appeal.append(senior_pct)
        
        # Non-senior appealing percentage
        non_senior_data = data[~data["is_senior"]]
        if not non_senior_data.empty:
            non_senior_pct = non_senior_data[col].isin(appealing_responses).mean() * 100
            non_senior_appeal.append(non_senior_pct)
    
    # Create DataFrame for plotting
    appeal_df = pd.DataFrame({
        'Factor': appeal_factors,
        'Seniors (%)': senior_appeal,
        'Non-Seniors (%)': non_senior_appeal
    })
    
    # Sort by the difference between seniors and non-seniors
    appeal_df['Difference'] = appeal_df['Seniors (%)'] - appeal_df['Non-Seniors (%)']
    appeal_df = appeal_df.sort_values('Difference', ascending=False)
    
    # Create a horizontal bar chart for appeal factors
    plt.figure(figsize=(12, 10))
    
    # First create a barplot for non-seniors
    bar1 = plt.barh(appeal_df['Factor'], appeal_df['Non-Seniors (%)'], 
                   color='lightgreen', alpha=0.8, label='Non-Seniors')
    
    # Then create a barplot for seniors
    bar2 = plt.barh(appeal_df['Factor'], appeal_df['Seniors (%)'], 
                   color='darkgreen', alpha=0.6, label='Seniors')
    
    plt.xlabel('Percentage Finding Factor Appealing (%)')
    plt.title('Factors Making Volunteering More Appealing: Seniors vs. Non-Seniors')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.show()
    
    # Create heatmap for one specific factor - this replicates your existing analysis
    chosen_value = "Organizations that regularly recognize the contributions of volunteers. : To what extent would each of the following make formal volunteering more appealing for you?"
    
    if chosen_value in data.columns:
        # Create cross-tabulation
        crosstab = pd.crosstab(
            index=data["What age range do you fall into?"],
            columns=data[chosen_value],
            normalize='index'
        ) * 100
        
        # Convert to long format for plotting
        plot_data = crosstab.reset_index().melt(
            id_vars="What age range do you fall into?",
            var_name="response",
            value_name="percentage"
        )
        
        # Create the plot
        p = (
            ggplot(plot_data, 
                   aes(x="What age range do you fall into?", 
                       y="response", 
                       fill="percentage"))
            + geom_tile()
            + theme(figure_size=(12, 8),
                    axis_text_x=element_text(angle=45, hjust=1))
            + labs(title="Volunteer Appreciation Appeal by Age Group (%)",
                   x="Age Range",
                   y="Response Level",
                   fill="Percentage (%)")
            + theme(axis_text_x=element_text(angle=30, hjust=1, size=10))
            + scale_fill_gradient2(low="white", mid="skyblue", high="navy", midpoint=25)
        )
        
        print(p)

# 7. MAIN ANALYSIS FUNCTION
def main_analysis(file_path):
    """Main function to run the complete analysis pipeline"""
    print("="*50)
    print("ALBERTA VOLUNTEER SURVEY ANALYSIS")
    print("="*50)
    
    # Load and inspect data
    print("\n1. DATA LOADING AND INSPECTION")
    print("-"*30)
    data_raw, questions = load_and_inspect_data(file_path)
    
    # Clean and preprocess data
    print("\n2. DATA CLEANING AND PREPROCESSING")
    print("-"*30)
    data_clean = clean_and_preprocess(data_raw, questions)
    
    # Analyze demographics
    print("\n3. DEMOGRAPHIC ANALYSIS")
    print("-"*30)
    analyze_demographics(data_clean)
    
    # Analyze volunteering behavior
    print("\n4. VOLUNTEERING BEHAVIOR ANALYSIS")
    print("-"*30)
    analyze_volunteering_behavior(data_clean)
    
    # Analyze challenges
    print("\n5. CHALLENGES ANALYSIS")
    print("-"*30)
    analyze_challenges(data_clean)
    
    # Analyze appeal factors
    print("\n6. WHAT WOULD MAKE VOLUNTEERING MORE APPEALING")
    print("-"*30)
    analyze_appeal_factors(data_clean)
    
    print("\nAnalysis complete!")
    
    return data_clean

# Run the analysis
if __name__ == "__main__":
    file_path = "Alberta/acsw-survey-albertans-data-file-2022-2023.xlsx"
    clean_data = main_analysis(file_path)

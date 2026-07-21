import os
import pandas as pd

def clean_and_analyze_data(interim_file="data/interim/hockey_teams.json", output_file="data/processed/hockey_teams.csv"):
    """
    Cleans raw JSON data, assigns teams to leagues (A, B, C, D), and saves to CSV.
    """
    if not os.path.exists(interim_file):
        print(f"Interim file {interim_file} does not exist!")
        return
        
    print(f"Loading interim data from {interim_file}...")
    df_raw = pd.read_json(interim_file)
    
    # Standardize column mapping
    column_mapping = {
        'Team Name': 'team',
        'Year': 'season',
        'Wins': 'victories',
        'Losses': 'defeats',
        'OT Losses': 'overtime_defeats',
        'Win %': 'victory_percentage',
        'Goals For (GF)': 'scored_goals',
        'Goals Against (GA)': 'received_goals',
        '+ / -': 'goal_difference'
    }
    
    df = df_raw.rename(columns=column_mapping)
    
    # Clean overtime_defeats: fill empty with 0 and convert to int
    df['overtime_defeats'] = df['overtime_defeats'].fillna(0)
    df.loc[df['overtime_defeats'] == '', 'overtime_defeats'] = 0
    df['overtime_defeats'] = df['overtime_defeats'].astype(int)
    
    # Ensure numeric columns are correct types
    numeric_cols = ['season', 'victories', 'defeats', 'scored_goals', 'received_goals', 'goal_difference']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
        
    df['victory_percentage'] = pd.to_numeric(df['victory_percentage'], errors='coerce').fillna(0.0).astype(float)
    
    # Aggregate to calculate overall win probability per team for categorization
    df_agg_team = (
        df
        .groupby('team')
        .agg({'victories': 'sum', 'defeats': 'sum'})
    )
    
    # Overall victory rate per team (victories / total games)
    df_agg_team['overall_victory_percentage'] = df_agg_team['victories'] / (df_agg_team['victories'] + df_agg_team['defeats'])
    df_agg_team['overall_victory_percentage'] = df_agg_team['overall_victory_percentage'].fillna(0.0)
    
    # Cutoff points based on quantiles of overall victory percentage
    top_a_cutoff = df_agg_team['overall_victory_percentage'].quantile(0.95)
    top_b_cutoff = df_agg_team['overall_victory_percentage'].quantile(0.70)
    top_c_cutoff = df_agg_team['overall_victory_percentage'].quantile(0.20)
    
    def assign_team_to_league(win_pct):
        if win_pct >= top_a_cutoff:
            return 'A'
        elif win_pct >= top_b_cutoff:
            return 'B'
        elif win_pct >= top_c_cutoff:
            return 'C'
        else:
            return 'D'
            
    df_agg_team['league'] = df_agg_team['overall_victory_percentage'].apply(assign_team_to_league)
    
    # Merge league classification back into df
    df = df.merge(
        df_agg_team[['league']],
        left_on='team',
        right_index=True
    )
    
    # Ensure processed directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save to CSV using semicolon separator as specified in notebooks
    df.to_csv(output_file, sep=';', index=False)
    print(f"Cleaned and analyzed data saved to {output_file}. Total rows: {len(df)}")
    
    # Display some stats
    print("\nLeague assignment summary:")
    league_counts = df_agg_team['league'].value_counts()
    for league, count in league_counts.items():
        print(f"  League {league}: {count} teams")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_and_analyze_data(
        interim_file=os.path.join(base_dir, "data", "interim", "hockey_teams.json"),
        output_file=os.path.join(base_dir, "data", "processed", "hockey_teams.csv")
    )

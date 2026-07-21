import numpy as np
import pandas as pd
from scipy.stats import poisson
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class HockeyPredictorML:
    """
    Predictive ML model for hockey team matchups using historical stats, 
    rolling form averages, classification algorithms, Poisson goal distribution, 
    and betting value analytics (Kelly Criterion & Expected Value).
    """
    def __init__(self):
        self.scaler = StandardScaler()
        self.log_reg = LogisticRegression(random_state=42)
        self.rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False

    @staticmethod
    def calculate_kelly_and_ev(p, market_odd, bankroll=10000.0, kelly_fraction=0.5):
        """
        Calculates Expected Value (EV %) and recommended Kelly Criterion bet size.
        """
        if market_odd <= 1.0 or p <= 0:
            return {"ev_pct": 0.0, "kelly_pct": 0.0, "recommended_stake": 0.0}
            
        # Expected Value: EV = (p * odd - 1) * 100%
        ev_pct = (p * market_odd - 1.0) * 100.0
        
        # Kelly Criterion: f* = (p * b - (1 - p)) / b = (p * odd - 1) / (odd - 1)
        b = market_odd - 1.0
        kelly_full = (p * market_odd - 1.0) / b if b > 0 else 0.0
        kelly_pct = max(0.0, kelly_full * kelly_fraction * 100.0)
        recommended_stake = (bankroll * (kelly_pct / 100.0))
        
        return {
            "ev_pct": ev_pct,
            "kelly_pct": kelly_pct,
            "recommended_stake": recommended_stake
        }

    def predict_over_under(self, df, team_a, team_b, threshold=5.5):
        """
        Predicts Over/Under goal probabilities using Poisson Distribution based on team scoring averages.
        """
        # Average goals scored per match (assuming 82 games or average seasonal pace)
        # Average goals per season / 82 matches
        df_feat = self.prepare_features(df)
        latest = df_feat.groupby('team').last().reset_index()
        
        t1_rows = latest[latest['team'] == team_a]
        t2_rows = latest[latest['team'] == team_b]
        
        if t1_rows.empty or t2_rows.empty:
            return {
                "lambda_a": 2.5, "lambda_b": 2.5, "lambda_total": 5.0,
                "prob_under": 0.5, "prob_over": 0.5, "odd_under": 2.0, "odd_over": 2.0
            }
            
        t1 = t1_rows.iloc[0]
        t2 = t2_rows.iloc[0]
        
        # Convert seasonal goals to per-game estimates (~82 matches)
        # Goal expectations lambda: (scored_by_team + received_by_opponent) / (2 * matches)
        avg_matches = 82.0
        lambda_a = max(0.5, (t1['rolling_scored_goals'] + t2['rolling_received_goals']) / (2.0 * avg_matches))
        lambda_b = max(0.5, (t2['rolling_scored_goals'] + t1['rolling_received_goals']) / (2.0 * avg_matches))
        
        # Adjust for home ice advantage (+5% goals for home team)
        lambda_a = lambda_a * 1.05
        lambda_total = lambda_a + lambda_b
        
        # Poisson CDF for Under (floor of threshold, e.g. 5 goals for 5.5 threshold)
        k_threshold = int(np.floor(threshold))
        prob_under = poisson.cdf(k_threshold, lambda_total)
        prob_over = 1.0 - prob_under
        
        prob_under = max(0.01, min(0.99, prob_under))
        prob_over = max(0.01, min(0.99, prob_over))
        
        return {
            "lambda_a": lambda_a,
            "lambda_b": lambda_b,
            "lambda_total": lambda_total,
            "prob_under": prob_under,
            "prob_over": prob_over,
            "odd_under": 1.0 / prob_under,
            "odd_over": 1.0 / prob_over
        }

        
    def prepare_features(self, df):
        """
        Engineers rolling form features and team level metrics.
        """
        df_sorted = df.sort_values(['team', 'season']).copy()
        
        # Calculate overall victory percentage per team if not present
        if 'overall_victory_percentage' not in df_sorted.columns:
            df_sorted['overall_victory_percentage'] = df_sorted.groupby('team')['victory_percentage'].transform('mean')

        # Calculate 3-season rolling averages for team form
        df_sorted['rolling_win_pct'] = df_sorted.groupby('team')['victory_percentage'].transform(
            lambda x: x.rolling(window=3, min_periods=1).mean()
        )

        df_sorted['rolling_scored_goals'] = df_sorted.groupby('team')['scored_goals'].transform(
            lambda x: x.rolling(window=3, min_periods=1).mean()
        )
        df_sorted['rolling_received_goals'] = df_sorted.groupby('team')['received_goals'].transform(
            lambda x: x.rolling(window=3, min_periods=1).mean()
        )
        df_sorted['rolling_goal_diff'] = df_sorted.groupby('team')['goal_difference'].transform(
            lambda x: x.rolling(window=3, min_periods=1).mean()
        )
        
        return df_sorted

    def train(self, df):
        """
        Trains Logistic Regression and Random Forest models on pairwise team comparisons.
        """
        df_feat = self.prepare_features(df)
        
        # Get latest team form features
        latest_team_stats = df_feat.groupby('team').last().reset_index()
        
        # Create synthetic pairwise match samples for training
        X_samples = []
        y_samples = []
        
        teams = latest_team_stats['team'].unique()
        for i in range(len(teams)):
            for j in range(len(teams)):
                if i != j:
                    t1 = latest_team_stats[latest_team_stats['team'] == teams[i]].iloc[0]
                    t2 = latest_team_stats[latest_team_stats['team'] == teams[j]].iloc[0]
                    
                    # Feature vector: differences in win pct, goal diff, rolling win pct, scored goals
                    diff_win_pct = t1['victory_percentage'] - t2['victory_percentage']
                    diff_goal_diff = t1['goal_difference'] - t2['goal_difference']
                    diff_roll_win_pct = t1['rolling_win_pct'] - t2['rolling_win_pct']
                    diff_roll_goals = t1['rolling_scored_goals'] - t2['rolling_scored_goals']
                    
                    feat = [diff_win_pct, diff_goal_diff, diff_roll_win_pct, diff_roll_goals]
                    
                    # Target: 1 if Team 1 higher overall win pct, else 0
                    target = 1 if t1['overall_victory_percentage'] > t2['overall_victory_percentage'] else 0
                    
                    X_samples.append(feat)
                    y_samples.append(target)
                    
        X = np.array(X_samples)
        y = np.array(y_samples)
        
        # Fit scaler and models
        X_scaled = self.scaler.fit_transform(X)
        self.log_reg.fit(X_scaled, y)
        self.rf_clf.fit(X_scaled, y)
        self.is_trained = True

    def predict_matchup(self, df, team_a, team_b, home_advantage_pct=5.0, goalie_impact_pct=0.0):
        """
        Predicts win probabilities using Historical Baseline, Form-Weighted Rolling, 
        Logistic Regression, and Random Forest models, factoring in Home Ice Advantage 
        and Goalie/Absence modifiers.
        """
        df_feat = self.prepare_features(df)
        latest_stats = df_feat.groupby('team').last().reset_index()
        
        # Get team records
        t1_rows = latest_stats[latest_stats['team'] == team_a]
        t2_rows = latest_stats[latest_stats['team'] == team_b]
        
        if t1_rows.empty or t2_rows.empty:
            return {"baseline": (0.5, 0.5), "form": (0.5, 0.5), "logreg": (0.5, 0.5), "rf": (0.5, 0.5)}
            
        t1 = t1_rows.iloc[0]
        t2 = t2_rows.iloc[0]
        
        # 1. Baseline Historical Model
        h1 = t1['overall_victory_percentage']
        h2 = t2['overall_victory_percentage']
        denom_h = h1 + h2 if (h1 + h2) > 0 else 1.0
        prob_base_a = h1 / denom_h
        prob_base_b = h2 / denom_h
        
        # 2. Form-Weighted Rolling Average Model (Recent 3 seasons)
        f1 = t1['rolling_win_pct']
        f2 = t2['rolling_win_pct']
        denom_f = f1 + f2 if (f1 + f2) > 0 else 1.0
        prob_form_a = f1 / denom_f
        prob_form_b = f2 / denom_f
        
        # Train ML if not trained
        if not self.is_trained:
            self.train(df)
            
        # 3. ML Feature vector for team_a vs team_b
        diff_win_pct = t1['victory_percentage'] - t2['victory_percentage']
        diff_goal_diff = t1['goal_difference'] - t2['goal_difference']
        diff_roll_win_pct = t1['rolling_win_pct'] - t2['rolling_win_pct']
        diff_roll_goals = t1['rolling_scored_goals'] - t2['rolling_scored_goals']
        
        feat = np.array([[diff_win_pct, diff_goal_diff, diff_roll_win_pct, diff_roll_goals]])
        feat_scaled = self.scaler.transform(feat)
        
        # Logistic Regression Prediction
        probs_logreg = self.log_reg.predict_proba(feat_scaled)[0]
        prob_logreg_a = probs_logreg[1]
        prob_logreg_b = probs_logreg[0]
        
        # Random Forest Prediction
        probs_rf = self.rf_clf.predict_proba(feat_scaled)[0]
        prob_rf_a = probs_rf[1]
        prob_rf_b = probs_rf[0]
        
        # Helper to apply Home Ice Advantage and Goalie Impact factors and normalize
        def adjust_factors(p_a, p_b):
            p_a_adj = p_a * (1.0 + home_advantage_pct / 100.0) * (1.0 + goalie_impact_pct / 100.0)
            p_b_adj = p_b
            total_p = p_a_adj + p_b_adj if (p_a_adj + p_b_adj) > 0 else 1.0
            return (p_a_adj / total_p, p_b_adj / total_p)
        
        return {
            "baseline": adjust_factors(prob_base_a, prob_base_b),
            "form": adjust_factors(prob_form_a, prob_form_b),
            "logreg": adjust_factors(prob_logreg_a, prob_logreg_b),
            "rf": adjust_factors(prob_rf_a, prob_rf_b)
        }


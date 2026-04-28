from sklearn.linear_model import LogisticRegressionCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.calibration import CalibratedClassifierCV

def build_log_regression():

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    model = LogisticRegressionCV(
        l1_ratios=(1,),
        solver='saga',
        cv=cv,
        scoring='roc_auc',
        class_weight='balanced',
        max_iter=1000,
        use_legacy_attributes=False
    )
    calibrated_model = CalibratedClassifierCV(model, method='sigmoid')

    return calibrated_model

def build_decision_tree():
    tree = DecisionTreeClassifier(
        max_depth=3,
        min_samples_leaf=15,
        class_weight='balanced',
        criterion='gini',
        random_state=42
    )
    return tree


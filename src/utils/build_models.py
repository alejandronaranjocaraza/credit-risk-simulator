from sklearn.linear_model import LogisticRegressionCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.calibration import CalibratedClassifierCV


def build_model(name: str()):

    builders = {
        'log-regression-cv': lambda: build_log_regression_cv(),
        'decision-tree': lambda: build_decision_tree()
    }
    if name not in builders:
        raise ValueError("Unkown model: "+name+".")
    return builders[name]()


def build_log_regression_cv(calibrate=True, max_iter=5000):

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    model = LogisticRegressionCV(
        l1_ratios=(1,),
        solver='saga',
        cv=cv,
        scoring='roc_auc',
        class_weight='balanced',
        max_iter=max_iter,
        use_legacy_attributes=False
    )
    if calibrate:
        res = CalibratedClassifierCV(model, method='sigmoid')
    else:
        res = model
    return res


def build_decision_tree(calibrate=True):
    tree = DecisionTreeClassifier(
        max_depth=3,
        min_samples_leaf=15,
        class_weight='balanced',
        criterion='gini',
        random_state=42
    )
    if calibrate:
        res = CalibratedClassifierCV(tree, method='sigmoid')
    else:
        res = tree
    return res

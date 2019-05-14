from sklearn.ensemble import IsolationForest


def train_isolation_forest(training_data):
    clf = IsolationForest(max_samples=300, contamination=0, behaviour='new')
    clf.fit(training_data)
    return clf

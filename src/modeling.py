from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import ExtraTreesClassifier
from src.wikipedia_corpora_tools import WikipediaDfGenerator


def train_model(x_train, y_train):
    """
    Joins all the features together, and trains the model, all using sklearn methods
    :param x_train: training data (list of sentences)
    :param y_train: training label (list)
    """
    vectorizer = TfidfVectorizer(ngram_range=(1,1))
    svd = TruncatedSVD(30)
    clf = ExtraTreesClassifier(n_estimators=3000, class_weight="balanced", max_depth=15, random_state=655321)

    svd_pipe = Pipeline([("tfidf", vectorizer), ("svd", svd)])
    fu = FeatureUnion([("svd", svd_pipe), 
                       ("en", WikipediaDfGenerator(u"enwiki", 10)),
                       ("nl", WikipediaDfGenerator(u"nlwiki", 10)), 
                       ("af", WikipediaDfGenerator(u"afwiki", 10))])
    pipeline = Pipeline([("features", fu), ("clf", clf)])
    model = pipeline.fit(x_train, y_train)
    return model
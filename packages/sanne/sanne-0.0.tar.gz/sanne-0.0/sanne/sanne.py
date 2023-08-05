import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import sqrt
from sklearn.metrics import mean_squared_error
from typing import Union
from sklearn.metrics import accuracy_score, recall_score, confusion_matrix, roc_auc_score, precision_recall_curve, f1_score, cohen_kappa_score, roc_curve, auc
from scikitplot.metrics import plot_roc
from sklearn import metrics
from sklearn.model_selection import learning_curve
import typing


def validation_metrics_lgbm(model, y_valid, y_pred):
    rmse = mean_squared_error(y_valid, y_pred, squared=False)
    df_plot = y_valid.copy()
    df_plot['y_pred'] = y_pred
    print(f" LightGBM RMSE: {rmse}")
    plt.figure(1)
    sns.scatterplot(x=df_plot['scrap_rate'], y=df_plot['y_pred'])
    plt.title('Correlation between Actual Scrap Rate and LGBM Predicted Scrap Rate')
    plt.xlabel('Actual Scrap Rate (Validation set)')
    plt.ylabel('LGBM Prediction')
    plt.show()
    plt.figure(2)
    plot_metric(model)
    plt.show()
    df_plot['error'] = df_plot['scrap_rate'] - df_plot['y_pred']
    plt.figure(3)
    plt.hist(df_plot['error'])
    plt.title("Distribution of the error")
    plt.show()


def validation_metrics(y_valid, y_pred):
    rmse = mean_squared_error(y_valid, y_pred, squared=False)
    print(f" Model RMSE: {rmse}")
    df_plot = pd.DataFrame(y_valid.copy())
    df_plot['y_pred'] = y_pred
    plt.figure(1)
    sns.scatterplot(x=df_plot['scrap_rate'], y=df_plot['y_pred'])
    plt.title('Correlation between Actual Scrap Rate and LGBM Predicted Scrap Rate')
    plt.xlabel('Actual Scrap Rate (Validation set)')
    plt.ylabel('LGBM Prediction')
    plt.show()
    df_plot['error'] = df_plot['scrap_rate'] - df_plot['y_pred']
    plt.figure(2)
    plt.hist(df_plot['error'])
    plt.title("Distribution of the error")
    plt.show()


def plot_learning_curve(estimator, title, X, y, cv=None, n_jobs=None):
    train_sizes, train_scores, test_scores, fit_times, score_times = learning_curve(estimator, X, y, cv, n_jobs, return_times=True)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    fit_times_mean = np.mean(fit_times, axis=1)
    fit_times_std = np.std(fit_times, axis=1)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    plt.grid()
    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1,
                     color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")
    plt.legend(loc="best")
    plt.show()
    return plt

def learning_curves(estimator, data, features, target, train_sizes, cv):
    train_sizes, train_scores, validation_scores = learning_curve(
    estimator, data[features], data[target], train_sizes = train_sizes,
    cv = cv, scoring = 'neg_mean_squared_error')
    train_scores_mean = -train_scores.mean(axis = 1)
    validation_scores_mean = -validation_scores.mean(axis = 1)

    plt.plot(train_sizes, train_scores_mean, label = 'Training error')
    plt.plot(train_sizes, validation_scores_mean, label = 'Validation error')
    plt.ylabel('MSE', fontsize = 14)
    plt.xlabel('Training set size', fontsize = 14)
    title = 'Learning curves for a ' + str(estimator).split('(')[0] + ' model'
    plt.title(title, fontsize = 18, y = 1.03)
    plt.legend()
    plt.ylim(0,40)


def complete_preprocessing(df, cat_cols):
    other_preprocessing(df)
    type_category(df, cat_cols)



def other_preprocessing(df):
    '''Specific for the E&M Scrap rate case'''
#     df.loc[df['engine_oil_type'].isna(), 'engine_oil_type'] = df.groupby(['engine_type', 'engine_configuration_nr'])['engine_oil_type'].transform(lambda x: x.mode()[0] if any(x.mode()) else 'ALL_NAN')
#     df.loc[df['existing_customer_name'].isna(), 'existing_customer_name'] = 'Unknown'
#     df.loc[df['region'].isna(), 'region'] = df.groupby(['existing_customer_name'])['region'].transform(lambda x: x.mode()[0] if any(x.mode()) else 'ALL_NAN')
#     df.loc[df['engine_removal'].isna(), 'engine_removal'] = df.groupby(['engine_type', 'engine_configuration_nr', 'engine_oil_type'])['engine_removal'].transform(lambda x: x.mode()[0] if any(x.mode()) else 'ALL_NAN')
#     df.loc[df['fuel'].isna(), 'fuel'] = 'NORMAL'
#     df['av_flighttime_lastvisit'] = df['tslv_engine']/df['cslv_engine']
#     df['av_flighttime_lastvisit'] = df['av_flighttime_lastvisit'].fillna(df['av_flighttime_lastvisit'].mean())
    df['relocation_date'] = pd.to_datetime(df['relocation_date'])
    df.sort_values(by='relocation_date')
    df['engine_position'] = df['engine_position'].astype('category')
    df["scrap_amount"] = (df["quantity"] * df["scrap_rate"]) /100
    df['scrap_rate_log'] = np.log1p(df['scrap_rate'])
    df['scrap_amount_log'] = np.log1p(df['scrap_amount'])
    Mean_encoded_subject = df.groupby(['cdp'])['scrap_rate'].mean().to_dict()
    df['cdp_mean_enc'] =  df['cdp'].map(Mean_encoded_subject)
    df['cdp_target_enc'] = df['cdp'].copy()

    return df

def specific_dtime(df, date_time_column):
    df[date_time_column] = pd.to_datetime(df[date_time_column])
    df['week'] = df[date_time_column].dt.week
    df['month'] = df[date_time_column].dt.month
    return df


def cyclical_encoding(df: pd.DataFrame, col: str, max_val: int) -> pd.DataFrame:
    df[col + '_sin'] = np.sin(2 * np.pi * df[col]/max_val)
    df[col + '_cos'] = np.cos(2 * np.pi * df[col]/max_val)
    return df


def cyclical_features_scraprate(df: pd.DataFrame) -> pd.DataFrame:
    df = cyclical_encoding(df, 'week', 52)
    df = cyclical_encoding(df, 'month', 12)
    df.drop(['week', 'month'], axis=1, inplace=True)
    return df

def season(df, date_time_column):
    seasons = [1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 1]
    month_to_season = dict(zip(range(1,13), seasons))
    df['season'] = df[date_time_column].dt.month.map(month_to_season)



def print_columns(df: pd.DataFrame) -> str:
    for col in df.columns:
        print(f"'{col}' : '', ")

def rename_columns(df: pd.DataFrame, columns_dict: typing.Dict[str, str]) -> pd.DataFrame:
    df.rename(columns=columns_dict, inplace=True)
    return df.head(1)

def parse_dates(df: pd.DataFrame, columns: typing.List[str]) -> pd.DataFrame:
    for col in columns:
        df[col] = pd.to_datetime(df[col])
    return df

def parse_dates_utc(df: pd.DataFrame, columns: typing.List[str]) -> pd.DataFrame:
    for col in columns:
        df[col] = pd.to_datetime(df[col], utc=True)
    return df

def fillna_zeros(df: pd.DataFrame, columns: typing.List[str]) -> pd.DataFrame:
    for col in columns:
        df[col] = df[col].fillna(0)
    return df

def type_int(df: pd.DataFrame, columns: typing.List[str]) -> pd.DataFrame:
    for col in columns:
        df[col] = df[col].astype(int)
    return df


def type_float(df: pd.DataFrame, columns: typing.List[str]) -> pd.DataFrame:
    for col in columns:
        df[col] = df[col].astype(float)
    return df


def type_category(df: pd.DataFrame, columns: typing.List[str]) -> pd.DataFrame:
    for col in columns:
        df[col] = df[col].astype('category')


def drop_features(df: pd.DataFrame, columns: typing.List[str]) -> pd.DataFrame:
    df.drop([columns], axis=1, inplace=True)
    return df


def sort_by_date(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    df.sort(date_column)
    df.sort_values(by=date_column)
    return df


def show_correlations(df: pd.DataFrame, outcome: str, k: int = 10) -> pd.Series:
    ''' Takes a Pandas DataFrame (df), an outcome variable to see the correlation of, a number k of the number of largest correlations. And returns a correlation matrix. '''
    corrmat = df.corr()
    return corrmat.nlargest(k, outcome)[outcome]


def corr_matrix(df: pd.DataFrame, outcome: str, k: int = 10) -> None:
    corrmat = df.corr()
    cols = corrmat.nlargest(k, outcome)[outcome].index
    cm = np.corrcoef(df[cols].values.T)
    fig, ax = plt.subplots(figsize=(10,10))
    sns.set(font_scale=1.25)
    hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 13}, yticklabels=cols.values, xticklabels=cols.values)
    plt.show()



def missing_value_percentage(df: pd.DataFrame, k: int) -> float:
    '''Takes a Pandas DataFrame (df) and shows the 20 columns with highest % of missing values in descending order'''
    total = df.isnull().sum().sort_values(ascending=False)
    percent = (df.isnull().sum() / df.isnull().count()).sort_values(ascending=False)
    missing_data = pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
    return missing_data.head(k)

def find_cat_vars(df: pd.DataFrame) -> str:
    '''Finds all columns with dtype 'object' or 'category' in a dataframe'''
    s = (df.dtypes == 'object') | (df.dtypes == 'category')
    object_cols = list(s[s].index)
    print("Categorical variables:")
    print(object_cols)

def find_num_vars(df: pd.DataFrame) -> str:
    '''Finds all columns with dtype 'int' or 'float' in a dataframe'''
    k = (df.dtypes == 'int32') | (df.dtypes == 'int64') | (df.dtypes == 'float')
    object_cols = list(k[k].index)
    print("Numerical variables:")
    print(object_cols)

def print_num_cat(df: pd.DataFrame) -> typing.List[str]:
    '''Print out all numeric columns'''
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    numeric_df = df.select_dtypes(include=numerics)
    print('Numeric columns: ')
    print(numeric_df.columns)
    categorical = ['category', 'object']
    categorical_df = df.select_dtypes(include=categorical)
    print('Categorical columns: ')
    print(categorical_df.columns)
    date = ['datetime64[ns]', 'datetime64[ns, UTC]']
    date_df = df.select_dtypes(include=date)
    print('Date columns: ')
    print(date_df.columns)


def pivot_table(df: pd.DataFrame, groupby_var: str, show_var: str) -> pd.DataFrame:
    ''' Make a pivot table grouped by to show if difference between groups '''
    return df[[groupby_var, show_var]].groupby([groupby_var], as_index=False).mean().sort_values(by=groupby_var, ascending=False)


def show_histograms(df: pd.DataFrame):
    fig = plt.figure(figsize=(20, 20))
    ax = fig.gca()
    df.hist(edgecolor="black", grid=True, ax=ax)

def box_plot(df: pd.DataFrame, outcome: str, column: str):
    var = column
    data =  pd.concat([df[outcome], df[var]], axis=1)
    f, ax = plt.subplots(figsize=(8, 6))
    fig = sns.boxplot(x=var, y=outcome, data=df)
    return fig


def train_test_date_split(
    df,
    date_column,
    split_date="2018-01-01",
    train_size=1.0,
    test_size=1.0,
    bootstrap=False,
    seed=1984,
):
    """
    Split the data into a train set and a test set by date.
    :param df: input dataframe
    :param split_date: the date on which to split. All rows on or after this date are included in the test set
    :param train_size: fraction of train data to return (default 1.0)
    :param test_size: fraction of test data to return (default 1.0)
    :param bootstrap: if True, will sample with replacement on the test data. (default False)
    :param seed: random seed to use (default 1984, set to None to use system seed)
    :return: (train, test) tuple of data frames
    """
    df[date_column] = pd.to_datetime(df[date_column])
    df = df.sort_values(by=date_column)
    date = pd.to_datetime(split_date)
    train = df[df[date_column] < date].sample(frac=train_size, random_state=seed)
    test = (
        df[df[date_column] >= date]
        .sample(frac=test_size, random_state=seed, replace=bootstrap)
        .reset_index(drop=True)
    )
    print(
        "Train data size of {}, test data size of {}, split after date {}.".format(
            len(train), len(test), date.date()
        )
    )

    return train, test


def create_time_features(df: pd.DataFrame, date_time_column: str) -> pd.DataFrame:
    df['hour'] = df[date_time_column].datetime.dt.hour
    df['day'] = df[date_time_column].datetime.dt.day
    df['week'] = df[date_time_column].datetime.isocalendar().week
    df['month'] = df[date_time_column].datetime.dt.month
    df['dayof_week'] = df[date_time_column].dt.dayofweek
    df['dayof_year'] = df[date_time_column].dt.dayofyear
    df['year'] = df[date_time_column].dt.year
    return df


def cyclical_encoding(df: pd.DataFrame, col: str, max_val: int) -> pd.DataFrame:
    df[col + '_sin'] = np.sin(2 * np.pi * df[col]/max_val)
    df[col + '_cos'] = np.cos(2 * np.pi * df[col]/max_val)
    return df


def create_cyclical_features(df: pd.DataFrame) -> pd.DataFrame:
    df = cyclical_encoding(df, 'hour', 24)
    df = cyclical_encoding(df, 'day', 31)
    df = cyclical_encoding(df, 'week', 52)
    df = cyclical_encoding(df, 'month', 12)
    df = cyclical_encoding(df, 'dayof_week', 7)
    df = cyclical_encoding(df, 'dayof_year', 365)
    df = cyclical_encoding(df, 'year', 2021)
    df.drop(['hour', 'day', 'week', 'month', 'dayof_week', 'dayof_year', 'year'], axis=1, inplace=True)
    return df



def write_predictions_to_csv(
    predictions: Union[pd.DataFrame, np.ndarray],
    teamname: str,
    predictions_column: str = None,
) -> None:
    """Writes the predictions to a final .csv file for evaluation. If passed a pd.DataFrame and `predictions_column`,
    this column is first moved to the last place.
    In case a `np.ndarray` is passed, nothing is changed to the structure.
    Args:
        predictions Union[pd.DataFrame, np.ndarray]: The predictions, either in pd.DataFrame or np.ndarray format
        teamname (str): Name of participating team, will be used as the filename
        predictions_column (str, optional): Name of the column that contains the predictions
    Returns:
        Tuple[str, pd.Series]: teamname, predictions
    """
    filename = teamname + ".csv"
    if isinstance(predictions, pd.DataFrame):
        predictions_df = move_column_to_last_place(predictions, predictions_column)
        predictions_df.to_csv(filename)
    if isinstance(predictions, np.ndarray):
        pd.DataFrame(predictions).to_csv(filename)


def move_column_to_last_place(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Moves specified column to the last  (i.e. most right) place in the DataFrame.
    Args:
        df (pd.DataFrame): DataFrame to place column in
        column_name (str): Column name of `df` to move to the last place
    Returns:
        new_df (pd.DataFrame): DataFrame with specified column moved to the last place
    """
    new_df = df[[col for col in df.columns if col != column_name] + [column_name]]
    return new_df

def feature_importance(model, X_train: pd.Series):
    '''Input is model (should be random forest / decision tree / gradient boosting / Extra tree / extra trees / ada boost) output is printed table of feature importance values per feature for the top 10. And a plot of the feature importance'''
    feature_importances = pd.DataFrame(model.feature_importances_,index = X_train.columns, columns=['importance']).sort_values('importance',ascending=False)
    print(feature_importances['importance'].nlargest(10))
    #plot feature importance
    feat_importances = pd.Series(model.feature_importances_, index=X_train.columns)
    feat_importances.nlargest(10).plot(kind='barh')
    plt.show()


def classification_metrics(y_true, Y_pred):
    cm = confusion_matrix(y_true, Y_pred)
    tn, fp, fn, tp = cm.ravel()
    print('Amount of True Negatives: ', tn)
    print('Amount of False Positives: ', fp)
    print('Amount of False Negatives: ', fn)
    print('Amount of True Positives: ', tp)

    # True positive rate, sensitivity, recall
    tpr = tp / (tp + fn)
    print('\nTrue positive rate  (Recall/Sensitivity): {0:0.4f}'.format(tpr))
    # True negative rate, specificity
    tnr = tn / (tn + fp)
    print('True negative rate (Specificity: {0:0.4f}'.format(tnr))
    # Precision or positive predictive value
    ppv = tp / (tp + fp)
    print('Precision: {0:0.4f}'.format(ppv))

     # False positive rate or fall out
    fpr = fp / (fp + tn)
    print('\nFalse positive rate: {0:0.4f}'.format(fpr))
    # False negative rate
    fnr = fn / (tp + fn)
    print('False negative rate: {0:0.4f}'.format(fnr))
    # False discovery rate
    fdr = fp / (tp + fp)
    print('False discovery rate: {0:0.4f}'.format(fdr))
    # Negative predictive value
    npv = tn / (tn +fn)
    print('Negative predictive value: {0:0.4f}'.format(npv))

    # Accuracy score
    accuracy = accuracy_score(y_true, Y_pred)
    print('\nAccuracy score: {0:0.4f}'.format(accuracy))

    roc_auc = roc_auc_score(y_true, Y_pred)
    print('\nROC AUC score is: {0:0.4f}'.format(roc_auc))
    print('\nConfusion matrix: \n', cm)


def plot_roc_curve(fpr, tpr):
    plt.plot(fpr, tpr, color='orange', label='ROC')
    plt.plot([0, 1], [0, 1], color='darkblue', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend()
    plt.show()

def plot_precision_recall_curve(recall, precision):
    plt.plot(recall, precision, color='orange', label='Model')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend()
    plt.show()

def to_labels(pos_probs, threshold):
    return (pos_probs >= threshold).astype('int')

def threshold_tuning(model, X_validation, y_validation):
    '''  Tuning threshold for synthetic imbalanced classification: define set of thresholds, evaluate predicted probabilities, select the optimal threshold, use F scores '''
    probs = model.predict_proba(X_validation)
    probs = probs[:, 1]
    thresholds = np.arange(0, 1, 0.001)
    scores = [f1_score(y_validation, to_labels(probs, t)) for t in thresholds]
    ix = np.argmax(scores)
    print('Threshold=%.3f, F-Score=%.5f' % (thresholds[ix], scores[ix]))

def threshold_tuning_ROC(model, X_validation, y_validation):
    '''Threshold tuning with ROC AUC scores, using G-means and Youden's J statistic'''
    probs = model.predict_proba(X_validation)
    probs = probs[:, 1]
    auc = roc_auc_score(y_validation, probs)
    print('AUC: %.2f' % auc)
    fpr, tpr, thresholds = roc_curve(y_validation, probs)
    gmeans = np.sqrt(tpr * (1-fpr).astype(int))
    ix = np.argmax(gmeans)
    print('Best Threshold G-Mean=%f, G-Mean=%.3f' % (thresholds[ix], gmeans[ix]))
    J = tpr - fpr
    ix = np.argmax(J)
    best_thresh = thresholds[ix]
    print('Best Threshold Youden’s J statistic =%f' % (best_thresh))

def threshold_tuning_ROC_plot(model, X_validation, y_validation):
    '''Threshold tuning with ROC AUC scores, using G-means and Youden's J statistic and with display in a plot'''
    probs = model.predict_proba(X_validation)
    probs = probs[:, 1]
    auc = roc_auc_score(y_validation, probs)
    print('AUC: %.2f' % auc)
    fpr, tpr, thresholds = roc_curve(y_validation, probs)
    gmeans = np.sqrt(tpr * (1-fpr).astype(int))
    ix = np.argmax(gmeans)
    print('Best Threshold G-Mean=%f, G-Mean=%.3f' % (thresholds[ix], gmeans[ix]))
    J = tpr - fpr
    ix = np.argmax(J)
    best_thresh = thresholds[ix]
    print('Best Threshold Youden’s J statistic =%f' % (best_thresh))
    plt.plot([0,1], [0,1], linestyle='--', label='Worst')
    plt.plot(fpr, tpr, marker='.', label='Model')
    plt.scatter(fpr[ix], tpr[ix], marker='o', color='black', label='Best')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend()
    plt.show()

def ROC_threshold_plot(model, X_validation, y_validation):
    '''Threshold tuning with ROC AUC scores, using G-means and Youden's J statistic and with display in 3 plots with
    1: tpr - fpr
    2: for every threshold the tpr plot
    3: for every threshold the fpr plot'''
    probs = model.predict_proba(X_validation)
    probs = probs[:, 1]
    auc = roc_auc_score(y_validation, probs)
    print('AUC: %.2f' % auc)
    fpr, tpr, thresholds = roc_curve(y_validation, probs)
    gmeans = np.sqrt(tpr * (1-fpr).astype(int))
    ix = np.argmax(gmeans)
    print('Best Threshold G-Mean=%f, G-Mean=%.3f' % (thresholds[ix], gmeans[ix]))
    J = tpr - fpr
    ix = np.argmax(J)
    best_thresh = thresholds[ix]
    print('Best Threshold Youden’s J statistic =%f' % (best_thresh))
    plt.figure(1)
    plt.plot([0,1], [0,1], linestyle='--', label='Worst')
    plt.plot(fpr, tpr, marker='.', label='Model')
    plt.scatter(fpr[ix], tpr[ix], marker='o', color='black', label='Best')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend()
    plt.show()
    plt.figure(2)
    plt.plot(thresholds, tpr, marker='.', label='TPR')
    plt.xlabel('Thresholds')
    plt.ylabel('True Positive Rate')
    plt.legend()
    plt.show()
    plt.figure(3)
    plt.plot(thresholds, fpr, marker='.', label='FPR')
    plt.xlabel('Thresholds')
    plt.ylabel('False Positive Rate')
    plt.legend()
    plt.show()

def threshold_tuning_precision_recall(model, X_validation, y_validation, Y_pred):
    '''Threshold tuning with Precision-Recall Curves, using F scores to get optimal threshold'''
    probs = model.predict_proba(X_validation)
    probs = probs[:, 1]
    precision, recall, thresholds = precision_recall_curve(y_validation, probs)
    f1 = f1_score(y_validation, Y_pred)
    auc = metrics.auc(recall, precision)
    print('Model: f1=%.3f auc=%.3f' % (f1, auc))
    fscore = (2 * precision * recall) / (precision + recall)
    ix = np.argmax(fscore)
    print('Best Threshold=%f, F-Score=%.3f' % (thresholds[ix], fscore[ix]))

def threshold_tuning_precision_recall_plot(model, X_validation, y_validation, Y_pred):
    '''Threshold tuning with Precision-Recall Curves, using F scores to get optimal threshold and with display in a plot'''
    probs = model.predict_proba(X_validation)
    probs = probs[:, 1]
    precision, recall, thresholds = precision_recall_curve(y_validation, probs)
    f1 = f1_score(y_validation, Y_pred)
    auc = metrics.auc(recall, precision)
    print('Model: f1=%.3f auc=%.3f' % (f1, auc))
    fscore = (2 * precision * recall) / (precision + recall)
    ix = np.argmax(fscore)
    print('Best Threshold=%f, F-Score=%.3f' % (thresholds[ix], fscore[ix]))
    plt.plot(recall, precision, color='orange', label='Precision-Recall Curve')
    plt.scatter(recall[ix], precision[ix], marker='o', color='black', label='Best')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.legend(loc=3)
    plt.show()



def determine_nbr_knn(X_train, y_train, X_test, y_test):
    '''Plots a graph that shows model accuracy for number of neighbors in range (1,30)'''
    k_range = range(1,30)
    scores = []
    for k in k_range:
        knn = kNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
        scores.append(accuracy_score(y_test, y_pred))
    plt.plot(k_range, scores)
    plt.xlabel('Value of k for KNN')
    plt.ylabel('Testing Accuracy')

def determine_max_leaf_nodes(max_leaf_nodes, X_train, X_test, y_train, y_test):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(X_train, y_train)
    preds_val = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds_val)
    return(mae)

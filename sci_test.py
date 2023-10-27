import pandas as pd
import numpy as np
from sklearn.compose import make_column_selector as selector
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_validate
from sklearn.metrics import PredictionErrorDisplay
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_predict

# 0.0031265358167257284
# The mean cross-validation accuracy is: 0.001 ± 0.011

data = pd.read_csv("/Users/emmaeescandon/CS229/project/sample_data_large.csv")

data.drop(['id', 'name', 'start_date', 'end_date', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun', 'end_year', 'end_month', 'end_day_of_year', 'FIRE_SIZE_CLASS' ],  axis=1, inplace=True)
data.drop(data.columns[0], axis=1, inplace = True)

target_name = "size"
target = data[target_name]

Y = data.loc[:, ~data.columns.isin(['cause', 'state'])]
print(Y)
imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean')
imputed_DF = pd.DataFrame(imp_mean.fit_transform(Y))
imputed_DF.columns = Y.columns
imputed_DF.index = Y.index
    
Y = imputed_DF
print(Y)

extracted_col = data["cause"] 
Y = Y.join(extracted_col) 
extracted_col2 = data["state"] 
Y = Y.join(extracted_col2) 

data = Y
print(data)

data.drop(columns=[target_name],inplace=True)


#one-hot encoder for causes and state
numerical_columns_selector = selector(dtype_exclude=object)
categorical_columns_selector = selector(dtype_include=object)

numerical_columns = numerical_columns_selector(data)
categorical_columns = categorical_columns_selector(data)

categorical_preprocessor = OneHotEncoder(handle_unknown="ignore")
numerical_preprocessor = StandardScaler()

preprocessor = ColumnTransformer(
    [
        ("one-hot-encoder", categorical_preprocessor, categorical_columns),
        ("standard_scaler", numerical_preprocessor, numerical_columns),
    ]
)

model = make_pipeline(preprocessor, LinearRegression())
model

data_train, data_test, target_train, target_test = train_test_split(
    data, target, test_size=0.3
)
_ = model.fit(data_train, target_train)

data_test.head()
model.predict(data_test)[:5]

target_test[:5]
print(model.score(data_test, target_test))

cv_results = cross_validate(model, data, target, cv=10)

y_pred = cross_val_predict(model, data, target, cv=10)

scores = cv_results["test_score"]
print(
    "The mean cross-validation accuracy is: "
    f"{scores.mean():.3f} ± {scores.std():.3f}"
)

y = target
fig, axs = plt.subplots(ncols=2, figsize=(8, 4))
PredictionErrorDisplay.from_predictions(
    y,
    y_pred=y_pred,
    kind="actual_vs_predicted",
    subsample=100,
    ax=axs[0],
    random_state=0,
)
axs[0].set_title("Actual vs. Predicted values")
PredictionErrorDisplay.from_predictions(
    y,
    y_pred=y_pred,
    kind="residual_vs_predicted",
    subsample=100,
    ax=axs[1],
    random_state=0,
)
axs[1].set_title("Residuals vs. Predicted Values")
fig.suptitle("Plotting cross-validated predictions")
plt.tight_layout()
plt.show()
import pandas as pd
import numpy as np
import pydotplus
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor
from sklearn import ensemble
from sklearn.ensemble import RandomForestRegressor

def trainModel():

	# Read in csv, skip first line
	df = pd.read_csv('mvp.csv')

	# Drop non-numerical values from data set
	df.drop(['Player'], axis=1, inplace=True)

	#print(df.head())

	# Separate independent and target variables
	X = df.values[:, :12]
	Y = df.values[:,12]

	# Build decision tree regressor, we will use to visualize feature importances
	dt_reg = DecisionTreeRegressor()
	dt_reg.fit(X, Y)

	# Get feature importances
	print("\nFeature importances:")
	df.drop(['Share'], axis=1, inplace=True)
	importance = dt_reg.feature_importances_
	importance = pd.DataFrame(importance, index=df.columns, columns=["Importance"])
	print(importance.sort_values('Importance', ascending=False))

	# Export decision tree as PNG file via pydotplus
	dot_data = tree.export_graphviz(dt_reg, feature_names=df.columns)
	graph = pydotplus.graphviz.graph_from_dot_data(dot_data)
	graph.write("tree.png", format="png")

	# Utilize RandomForestRegressor to make predictions
	rf = ensemble.RandomForestRegressor(n_estimators=10)
	rf.fit(X, Y)

	return rf

def predict(model):
	# We now need to use the current season data.
	prediction_df = pd.read_csv('players.csv')

	# Keep track of the players and drop from df
	playerList = prediction_df['Player'].tolist()
	prediction_df.drop(['Player'], axis=1, inplace=True)

	predictions = model.predict(prediction_df)

	# Display results
	results = {'name': playerList, 'pct': predictions}
	df = pd.DataFrame(data=results)
	df = df.sort_values(by='pct', ascending=False)

	best = df.loc[0]

	print("\nThe current MVP is...")
	print(best)

	print("")

def main():

	dt_reg = trainModel()
	predict(dt_reg)

if __name__ == "__main__":
	main()
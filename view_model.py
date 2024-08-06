# Usage `python3 view_model.py figure.pkl` to view the figure saved in `figure.pkl`.
import pickle
import matplotlib.pyplot as plt
import sys

fig = pickle.load(open(sys.argv[1], 'rb'))
plt.show()
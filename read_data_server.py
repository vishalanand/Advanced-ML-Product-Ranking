import sys, re, time, datetime, math, pickle

lambds = [0.001, 0.02, 0.1, 1.0]
ranks = [10, 20, 30, 60]
eta = 0.002

for rank in ranks:
	for lambd in lambds:
		for i in range(10):
			f_save = "output/rank_" + str(rank) + "_lambda_" + str(lambd) + "_iter_" + str(i+1) + "_step_" + str(eta) + ".pkl"
			try:
				with open(f_save, 'rb') as f:
					try:
						rank_val, lambd_val, i_val, eta_val, RMSE_train, RMSE_test, MRR = pickle.load(f)
						print(rank_val, lambd_val, i_val, RMSE_train, RMSE_test, MRR)
					except:
						print(f_save, "Empty file")
						pass
			except:
				print(f_save, "No file")

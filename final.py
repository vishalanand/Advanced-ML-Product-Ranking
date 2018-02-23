import sys, codecs, re, pdb, time, datetime, math, tqdm, pickle, numpy as np

def build_movies_dict(movies_file):
    i = 0
    movie_id_dict = {}
    with codecs.open(movies_file, 'r', 'utf-8') as f:
        for line in f:
            if i == 0:
                i = i+1
            else:
                line1 = line.split(',')
                movieId = line1[0]
                genres = line1[2][:-1]
                title = "".join(line1[1:-1])
                movie_id_dict[int(movieId)] = i-1
                i = i+1
    return movie_id_dict

def read_data(input_file,movies_dict):
    users =  138493
    movies = 27278
    i = 0
    ret = []

    prev_user = 0;
    with open(input_file,'r') as f:
        for line in f:
            if i == 0:
                i = i +1
            else:
                user,movie_id,rating,timestamp = line.split(',')
                id = movies_dict[int(movie_id)]
                cur_row = int(user) - 1
                cur_col = id
                cur_data = float(rating)
                ret.append((cur_row, cur_col, cur_data))
    return ret

def loader(test_ratings_file, train_ratings_file, movies_mapping_file, f_output_val):
    movies_dict = build_movies_dict(movies_mapping_file)
    print("Reading dicitionary", file=f_output_val, flush=True)
    test_numpy_arr = read_data(test_ratings_file,movies_dict)
    train_numpy_arr = read_data(train_ratings_file,movies_dict)
    print("Reading ratings", file=f_output_val, flush=True)
    return test_numpy_arr, train_numpy_arr

def matrix_factorization(R_train, R_test, V, W, rank, steps, lambd, eta, f_output_val):
    RMSE_old = 0.0
    for i in range(steps):
        print("Step" + str(i + 1), "\t", datetime.datetime.now().time(), file=f_output_val, flush=True)
        
        error_sum = 0.0
        for data in R_train:
            (user,movie,rating) = data
            error = rating - np.dot(V[user,:],W[movie,:])
            error_sum = error_sum + error**2
            
            V[user, :] = V[user, :] + eta * ((error * W[movie,:]) - (lambd * V[user,:]))
            W[movie, :] = W[movie, :] + eta * ((error * V[user,:]) - (lambd * W[movie,:]))

        RMSE_train = math.sqrt(error_sum / len(R_train))
        print("Train:\t", datetime.datetime.now().time(), "\t", RMSE_train, file=f_output_val, flush=True)
        
        error_sum = 0.0
        predicted_ranking=[[] for i in range(138493)]
        real_rating=[[] for i in range(138493)]
        
        for data in R_test:
            (user,movie,rating) = data
            calc_rating = np.dot(V[user,:],W[movie,:])
            
            error = rating - calc_rating
            error_sum = error_sum + error**2
            
            predicted_ranking[user].append((movie, calc_rating))
            if(rating >= 3.0):
                real_rating[user].append(movie)
        

        RMSE_test = math.sqrt(error_sum / len(R_test))
        print("Test:\t", datetime.datetime.now().time(), "\t", RMSE_test, file=f_output_val, flush=True)
        
        MRR = 0.0
        for idx, user_movies in enumerate(real_rating):
            predicted_ranking[idx].sort(key=lambda x: x[1], reverse=True)
            RR = 0.0
            for movie in user_movies:
                RR = RR + 1.0/(next((i for i, v in enumerate(predicted_ranking[idx]) if v[0] == movie), None) + 1)
            
            cnt = len(user_movies)
            if(cnt > 0):
                MRR = MRR + RR / cnt
        MRR = MRR / 138493.0
        print("MRR:\t", datetime.datetime.now().time(), "\t", MRR, "\n", file=f_output_val, flush=True)
        
        with open("output/rank_" + str(rank) + "_lambda_" + str(lambd) + "_iter_" + str(i+1) + "_step_" + str(eta) + ".pkl", 'wb') as f:
            pickle.dump([V, W, rank, lambd, i+1, eta, RMSE_train, RMSE_test, MRR], f)
        
        if(abs(RMSE_train - RMSE_old) < 0.001):
           break
        RMSE_train
        
    return V, W, RMSE_train, RMSE_test, MRR

def train_V_W(R_train, R_test, n, m, rank, steps, lambd, eta, f_output_val):
    
    V = np.random.rand(n,rank)
    W = np.random.rand(m,rank)
    est_V, est_W, RMSE_train, RMSE_test, MRR = matrix_factorization(R_train, R_test, V, W, rank, steps, lambd, eta, f_output_val)

def main():
    load_param = open('parameters.txt', "r")
    lines = load_param.read().splitlines()
    test_data = lines[0]
    train_data = lines[1]
    movie_data = lines[2]
    ranks = list(map(int, lines[3].split()))
    lambds = list(map(float, lines[4].split()))
    f_output = lines[5]
    load_param.close()
    
    n = 138493
    m = 27278
    steps=1
    eta=0.002

    f_output_val=open(f_output, 'w+')

    print(datetime.datetime.now().time(), file=f_output_val, flush=True)
    R_train, R_test = loader(test_data, train_data, movie_data, f_output_val)
    print(datetime.datetime.now().time(), file=f_output_val, flush=True)

    print("\n")
    for rank in ranks:
        for lambd in lambds:
            print("\nn=",n, "m=",m, "rank=", rank, "steps=", steps, "lambd=", lambd, "eta=", eta, file=f_output_val, flush=True)
            train_V_W(R_train, R_test, n, m, rank, steps, lambd, eta, f_output_val)

if __name__ == "__main__":
    main()

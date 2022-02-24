N = 1
M = 1
INPUT_FEATURES_NUM = N
HIDDEN_SIZE = 100
OUTPUT_FEATURES_NUM = M
EPOCHS = 200



TRAIN_STEP = 2
MONTH = 5
name = 'bc'
# mean = 0
# std = 0
max = 0
min = 0

def normalize(data, min, max):
    return (data - min) / (max - min)

def step_train(dataset, df, path):
    pred_value = [0 for i in range(len(df))]

    
    for i in range(TRAIN_STEP, len(dataset)):

        lstm_model = LSTM(INPUT_FEATURES_NUM, HIDDEN_SIZE, \
            OUTPUT_FEATURES_NUM, num_layers=1) # 16 hidden units

        if i % TRAIN_STEP == 0:
            if i < MONTH:
                X = dataset[0:i, 0]
                y = dataset[0:i, 1]
                # X = dataset[:i, 0:N]
                # y = dataset[:i, N:N+M]
            else:
                X = dataset[i-MONTH:i, 0]
                y = dataset[i-MONTH:i, 1]
                # X = dataset[:i, 0:N]
                # y = dataset[:i, N:N+M]
            # mean = np.mean(y[0:i])
            # std = np.std(y[0:i])
            # X = (X - mean) / (std)
            # y = (y - mean) / (std)
            # print(X, mean, std)
            max = np.max(y)
            min = np.min(y)
            # print(np.ravel(y), min, max)
            X = normalize(X, min, max)
            y = normalize(y, min, max)
            # print(np.ravel(y), min, max)
            train(X, y, name)

        lstm_model.load_state_dict(torch.load(name+'.pkl'))  
        # load model parameters from files
        lstm_model = lstm_model.eval() # switch to testing model
        # prediction on test dataset
        X = normalize(dataset[i, 0], min, max)
        pred_x_tensor = X.reshape(-1, 1, INPUT_FEATURES_NUM) 
        # set batch size to 5, the same value with the training set
        pred_x_tensor = torch.from_numpy(pred_x_tensor)
        pred = lstm_model(pred_x_tensor)
        pred = pred.view(-1, OUTPUT_FEATURES_NUM).data.numpy()

        # print(i, pred[0][0] * (max - min) + min + df.iloc[i, 1])
        print(i, pred[0][0] * (max - min) + min)
        pred_value[i] = pred[0][0] * (max - min) + min
    # df['pred'] = pred_value + df['Value']
    df['pred'] = pred_value
    df.to_csv(path, index=False)

bc_df = pd.read_csv(bc_path)
gold_df = pd.read_csv(gold_path)

bc_diff = np.array(pd.read_csv(bc_diff_path))
gold_diff = np.array(pd.read_csv(gold_diff_path))

step_train(bc_data, bc_df, bc_pred)
step_train(gold_data, gold_df, gold_pred)
print('step train finished.')
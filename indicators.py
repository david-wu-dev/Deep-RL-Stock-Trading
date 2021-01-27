def sma(data_dict):
    n = len(data_dict['Close'])
    sma_20 = [0] * 19
    sma_50 = [0] * 49
    sma_200 = [0] * 199

    running_total_20 = sum(data_dict['Close'][0:20])
    running_total_50 = sum(data_dict['Close'][0:50])
    running_total_200 = sum(data_dict['Close'][0:200])

    sma_20.append(running_total_20 / 20)
    sma_50.append(running_total_50 / 50)
    sma_200.append(running_total_200 / 200)

    for i in range(n):
        if i >= 20:
            running_total_20 += (data_dict['Close'][i] - data_dict['Close'][i-20])
            sma_20.append(running_total_20 / 20)
        
        if i >= 50:
            running_total_50 += (data_dict['Close'][i] - data_dict['Close'][i-50])
            sma_50.append(running_total_50 / 50)
        
        if i >= 200:
            running_total_200 += (data_dict['Close'][i] - data_dict['Close'][i-200])
            sma_200.append(running_total_200 / 200)
    
    return sma_20, sma_50, sma_200

def macd(data_dict):
    n = len(data_dict['Close'])
    ema_12 = [0]*12
    ema_26 = [0]*26
    ema_12_val = sum(data_dict['Close'][0:12]) / 12
    ema_26_val = sum(data_dict['Close'][0:26]) / 26

    for i in range(n):
        if i >= 12:
            new_ema_12 = (data_dict['Close'][i] * 2 / 13) + (ema_12_val * 11 / 13)
            ema_12.append(new_ema_12)
            ema_12_val = new_ema_12
        
        if i >= 26:
            new_ema_26 = (data_dict['Close'][i] * 2 / 27) + (ema_26_val * 25 / 27)
            ema_26.append(new_ema_26)
            ema_26_val = new_ema_26

    macd = []
    for j in range(n):
        macd.append(ema_12[j] - ema_26[j])
    
    return macd

def rsi(data_dict):
    n = len(data_dict['Close'])
    gain = 0
    loss = 0

    for i in range(14):
        if data_dict['Close'][i+1] > data_dict['Close'][i]:
            gain += (data_dict['Close'][i+1] - data_dict['Close'][i])
        else:
            loss += (data_dict['Close'][i] - data_dict['Close'][i+1])

    avg_gain = gain / 14
    avg_loss = loss / 14

    avg_gains = [0] * 14
    avg_losses = [0] * 14

    avg_gains.append(avg_gain)
    avg_losses.append(avg_loss)

    for j in range(14, n-1):
        diff = data_dict['Close'][j+1] - data_dict['Close'][j]
        if diff > 0:
            avg_gains.append((avg_gains[-1] * 13 + diff) / 14)
            avg_losses.append(avg_losses[-1] * 13 / 14)
        else:
            avg_gains.append(avg_gains[-1] * 13 / 14)
            avg_losses.append((avg_losses[-1] * 13 - diff) / 14)

    rsi = [0]*14

    for k in range(14, n):
        rs = avg_gains[k] / avg_losses[k]
        rsi.append(100 - (100 / (1 + rs)))
    
    return rsi

def cci(data_dict, sma_20):
    n = len(data_dict['Close'])
    typical_price = []

    for i in range(n):
        typical_price.append((data_dict['High'][i] + data_dict['Low'][i] + data_dict['Close'][i]) / 3)

    mean_deviation = [0] * 19
    for j in range(19, n):
        total = sum([abs(typical_price[i] - sma_20[j]) for i in range(j - 19, j + 1)])
        mean_deviation.append(total / 20)

    cci = [0]*19
    for k in range(19, n):
        cci.append((typical_price[k] - sma_20[k]) / (0.015 * mean_deviation[k]))

    return cci

def get_indicators(data_dict):
    sma_20, sma_50, sma_200 = sma(data_dict)
    macd_vals = macd(data_dict)
    rsi_vals = rsi(data_dict)
    cci_vals = cci(data_dict, sma_20)

    indicators = {'sma_20': sma_20, 'sma_50': sma_50, 'sma_200': sma_200, 'macd': macd_vals, 'rsi': rsi_vals, 'cci': cci_vals}
    return indicators
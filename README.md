# Deep Reinforcement Learning: Stock Trading

## Overview
The goal of this project was to create and train a trading agent using reinforcement learning then analyze their performance compared to a simple stock investing strategy, such as buying and holding. The first approach relies on OpenAI's stable-baselines which contains many pretrained reinforcement learning models. The architecture used in this project from the OpenAI stable-baselines model was the DQN (Deep Q-Network). In order to leverage the stable-baselines module, an OpenAI gym environment, simulating the stock market, was defined, which also included information about common stock indicators including the MACD, RSI, etc. The second approach involved implementing an advantage actor-critic model from scratch in Pytorch which would also interact with the OpenAI gym environment in a similar fashion. 

## Instructions to run this code
To simplify the problem of version compatibility, all the code was run in Google Colab. Therefore, to run this code, clone this repository and upload the folder to Google Drive where the Juypyter notebooks can then be run.

## Results
Both models were trained on the first 1000 days of Apple stock (AAPL). After training, the DQN actually became quite an effective trading agent as it was able to keep up well with the strategy of buying and holding while decreasing the fluctuation in portfolio value dramatically. The advantage actor critic model defined from scratch also showed similar characteristics, but overall had worse performance than the DQN. Additionally, the training for the actor critic model was not stable and it often failed to converge, hinting at underlying issues with hyperparameters and the implementation. 


<div>
	<img src="/results/DQN%20stock%20graph.PNG" width="400" height="Automated"/>
	<img src="/results/AC%20stock%20graph.PNG" width="400" height="Automated"/>
</div>

In the above graphs, the orange lines are directly related to the stock price (stock price * 367), which reflects the value of a portfolio maintained under the buy and hold strategy if $100 worth of Apple stock was bought on the first day. The blue lines show the value of the portfolio managed under the trading agents, who were also given $100 on the first day. Though the trading agents did not always outperform buying and holding a high performing stock like AAPL, they were able to drastically lower the variation in portfolio value in both cases while mostly keeping up with the stock price, ensuring that the investor would not have to worry large fluctuations in stock price. As this is one of the central risks people face in the stock market, this simple approach and relatively general models imply that it is possible to take advantage of reinforcement learning to do smarter stock investing.

## Additional Notes
The current features presented to the models include several simple moving averages. There is a problem with this approach as the stock price changes drastically throughout the course of many days, shifting the distribution of the input. However, this approach seems to suffice for this sort of demonstration as the simple moving averages are often used relative to one another in order to provide any useful information so they help normalize themselves. In a future implementation, this problem can be more directly solved with some sort of explicit normalization of the simple moving averages, perhaps with the current stock price.

## References
Hongyang Yang, Xiao-Yang Liu, Shan Zhong, and Anwar Walid. 2020. Deep Reinforcement Learning for Automated Stock Trading: An Ensemble Strategy. In ICAIF ’20: ACM International Conference on AI in Finance, Oct. 15–16, 2020, Manhattan, NY. ACM, New York, NY, USA.
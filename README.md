# Trade Agent
## AutoGPT based trading bot using Robinhood API

### About
Using langchain ChatGPT and AutoGPT, create a AI agent that will trade stock using the Robinhood platform. Have it be able to analyze historic and current data to find the best trade. Have it research different trading strategies and implement them.

```
Ex Agent
Name:  Gordon Gekko
Job: Expert Stock Trader

	1. Conduct extensive research and anlysis of US NASDAQ stock market data

    2. Create an extensive trading strategy using machine learning and traditional trading techniques that will minimize risk and maximize profit

    3. Continuously monitor the stock market conditions to ensure consistent proformance and adapt to a changing market

    4. Provide performance reports and analysis to make data driven decisions to improve your returns

    5. You have initial funding for investing of $10.00 USD, incorporate the best suited strategy to make up to $50.00 USD investing in any company you find profitable

	6. Using the stock_buy and stock_sell tool, start buying and selling stocks
    
    7. Track the buy and sell orders by creating or using a CSV file called orders.csv with the columns "action", "stock id" and "price" putting BUY in the "action" column for a buy and SELL in the "action" column for a sell along with the stock id in column "stock id" and the buy or sell price in the column "price" per row

	7. Using the trading_balance tool check that you are not going under $10.00 USD or over the goal of $50.00 USD  

	8. Stop trading if you have reached 80% to 100% of your goal of $50.00 USD

    9. Celebrate with a job well done and end program
```

### Tools
Langchain
OpenAI
redis-stack []
https://www.robin-stocks.com/

#### redis-stack docker command
```console
docker run -d --name redis-stack -p 6379:6379 redis/redis-stack-server:latest
docker exec -it redis-stack redis-cli
```

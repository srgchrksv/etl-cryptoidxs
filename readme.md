## ETL pipeline using Azure services

### Idea is to get financial timeseries for multiple crypto currencies and calculate custom index for each symbol. 

### Pairs:
- BTCUSDT
- ETHUSDT
- BNBUSDT
- ETHBTC
- BNBETH
- BNBBTC
 

### Looking to calculate Relative Strength Index for each pair and then use this formula for currency indexes:

| Currency | Calculation                                |
|----------|--------------------------------------------|
| BTC      | (BTCUSDT + (100 - ETHBTC) + (100 - BNBBTC)) / 3 |
| ETH      | (ETHUSDT + ETHBTC + (100 - BNBETH)) / 3        |
| BNB      | (BNBUSDT + BNBETH +  BNBBTC) / 3        |
| USDT     | ((100 - BTCUSDT) + (100 - ETHUSDT) + (100 - BNBUSDT)) / 3 |

RSI is ranging from 0 to 100 so we are getting standartized indexes.

*The same way we can calculate indexes for forex currencies*

### Plan:
1. Getting historical data from binance api
2. Loading raw in bronze storage layer
3. Adding schema and loading as silver layer
4. Calculating indexes for symbols and load as gold layer
5. Calculate correlations
6. Visualize data

### Correlations 
!["correlations"](/docs/correlations.png)

### Line plot
!["lineplot"](/docs/lineplot.png)

### Services used
!["azure etl pipleline"](/docs/etl-azure.png)
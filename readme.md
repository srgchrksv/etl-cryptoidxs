## ETL pipeline using Azure services

### Idea is to get financial timeseries for multiple crypto currencies and calculate custom index for each symbol. 

### Pairs:
- BTCUSDT
- ETHUSDT
- BNBUSDT
- ETHBTC
- BNBETH
- BNBBTC
 

### Plan:
1. Getting historical data from binance api
2. Loading raw in bronze storage layer
3. Adding schema and loading as silver layer
***
Work in progress...................
***
4. Calculating indexes for symbols and load as gold layer
5. Visualizing data

!["azure etl pipleline"](/docs/etl-azure.png)
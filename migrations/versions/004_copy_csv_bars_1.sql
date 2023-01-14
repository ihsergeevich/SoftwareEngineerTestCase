COPY
    bars_1("date", symbol, adjclose, "close", high, low, "open", volume)
FROM
    '/tmp/bars_1.csv'
WITH
    (FORMAT CSV, HEADER,DELIMITER ',');
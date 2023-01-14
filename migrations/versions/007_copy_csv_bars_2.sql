COPY
    bars_2("date", symbol, adjclose, "close", high, low, "open", volume)
FROM
    '/tmp/bars_2.csv'
WITH
    (FORMAT CSV, HEADER,DELIMITER ',');
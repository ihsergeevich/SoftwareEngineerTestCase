BEGIN;

LOCK bars_1 IN ROW EXCLUSIVE MODE NOWAIT;

CREATE INDEX ix_bars_1_symbol ON bars_1 USING btree(symbol);
CREATE INDEX ix_bars_1_date ON bars_1 USING btree("date" DESC);
CREATE INDEX ix_bars_1_date_symbol ON bars_1 USING btree("date", symbol);

COMMIT;
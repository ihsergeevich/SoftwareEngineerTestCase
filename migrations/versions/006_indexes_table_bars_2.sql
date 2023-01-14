BEGIN;

LOCK bars_2 IN ROW EXCLUSIVE MODE NOWAIT;

CREATE INDEX ix_bars_2_symbol ON bars_2 USING btree(symbol);
CREATE INDEX ix_bars_2_date ON bars_2 USING btree("date" DESC);
CREATE UNIQUE INDEX ix_bars_2_date_symbol ON bars_2 USING btree("date", symbol);

COMMIT;
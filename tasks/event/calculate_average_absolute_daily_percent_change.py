from core.base_task import BaseTask


class CalculateAverageAbsoluteDailyPercentChange(BaseTask):
    """
    Calculate Average Absolute Daily Percent Change
    """

    def __int__(self, app):
        self.app = app
        self.worker_name = 'CalculateAverageAbsoluteDailyPercentChange'

    async def get_info(self, cursor) -> (str, float):
        sql = """
        	select
                r.symbol,
                avg(r.abs_res) as res
            from
                (select
                    symbol,
                    abs(
                        (select
                            "close"
                        from 
                            bars_1 b2 
                        where
                            b2."date" < b."date"
                        order by 
                            b."date" desc
                        limit 
                            1
                    ) * 100 /  b."close" - 100) as abs_res
                from
                    bars_1 b
                group by
                    b."date",
                    b.symbol,
                    b."close"
            ) as r
            group by
                r.symbol
		"""

        return 'task_1_1_p4', [[x['symbol'], x['rs']] for x in await cursor.fetch(sql)]




from core.base_task import BaseTask


class RankStocksByPositiveVolume(BaseTask):
    """
    Rank stocks in 2015 by Positive Volume in ascending order.
    """

    def __init__(self, app):
        self.app = app
        self.worker_name = 'RankStocksByPositiveVolume'

    async def get_info(self, cursor):
        sql = """
        select 
            symbol,
            "date",
            case
                when bars_1.adjclose >= (
                    select 
                        adjclose 
                    from 
                        bars_1 b 
                    where 
                        b."date" <= bars_1."date"
                    order by
                        bars_1."date" desc
                    limit 1
                ) then bars_1.adjclose
                else 0
            end as r
        from 
            bars_1
        where 
            '2015-01-01' <= "date" and 
            "date" <= '2015-12-31'
        order by
            r
        """

        return 'task_1_1_p3', [[x['symbol'], x['date'], x['r']] for x in await cursor.fetch(sql)]



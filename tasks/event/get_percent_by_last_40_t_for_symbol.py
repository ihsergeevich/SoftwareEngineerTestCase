from core.base_task import BaseTask


class GetPercentByLast40tForSymbol(BaseTask):

    def __init__(self, app):
        self.app = app
        self.worker_name = 'GetPercentByLast40tForSymbol'

    async def get_info(self, cursor):
        sql = """
        select  
	        round(count(*), 2) * 100 / (
                                    select 
                                        count(*) 
                                    from 
                                        public.bars_1 
                                    where 
                                        '2019-01-01' <= "date" and 
                                        "date" <= '2019-12-31') as "percent"
        from 
	        public.bars_1 
        where 
            '2019-01-01' <= "date" and 
            "date" <= '2019-12-31' and 
            adjclose > (
                select
                    sum(tbl.adjclose) / count(tbl.adjclose)
                from
                    (
                        select
                            adjclose
                        from public.bars_1 as second_bars_1
                        where
                            second_bars_1.date < bars_1.date and 
                            second_bars_1.symbol = bars_1.symbol
                        order by 
                            bars_1.date desc
                        limit 40
                            ) as tbl		
            )
            """

        return 'task_1_1_p1', await cursor.fetchval(sql)

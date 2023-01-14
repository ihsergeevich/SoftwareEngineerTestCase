from core.base_task import BaseTask


class CalculateTheAverageDollarVolume(BaseTask):
    """
    Calculate the average dollar volume
    in February 2019
    """

    def __init__(self, app):
        self.app = app
        self.worker_name = 'CalculateTheAverageDollarVolume'

    async def get_info(self, cursor):
        sql = """
        select  
	        avg(adjclose * volume)
        from 
            bars_1
        where 
            '2019-02-01' <= "date" and 
            "date" <= '2019-02-28'
        """

        return 'task_1_1_p2', await cursor.fetchval(sql)

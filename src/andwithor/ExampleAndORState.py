import asyncio
from typing import Any, Dict, List
from crewai.flow.flow import Flow, and_, listen, start, or_
from pydantic import BaseModel

class LoggerState(BaseModel):
    results: List[str] = []
    
class ExampleAndOR(Flow[LoggerState]):

    @start()
    def start_method(self):
        print("---- Start Method ----")
        return "Welcome to Return Method of Start Method"

    @listen(start_method)
    async def second_method(self):
        await asyncio.sleep(1)
        print("---- Second Method ----")
        return "Welcome to Return Method of Second Method"
    
    @listen(second_method)
    async def third_method(self):
        await asyncio.sleep(2)
        print("---- Third Method ----")
        return "Welcome to Return Method of Third Method"
    
    @listen(second_method)
    async def fourth_method(self):
        await asyncio.sleep(3)
        print("---- Fourth Method ----")
        return "Welcome to Return Method of Fourth Method"
    
    @listen(or_(start_method, second_method, third_method, fourth_method))
    def logger(self, *results):
        self.state.results.extend(results)
        print("---- Logger ----")
        print("Results:", self.state.results)
        return self.state.results
        
def kickoff():
    flow = ExampleAndOR()
    flow.kickoff()

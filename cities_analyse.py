import heapq
from collections import defaultdict
import pandas as pd
import re

class DAO:
    _inst = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._inst is None:
            cls._inst = super().__new__(cls)
        return cls._inst

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self.data = []
            self.cols = []
            self.dataframe = None #dataframe approach
            self.readCsv()
    def readCsv(self):
        df = pd.read_csv("miasta.csv")
        self.data = df.values.tolist()
        self.cols = df.columns.tolist()
        self.dataframe = df
        return self.data

class CityPresenter:
    def __init__(self, dao_inst):
        self.dao_inst = dao_inst
    def display_cities(self, starts_with):
        towns = self.dao_inst.data
        pattern = re.compile(rf'^{starts_with}', re.IGNORECASE)
        for townInfo in towns:
            townName = townInfo[0]
            if pattern.match(townName):
                print(townInfo)

class CityStatistic:

    def __init__(self, dao_inst):
        self.dao_inst = dao_inst

    def top10Largest(self):
        top_n = 10
        df = self.dao_inst.dataframe
        top_cities = df.nlargest(top_n, 'population')['city'].tolist()
        return top_cities

    def meanSize(self):
        df = self.dao_inst.dataframe
        mean = df["population"].mean()
        return mean

    def meanCityForEachContinent(self):
        df = self.dao_inst.dataframe
        heap = []
        a = set(df["continent"])
        for continent in a:
            filtered_df = df[ df["continent"] == continent]
            heapq.heappush(heap, (continent,float(filtered_df['population'].mean())))
        return heap

    def largestCityForEachContinent(self):
        df = self.dao_inst.dataframe
        heap = []
        a = set(df["continent"])

        for continent in a:
            filtered_df = df[df["continent"] == continent]
            heapq.heappush(heap, (continent, filtered_df.nlargest(1, 'population')["city"].iloc[0])  )

        return heap

    def largestCityForEachCountry(self):
        df = self.dao_inst.dataframe
        res = []
        a = set(df["country"])
        for country in a:
            filtered_df = df[ df["country"] == country ]
            largestCity = filtered_df.nlargest(1, 'population')["city"].iloc[0]
            res.append((country,largestCity))
        res.sort(key = lambda x: x[1])

        return res



dao = DAO()

present = CityPresenter(dao_inst= dao)

stats = CityStatistic(dao)
print(stats.largestCityForEachCountry())
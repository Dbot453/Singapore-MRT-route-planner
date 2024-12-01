from Graph import Graph as g

class Station:
    
    def __init__(self):
        self.__graph = g().generateAdjacencyList()
        self.__info = g().generateStationInfo()
    
    def getStationInfo(self, stationCode):
        return self.__info[stationCode]
    
    def getGraph(self):
        return self.__graph[self.__stationCode]
    
    def getName(self):
        return self.__info[self.__stationCode][0]
    
    def getLineColor(self):
        return self.__info[self.__stationCode][1]
    
    def getLine(self):
        return self.__info[self.__stationCode][2]
    
    def getLat(self):
        return self.__info[self.__stationCode][3]

    def getLong(self):
        return self.__info[self.__stationCode][4]
    
    def getNeighbours(self):
        return self.__graph[self.__stationCode]
    
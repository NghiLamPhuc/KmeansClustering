from Point import Point
from Point import calculate_midpoint_of_list, compare_two_point
from make_folder import create_folder
from write_file import list_to_txt_with_last_comma, list_to_txt_continuos
from read_file import read_lines_to_list

class Kmeans:
    def __init__(self, dataInit: list, k_cluster: int, dType: int):
        self.dataInitial = dataInit
        self.size = len(dataInit)
        self.k = k_cluster
        self.distanceType = dType #1 euclid, 2 cosine..
        self.centers = list() #trung diem
        self.distancesPointToCenters = list(list()) #khoang cach tu trung diem toi input
        self.indexMinDistances = list() #cluster cac diem dua vao khoang cach o tren.
        self.kCluster = list(list()) #Chia cluster ra theo list
        self.kIndex = list(list())

        self.outfileDir = './outfile/'
    # Khong gop cac buoc first lai, vi sau nay cai tien.
    def set_center_list_first(self): # Co the cai thien trong tuong lai-----?
        # Gia su co it nhat 2 diem dau tien giong nhau (co the keo theo ket qua phan thieu lop)
        self.centers.append(self.dataInitial[0])
        if len(self.centers) == self.k:
            return
        for point in self.dataInitial:
            checkAdded = 0
            for center in self.centers:
                if compare_two_point(point, center) == 1:
                    checkAdded = 1
                    break
            if checkAdded == 0:
                self.centers.append(point)
                if len(self.centers) == self.k:
                    return
        
    def calculate_distances_first(self):
        for point in self.dataInitial:
            pointToCenters = list()
            for iCenter in self.centers:
                pointToCenters.append(point.euclid_distance(iCenter))
            self.distancesPointToCenters.append(pointToCenters)

    def set_point_to_cluster_first(self):
        for dList in self.distancesPointToCenters:
            minDistance = min(dList)
            self.indexMinDistances.append(dList.index(minDistance))

    def clustering(self):
        self.kCluster = list()
        self.kIndex = list()
        for iCluster in range(self.k):
            cluster = list()
            position = list()
            for index in range(self.size):
                if iCluster == self.indexMinDistances[index]:
                    cluster.append(self.dataInitial[index])
                    position.append(index)
            self.kCluster.append(cluster)
            self.kIndex.append(position)
        
    def update_center(self):
        self.centers = list()
        for cluster in self.kCluster:
            self.centers.append(calculate_midpoint_of_list(cluster))

    def update_distances(self):
        self.distancesPointToCenters = list()
        for point in self.dataInitial:
            pointToCenters = list()
            for iCenter in self.centers:
                pointToCenters.append(point.euclid_distance(iCenter))
            self.distancesPointToCenters.append(pointToCenters)

    def update_point_to_cluster(self) -> int:
        indexMinDistancesNew = list()
        for dList in self.distancesPointToCenters:
            minDistance = min(dList)
            indexMinDistancesNew.append(dList.index(minDistance))
        checkEnd = 1 # when new 'cluster-to-point' same with previous 'cluster-to-point'.
        # 0 for difference, 1 for same.
        for index in range(self.size):
            if (indexMinDistancesNew[index] != self.indexMinDistances[index]):
                checkEnd = 0
                break
        # strl1 = ''.join(str(num1) for num1 in indexMinDistancesNew)
        # strl2 = ''.join(str(num2) for num2 in self.indexMinDistances)
        self.indexMinDistances = indexMinDistancesNew
        return checkEnd
    
    def initial_step(self):
        self.set_center_list_first()
        self.calculate_distances_first()
        self.set_point_to_cluster_first()
        self.clustering()
        self.write_step_outfile()

    def update_step(self):
        self.update_center()
        self.update_distances()
        endOrNot = self.update_point_to_cluster()
        if endOrNot == 1:
            self.clustering()
            self.write_step_outfile()
            return
        if endOrNot == 0:
            self.clustering()
            self.write_step_outfile()
            return self.update_step()
    
    def write_step_outfile(self):
        dir = './outfile/' 
        fileName = ['centers.txt', 'distances.txt', 'pointCluster.txt', 'cluster.txt']
        # write centers
        self.write_step_center()
        # write distances
        self.write_step_distances()
        # write cluster of point
        self.write_step_cluster_of_point()
        # write k cluster
        self.write_step_kCluster()

    def write_step_center(self):
        pointStrList = list()
        for center in self.centers:
            pointStrList.append('c{0}: '.format(self.centers.index(center)) + center.display())
        list_to_txt_continuos(pointStrList, self.outfileDir, 'centers.txt')
    def write_step_distances(self):
        dPointsStrList = list()
        for dPoints in self.distancesPointToCenters:
            dPointsStrList.append(str(dPoints))
        list_to_txt_continuos(dPointsStrList, self.outfileDir, 'distances.txt')
    def write_step_cluster_of_point(self):
        list_to_txt_continuos(self.indexMinDistances, self.outfileDir, 'pointCluster.txt')
    def write_step_kCluster(self):
        pointStrList = list()
        for cluster in self.kCluster:
            pointStrList.append('cluster {0}'.format(self.kCluster.index(cluster)))
            for point in cluster:
                pointStrList.append('{0}.'.format(self.dataInitial.index(point)) + (point.display() + ' ').rstrip() )
        list_to_txt_continuos(pointStrList, self.outfileDir, 'cluster.txt')

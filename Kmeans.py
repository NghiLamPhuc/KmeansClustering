from Point import Point
from Point import calculate_midpoint_of_list, compare_two_point
# from make_folder import create_folder
from write_file import list_to_txt_continuos_with_last_comma, list_to_txt_continuos
from read_file import read_lines_to_list
import shutil
import os

class Kmeans:
    def __init__(self, dataInitType: int, dataInit: list, k_cluster: int, dType: int, dataName: str):
        self.dataInitialType = dataInitType #  0 text 1 vector
        self.dataInitial = dataInit
        self.size = len(dataInit)
        self.k = k_cluster
        self.distanceType = dType #1 euclid, 2 cosine..
        self.centers = list() #trung diem
        self.distancesPointToCenters = list(list()) #khoang cach tu trung diem toi input
        self.indexMinDistances = list() #cluster cac diem dua vao khoang cach o tren.
        self.kCluster = list(list()) #Chia cluster ra theo list
        self.kIndex = list(list())
        self.fileDir = './' + dataName

        self.outfileDir = './outfile/' + dataName + '/kmeans_vectorinput/'
        if dataInitType == 0:
            self.outfileDir = './outfile/' + dataName + '/kmeans_textinput/'
        
        self.numOfLoops = 1

        self.initial_step()
        self.update_step()
    # Khong gop cac buoc first lai, vi sau nay cai tien.
    def set_center_list_first(self): # Co the cai thien trong tuong lai-----?
        # Gia su co it nhat 2 diem dau tien giong nhau (co the keo theo ket qua phan thieu lop)
        if self.k == self.size:
            return 0
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
                    return 1
        #####
        ## Bị lỗi là, thí dụ datasets có 15 dòng, 2 dòng giống nhau, chọn k thì nó chỉ chọn 14, dẫn tới sai.
        #####

    def calculate_distances_first(self):
        if self.distanceType == 1:
            for point in self.dataInitial:
                pointToCenters = list()
                for iCenter in self.centers:
                    pointToCenters.append(point.euclid_distance(iCenter))
                self.distancesPointToCenters.append(pointToCenters)
        elif self.distanceType == 2:
            for point in self.dataInitial:
                pointToCenters = list()
                for iCenter in self.centers:
                    pointToCenters.append(point.cosine_distance(iCenter))
                self.distancesPointToCenters.append(pointToCenters)

    def set_point_to_cluster_first(self):
        if self.distanceType == 1:
            for dList in self.distancesPointToCenters:
                minDistance = min(dList)
                self.indexMinDistances.append(dList.index(minDistance))
        elif self.distanceType == 2:
            for dList in self.distancesPointToCenters:
                maxDistance = 0
                for num in dList:
                    if num < 1.0:
                        if maxDistance < num:
                            maxDistance = num
                self.indexMinDistances.append(dList.index(maxDistance))

    def clustering(self):
        self.kCluster = list()
        self.kIndex = list()
        for iCluster in range(int(self.k)):
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
        if self.distanceType == 1:
            for point in self.dataInitial:
                pointToCenters = list()
                for iCenter in self.centers:
                    pointToCenters.append(point.euclid_distance(iCenter))
                self.distancesPointToCenters.append(pointToCenters)
        elif self.distanceType == 2:
            for point in self.dataInitial:
                pointToCenters = list()
                for iCenter in self.centers:
                    pointToCenters.append(point.cosine_distance(iCenter))
                self.distancesPointToCenters.append(pointToCenters)

    def update_point_to_cluster(self) -> int:
        if self.distanceType == 1:
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
            self.indexMinDistances = indexMinDistancesNew
        elif self.distanceType == 2:
            indexMaxDistancesNew = list()
            for dList in self.distancesPointToCenters:
                maxDistance = 0
                for num in dList:
                    if num < 1.0:
                        if maxDistance < num:
                            maxDistance = num
                indexMaxDistancesNew.append(dList.index(maxDistance))
            checkEnd = 1 # when new 'cluster-to-point' same with previous 'cluster-to-point'.
            # 0 for difference, 1 for same.
            for index in range(self.size):
                if (indexMaxDistancesNew[index] != self.indexMinDistances[index]):
                    checkEnd = 0
                    break
            self.indexMinDistances = indexMaxDistancesNew
        return checkEnd
    
    def initial_step(self) -> int:
        step1 = self.set_center_list_first()
        if step1 == 0: # k = số dòng dữ liệu.
            return 0
        self.calculate_distances_first()
        self.set_point_to_cluster_first()
        self.clustering()
        shutil.rmtree(self.outfileDir, ignore_errors=True)
        self.write_step_outfile()
        return 1

    def update_step(self):
        self.numOfLoops += 1
        self.update_center()
        self.update_distances()
        endOrNot = self.update_point_to_cluster()
        if endOrNot == 1:
            self.clustering()
            self.write_step_outfile()
            self.write_last_centers()
            self.write_last_kCluster_index()
            return
        if endOrNot == 0:
            self.clustering()
            self.write_step_outfile()
            return self.update_step()
    
    def write_step_outfile(self):
        # dir = './outfile/' 
        # fileName = ['centers.txt', 'distances.txt', 'pointCluster.txt', 'cluster.txt']
        # write centers
        self.write_step_center()
        # write distances
        self.write_step_distances()
        # write clustering of point
        self.write_step_cluster_of_point()
        # write k cluster
        self.write_step_kCluster() ###### Gay ton bo nho.
        # write index k cluster
        self.write_step_kCluster_index()

    def write_step_center(self):
        pointStrList = ['Loop ' + str(self.numOfLoops)]
        for center in self.centers:
            pointStrList.append('c{0}: '.format(self.centers.index(center)) + center.display_with_parentheses())
        list_to_txt_continuos(pointStrList, self.outfileDir, 'centers.txt', '\n')

    def write_step_distances(self):
        dPointsStrList = ['Loop ' + str(self.numOfLoops)]
        for dPoints in self.distancesPointToCenters:
            dPointsStrList.append(str(dPoints))
        list_to_txt_continuos(dPointsStrList, self.outfileDir, 'distances.txt', '\n')

    def write_step_cluster_of_point(self):
        toWrite = ['Loop ' + str(self.numOfLoops) + ': ']
        toWrite += self.indexMinDistances
        list_to_txt_continuos(toWrite, self.outfileDir, 'point_clustering.txt', ' ')

    def write_step_kCluster(self):
        for cluster in self.kCluster:
            pointStrList = ['Loop ' + str(self.numOfLoops)]
            indexCluster = self.kCluster.index(cluster)
            pointStrList.append('\nCluster {0} has {1} objects: '.format(indexCluster, len(cluster)))
            for point in cluster:
                pointStrList.append('{0}.'.format(self.dataInitial.index(point)) + (point.display_with_parentheses() + ' ').rstrip() )
            list_to_txt_continuos(pointStrList, self.outfileDir + 'cluster/', 'cluster{0}.txt'.format(indexCluster), '\n')

    def write_last_kCluster(self):
        pointStrList = ['Loop {0}'.format(self.numOfLoops)]
        for cluster in self.kCluster:
            indexCluster = self.kCluster.index(cluster)
            pointStrList.append('\nCluster {0} has {1} objects: '.format(indexCluster, len(cluster)))
            for point in cluster:
                pointStrList.append('{0}.'.format(self.dataInitial.index(point)) + (point.display_with_parentheses() + ' ').rstrip() )
        list_to_txt_continuos(pointStrList, self.outfileDir, 'last_clustering.txt', '\n')

    def write_step_kCluster_index(self):
        indexPointStrList = ['Loop ' + str(self.numOfLoops)]
        for cluster in self.kCluster:
            indexPointStrList.append('\nCluster {0} has {1} objects: '.format(self.kCluster.index(cluster), len(cluster)))
            for point in cluster:
                indexPointStrList.append('{0}'.format(self.dataInitial.index(point)))
            # indexPointStrList.append('\n')
        list_to_txt_continuos(indexPointStrList, self.outfileDir, 'cluster_index.txt', ' ')

    def write_last_kCluster_index(self):
        indexPointStrList = ['Loop ' + str(self.numOfLoops)]
        for cluster in self.kCluster:
            indexPointStrList.append('\nCluster {0} has {1} objects: '.format(self.kCluster.index(cluster), len(cluster)))
            for point in cluster:
                indexPointStrList.append('{0}'.format(self.dataInitial.index(point)))
        list_to_txt_continuos(indexPointStrList, self.outfileDir, 'last_cluster_index.txt', ' ')

    def write_last_centers(self):
        pointStrList = []
        for center in self.centers:
            pointStrList.append(center.display())
        list_to_txt_continuos(pointStrList, self.outfileDir, 'last_centers.txt', '\n')

    def predict_new_point(self, newPoint: Point) -> str:
        res = str(0)
        lastCenters = self.centers
        if self.distanceType == 1: # euclid
            min = lastCenters[0].euclid_distance(newPoint)
            for center in lastCenters:
                d = center.euclid_distance(newPoint)
                if min > d:
                    min = d
                    res = str(lastCenters.index(center))
        elif self.distanceType == 2: # cosine
            max = lastCenters[0].cosine_distance(newPoint)
            for center in lastCenters:
                d = center.cosine_distance(newPoint)
                if max < d:
                    max = d
                    res = str(lastCenters.index(center))
        return res


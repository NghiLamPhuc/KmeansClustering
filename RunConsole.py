from Point import Point
from Kmeans import Kmeans
from read_file import read_lines_to_list, read_input_file_to_int

## K-means su dung input khong gan nhan (non label) 
##
# Read input with non-labeled at last.
def set_initData_with_nonLabeledData(dir: str, fileName: str, splitType: str) -> list:
    initData = list()
    datasetList = read_lines_to_list(dir, fileName, splitType)
    for rowStrList in datasetList:
        rowFloatList = list(map(float, rowStrList))
        initData.append(Point(rowFloatList))
    return initData
# Input dataset with last labeled.
def set_initData_with_labeledData(dir: str, fileName: str, splitType: str) -> list:
    initData = list()
    datasetList = read_lines_to_list(dir, fileName, splitType)
    for rowStrList in datasetList:
        rowFloatList = list(map(float, rowStrList))
        del rowFloatList[-1] # Trong truong hop dataset da gan nhan o vi tri cuoi (0, 1)
        initData.append(Point(rowFloatList))
    return initData

# This function must be in Kmeans class. But... :))
def get_last_centers(dirLastCenters: str, fileName: str, splitType: str) -> list:
    lastCentersStr = read_lines_to_list(dirLastCenters, fileName, ', ')[:-1]
    lastCenters = list()
    for centerStr in lastCentersStr:
        coordList = list()
        for coordStr in centerStr:
            coordList.append(float(coordStr))
        lastCenters.append(Point(coordList))
    return lastCenters

def predict_new_point_temporary(lastCenters: list(), newPoint: Point) -> str:
    res = str(0)
    min = lastCenters[0].euclid_distance(newPoint)
    for center in lastCenters:
        d = center.euclid_distance(newPoint)
        if min > d:
            min = d
            res = str(lastCenters.index(center))
    return res

def main():
    dir = './datasets/'
    datasetName = ['train_vn.txt', 'train_en.txt', 'BaiTapAnBinhLinhetc.txt']
    splitType = ' '
    fileName = datasetName[-1]
    lastCentersDir = './outfile/' + fileName + '/'

    initData = list()
    initData = set_initData_with_nonLabeledData(dir, fileName, splitType)
    dType = 1 # euclid distance

    k = read_input_file_to_int(dir, 'k.txt')
    
    if k > len(initData):
        print('k nhieu hon du lieu.')
        return
    kmeans = Kmeans(initData, k, dType, fileName)
    kmeans.initial_step()
    kmeans.update_step()
    for cluster in kmeans.kCluster:
        print(len(cluster))

    # lastCenters = get_last_centers(lastCentersDir, 'lastCenters.txt', ', ')
    
    # newPoint = Point([20,80])
    # newPoint = Point([22,15])
    # print('Predict {0} -> cluster {1}'.format(newPoint.display_with_parentheses(), predict_new_point_temporary(lastCenters, newPoint)) )


if __name__=="__main__": main()
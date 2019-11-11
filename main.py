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
    datasetName = ['train_vn.txt', 'train_en.txt', 'Spend_Age.txt', 'BaiTapAnBinhLinhetc.txt']
    splitType = ' '
    fileName = datasetName[-1]
    lastCentersDir = './outfile/' + fileName + '/'

    An = Point([10, 10])
    Binh = Point([40, 20])
    Linh = Point([10, 10])
    Loc = Point([22, 15])
    Nhan = Point([10, 16])
    Nghia = Point([30, 10])
    Phat = Point([20, 20])
    Trong = Point([32, 15])
    Nhan1 = Point([50, 22])
    Nhan2 = Point([45, 19])
    Nhan3 = Point([30, 75])
    Nhan4 = Point([25, 80])
    Nhan5 = Point([10, 90])
    Nhan6 = Point([65, 50])
    Nhan7 = Point([90, 10])

    initData = list()
    initData = set_initData_with_nonLabeledData(dir, fileName, splitType)
    # initData = [Loc,Nhan,Nghia,An,Binh,Linh,Phat,Trong,Nhan1,Nhan2,Nhan3,Nhan4,Nhan5,Nhan6,Nhan7]
    # k = 3
    # k = 2 # for train_vn
    # k = 13 # for train_en
    dType = 1 # euclid distance

    k = read_input_file_to_int(dir, 'k.txt')
    
    if k > len(initData):
        print('k nhieu hon du lieu.')
        return
    # kmeans = Kmeans(initData, k, dType, fileName)
    # kmeans.initial_step()
    # kmeans.update_step()
    # for cluster in kmeans.kCluster:
    #     print(len(cluster))

    lastCenters = get_last_centers(lastCentersDir, 'lastCenters.txt', ', ')
    
    newPoint = Point([20,80])
    # newPoint = An
    print('Predict {0} -> cluster {1}'.format(newPoint.display_with_parentheses(), predict_new_point_temporary(lastCenters, newPoint)) )


if __name__=="__main__": main()
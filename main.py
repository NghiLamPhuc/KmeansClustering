from Point import Point
from Kmeans import Kmeans
from read_file import read_lines_to_list

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

def main():
    dir = './datasets/'
    fileName = ['train_vn.txt', 'train_en.txt', 'Spend_Age.txt', 'BaiTapAnBinhLinhetc.txt']
    splitType = ' '

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
    # initData = set_initData_with_nonLabeledData(dir, fileName[-1], splitType)
    initData = [Loc,Nhan,Nghia,An,Binh,Linh,Phat,Trong,Nhan1,Nhan2,Nhan3,Nhan4,Nhan5,Nhan6,Nhan7]
    # k = 2 # for train_vn
    # k = 13 # for train_en
    k = 3 # spend_age
    dType = 1 # euclid distance

    if k > len(initData):
        print('k nhieu hon du lieu.')
        return
    kmeans = Kmeans(initData, k, dType)
    kmeans.initial_step()
    kmeans.update_step()
    
    for cluster in kmeans.kCluster:
        print(len(cluster))

    # for cluster in kmeans.kCluster:
    #     for point in cluster:
    #         print(point.display())

    # for cluster in kmeans.kIndex:
    #     for index in cluster:
    #         print(index + 1)
    

    




if __name__=="__main__": main()
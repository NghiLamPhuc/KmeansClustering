from PyQt5 import QtCore, QtGui, QtWidgets, uic
import read_file, write_file, make_folder
from RunConsole import set_initData_with_nonLabeledData, get_last_centers, predict_new_point_temporary
from Kmeans import Kmeans
from Point import Point
from datetime import datetime, timedelta
import sys

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('GUI.ui', self)

        openIcon = QtGui.QIcon('./GUIimage/openIcon')
        saveIcon = QtGui.QIcon('./GUIimage/saveIcon')
        runIcon = QtGui.QIcon('./GUIimage/runIcon')
        resIcon = QtGui.QIcon('./GUIimage/saveResIcon')
        pixmapLogo = QtGui.QPixmap('./GUIimage/logoIcon')
        
        self.btnImport.setIcon(openIcon)
        self.btnPredict.setIcon(resIcon)
        self.btnExport.setIcon(saveIcon)
        self.btnKmeans.setIcon(runIcon)
        self.labelLogo.setPixmap(pixmapLogo)

        self.btnKmeans.clicked.connect(self.on_Kmeans_clicked)
        self.btnPredict.clicked.connect(self.on_Predict_clicked)
        self.btnImport.clicked.connect(self.on_Import_clicked)
        self.btnExport.clicked.connect(self.on_Export_clicked)

        self.initData = None
        self.inputDir = './datasets/'
        self.fileInitName = None
        self.lastCentersName = 'lastCenters.txt'
        self.checkKmeans = 0
    
    def on_Export_clicked(self):
        inputDir = './datasets/'
        (dataPath, _) = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', inputDir, '*.txt')
        if dataPath:
            data = self.plainTextInput.toPlainText()
            with open(dataPath, 'w', encoding = 'utf-8') as f:
                f.write(data)

    def on_Import_clicked(self):
        self.labelLog.clear()
        self.labelInput.clear()
        self.labelInputName.setText('Dữ liệu số hóa')
        self.plainTextInput.clear()
        
        (dataPath, _) = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', self.inputDir, '*.txt')
        self.fileInitName = dataPath.split('/')[-1]
        if dataPath:
            self.initData = set_initData_with_nonLabeledData(self.inputDir, self.fileInitName, ' ')
            rowLen = len(self.initData)
            for (i, row) in enumerate(self.initData):
                rowStr = '[{0}]. {1}\n\n'.format(i, row.display())
                self.plainTextInput.insertPlainText(rowStr)
            self.labelInput.setText('Có {} dòng.'.format(rowLen) )
            self.labelInputName.setText(self.fileInitName)

    def on_Predict_clicked(self):
        instanceStr = self.lineEditPredict.text()
        if not instanceStr:
            self.labelLog.setText('Chưa nhập giá trị.')
        elif self.checkKmeans == 0:
            self.labelLog.setText('Chưa phân lớp.')
        else:
            dir = './outfile/' + self.fileInitName + '/'
            fileName = 'lastCenters.txt'
            lastCenters = get_last_centers(dir, fileName, ', ')
            inputNewPointStr = self.lineEditPredict.text()
            coordList = list()
            for coord in inputNewPointStr.split(','):
                coordList.append(float(coord))
            newPoint = Point(coordList)
            self.labelLog.setText('-->' + predict_new_point_temporary(lastCenters, newPoint))
    
    def on_Kmeans_clicked(self):
        if self.plainTextInput.toPlainText() == "":
            self.labelLog.setText('Chưa tải dữ liệu lên.')
        else:
            self.plainTextCluster.clear()
            k = float(self.spinBox.text())
            if k > len(self.initData):
                self.plainTextCluster.setText('K > số dòng dữ liệu, mời chọn lại K.')
            else:
                # dtype = 1 euclid distance, sau này nếu có cosin thì 2....
                self.plainTextCluster.clear()
                self.plainTextLastCenters.clear()
                
                start = datetime.now()
                kmeans = Kmeans(self.initData, k, 1, self.fileInitName)
                kmeans.initial_step()
                kmeans.update_step()
                exeTime = (datetime.now() - start).total_seconds()    
                
                #Hiển thị kết quả phân lớp.
                dir = './outfile/' + self.fileInitName + '/'
                fileClusterName = 'index_cluster.txt'
                indexClusterStr = open(dir + fileClusterName).read()
                self.plainTextCluster.insertPlainText(indexClusterStr)
                self.checkKmeans = 1
                #Hiển thị center cuối cùng.
                fileLastCentersName = 'lastCenters.txt'
                lastCentersStr = open(dir + fileLastCentersName).read()
                self.plainTextLastCenters.insertPlainText(lastCentersStr)
                
                self.labelLog.setText(str(timedelta(seconds = exeTime)))
            
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyWindow()
    window.setWindowTitle('K-means clustering')
    window.show()
    sys.exit(app.exec_())


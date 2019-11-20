from PyQt5 import QtCore, QtGui, QtWidgets, uic
import read_file, write_file, make_folder
from ReadDataInitialForKmeans import set_initData_with_nonLabeledData
from Kmeans import Kmeans
from Point import Point
from gensim.models import Word2Vec
from sentence2vec import Sentence2Vec
from underthesea import word_tokenize
from datetime import datetime, timedelta
import re
import sys

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('GUI.ui', self)

        imgDir = './GUIimage/'
        openIcon = QtGui.QIcon(imgDir + 'openIcon')
        saveIcon = QtGui.QIcon(imgDir + 'saveIcon')
        runIcon = QtGui.QIcon(imgDir + 'runIcon')
        resIcon = QtGui.QIcon(imgDir + 'saveResIcon')
        pixmapLogo = QtGui.QPixmap(imgDir + 'logoIcon')
        vectorIcon = QtGui.QIcon(imgDir + 'vectorIcon')
        
        self.btnImport.setIcon(openIcon)
        self.btnPredict.setIcon(resIcon)
        self.btnExport.setIcon(saveIcon)
        self.btnKmeans.setIcon(runIcon)
        self.btnVectorize.setIcon(vectorIcon)
        self.labelLogo.setPixmap(pixmapLogo)
        
        self.btnVectorize.clicked.connect(self.on_Vectorize_clicked)
        self.btnKmeans.clicked.connect(self.on_Kmeans_clicked)
        self.btnPredict.clicked.connect(self.on_Predict_clicked)
        self.btnImport.clicked.connect(self.on_Import_clicked)
        self.btnExport.clicked.connect(self.on_Export_clicked)
        self.spinBox.setValue(2)
        self.lineEditPredict.textChanged.connect(self.on_text_predict_changed)

        self.listRawSents = list()
        self.listSentToWord = list()
        self.initData = None
        self.inputDir = './datasets/'
        self.fileInitName = None
        self.checkKmeans = 0
        self.kMeans = None
    
    def on_Vectorize_clicked(self):
        if len(self.listRawSents) == 0:
            self.labelLog.setText('Chưa có câu.')
        else:
            linkFolder = 'outfile/{0}'.format(self.fileInitName)
            make_folder.create_folder(linkFolder)
            linkModel = linkFolder + '/word2vec.model'
            # token sentences --> to list
            for sent in self.listRawSents:
                tokens = word_tokenize(sent, format='text').split()
                words = []
                for token in tokens:
                    if re.match(r'^\w+', token):
                        words.append(token)
                self.listSentToWord.append(words)
            # training word2vec cho cái list tách từ.
            model = Word2Vec(self.listSentToWord, size=15, min_count=1)
            model.save(linkModel)
            sent2vec = Sentence2Vec(linkModel)
            listVect = []
            for sent in self.listRawSents:
                listVect.append(sent2vec.get_vector(sent).tolist())
            write_file.list_to_txt(listVect, linkFolder, 'Sent2Vect.txt')
            write_file.list_to_txt(self.listSentToWord, linkFolder, 'WordTokenize.txt')

            self.labelLog.setText('Đã lưu file vector.')

    def on_text_predict_changed(self):
        self.labelLog.clear()

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
        self.labelInputName.setText('Dữ liệu thô')
        self.plainTextInput.clear()
        self.plainTextCluster.clear()
        
        (dataPath, _) = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', self.inputDir, '*.txt')
        self.fileInitName = dataPath.split('/')[-1]
        if dataPath:
            # câu thô.
            self.listRawSents = read_file.read_line_to_sentenceList(self.inputDir, self.fileInitName, '\n')
            rowCount = len(self.listRawSents)
            for i in range(rowCount):
                rowStr = '[{0}]. {1}\n'.format(i, self.listRawSents[i])
                self.plainTextInput.insertPlainText(rowStr)

            # data đã số hóa.
            # self.initData = set_initData_with_nonLabeledData(self.inputDir, self.fileInitName, ' ')
            # rowLen = len(self.initData)
            # for (i, row) in enumerate(self.initData):
            #     rowStr = '[{0}]. {1}\n'.format(i, row.display())
            #     self.plainTextInput.insertPlainText(rowStr)
            self.labelInput.setText('Có {} dòng.'.format(rowCount) )
            self.labelInputName.setText(self.fileInitName)
            self.spinBox.setMaximum(rowCount)

    def on_Predict_clicked(self):
        newSent = self.lineEditPredict.text()
        if not newSent:
            self.labelLog.setText('Chưa nhập giá trị.')
        elif self.checkKmeans == 0:
            self.labelLog.setText('Chưa phân lớp.')
        else:
            linkModel = './outfile/{0}/word2vec.model'.format(self.fileInitName)
            sent2vec = Sentence2Vec(linkModel)
            vecSentList = sent2vec.get_vector(newSent).tolist()
            newPoint = Point(vecSentList)
            ### Đoạn này dùng với input là tọa độ.
            ## coordList = list()
            ## for coord in instanceStr.split(','):
            ##     coordList.append(float(coord))
            ## newPoint = Point(coordList)
            # self.labelLog.setText('({0}) --> {1}'.format(str(newPoint.display()), self.kMeans.predict_new_point(newPoint)) )
            self.labelLog.setText(' --> {0}'.format(self.kMeans.predict_new_point(newPoint)) )
    
    def on_Kmeans_clicked(self):
        if self.labelLog.text() != 'Đã lưu file vector.':
            self.labelLog.setText('Chưa số hóa dữ liệu.')
        elif self.plainTextInput.toPlainText() == "":
            self.labelLog.setText('Chưa tải dữ liệu lên.')
        else:
            self.plainTextCluster.clear()
            # dtype = 1 euclid distance, sau này nếu có cosin thì 2....
            self.plainTextCluster.clear()
            k = float(self.spinBox.text())
            if k == len(self.listRawSents):
                self.plainTextCluster.insertPlainText('Vì k bằng số dòng dữ liệu, nên mỗi dòng là một lớp.')
            else:
                start = datetime.now()
                # đọc initData từ Sent2Vect.txt
                sent2vect = read_file.read_lines_to_floatlist('./outfile/{0}/'.format(self.fileInitName), 'Sent2Vect.txt', ', ' )
                toPoints = []
                for vec in sent2vect:
                    toPoints.append(Point(vec))
                self.initData = toPoints
                self.kMeans = Kmeans(self.initData, k, 1, self.fileInitName)
                exeTime = (datetime.now() - start).total_seconds()    
                
                #Hiển thị kết quả phân lớp.
                dir = './outfile/' + self.fileInitName + '/kmeans/'
                fileClusterName = 'last_cluster_index.txt'
                indexClusterStr = open(dir + fileClusterName).read()
                self.plainTextCluster.insertPlainText(indexClusterStr)
                self.checkKmeans = 1
                
                self.labelLog.setText(str(timedelta(seconds = exeTime)))
            
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyWindow()
    window.setWindowTitle('K-means clustering')
    window.show()
    sys.exit(app.exec_())


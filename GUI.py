from PyQt5 import QtCore, QtGui, QtWidgets, uic
import read_file, write_file, make_folder
# from ReadDataInitialForKmeans import set_initData_with_nonLabeledData
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
        pixmapLogo = QtGui.QPixmap(imgDir + 'logoIconLarge')
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
        # self.btnScreenShot.clicked.connect(self.on_ScreenShot_clicked)

        self.spinBox.setValue(2)
        self.spinBoxVecSize.setValue(100)
        self.lineEditPredict.textChanged.connect(self.on_text_predict_changed)

        self.groupBoxVectorize.setEnabled(False)
        self.groupBoxKmeans.setEnabled(False)
        self.btnExport.setEnabled(False) ############################# Sau này thêm chức năng.
        self.labelInputName.setText('Dữ liệu')
        self.btnPredict.setEnabled(False)
        self.lineEditPredict.setEnabled(False)

        self.listRawSents = list()
        self.listSentToWord = list()
        self.initData = None
        self.inputDir = './datasets/'
        self.fileInitName = None
        self.checkKmeans = 0
        self.kMeans = None
        # 0, 1 sau này đưa về kiểu biến Str = 0 / 1
        self.checkVectorize = 0 # 0 khi chưa vector hóa, 1 khi vector hóa rồi.
        self.checkDataType = 0 # 0 khi Dữ liệu là text, 1 khi dữ liệu là vector.
    
    # def on_ScreenShot_clicked(self):
    #     screen = QtWidgets.QApplication.primaryScreen()
    #     screenshot = screen.grabWindow( QtWidgets.QWidget.winId() )
    #     screenshot.save('shot.jpg', 'jpg')
    #     QtWidgets.QWidget.close()

    def on_Vectorize_clicked(self):
        vectorSize = int(self.spinBoxVecSize.text())
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
            model = Word2Vec(self.listSentToWord, size=vectorSize, min_count=1)
            model.save(linkModel)
            sent2vec = Sentence2Vec(linkModel)
            listVect = []
            for sent in self.listRawSents:
                listVect.append(sent2vec.get_vector(sent).tolist())
            write_file.list_to_txt(listVect, linkFolder, 'Sent2Vect.txt')
            write_file.list_to_txt(self.listSentToWord, linkFolder, 'WordTokenize.txt')

            self.labelLog.setText('Đã lưu file vector.')
            self.checkVectorize = 1
            self.groupBoxKmeans.setEnabled(True)
            
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
        self.plainTextInput.clear()
        self.plainTextCluster.clear()
        self.lineEditPredict.clear()
        self.groupBoxVectorize.setEnabled(False)
        self.groupBoxKmeans.setEnabled(False)
        self.lineEditPredict.setEnabled(False)
        self.btnPredict.setEnabled(False)
        self.checkDataType = 0
        if self.radioVector.isChecked():
            self.checkDataType = 1
        
        self.checkVectorize = 0
        if self.radioVector.isChecked():
            self.checkDataType = 1
        # #################################################### input la text
        if self.checkDataType == 0:
            (dataPath, _) = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', self.inputDir, '*.txt')
            self.fileInitName = dataPath.split('/')[-1]
            if dataPath:
                # câu thô.
                self.listRawSents = read_file.read_line_to_sentenceList(self.inputDir, self.fileInitName, '\n')
                rowCount = len(self.listRawSents)
                for i in range(rowCount):
                    rowStr = '[{0}]. {1}\n'.format(i, self.listRawSents[i])
                    self.plainTextInput.insertPlainText(rowStr)

                self.labelInput.setText('Có {} dòng.'.format(rowCount) )
                self.labelInputName.setText(self.fileInitName)
                self.spinBox.setMaximum(rowCount)

            self.groupBoxVectorize.setEnabled(True)
        # ################################################# input la vector
        if self.checkDataType == 1:
            (dataPath, _) = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File', self.inputDir, '*.vector')
            self.fileInitName = dataPath.split('/')[-1]
            if dataPath:
                # data đã số hóa.
                # sent2vect = read_file.read_lines_to_floatlist_nonSquareBracklets(self.inputDir, self.fileInitName, ', ' )
                sent2vect = read_file.read_lines_to_floatlist(self.inputDir, self.fileInitName, ', ' )
                toPoints = []
                for vec in sent2vect:
                    toPoints.append(Point(vec))
                self.initData = toPoints

                rowCount = len(self.initData)
                for (i, row) in enumerate(self.initData):
                    rowStr = '[{0}]. {1}\n'.format(i, row.display())
                    self.plainTextInput.insertPlainText(rowStr)
                
                self.labelInput.setText('Có {} dòng.'.format(rowCount) )
                self.labelInputName.setText(self.fileInitName)
                self.spinBox.setMaximum(rowCount)

            self.groupBoxKmeans.setEnabled(True)

    def on_Predict_clicked(self):
        newSent = self.lineEditPredict.text()
        if self.checkDataType == 0:
            if not newSent:
                self.labelLog.setText('Chưa nhập câu.')
            elif self.checkKmeans == 0:
                self.labelLog.setText('Chưa phân lớp.')
            else:
                linkModel = './outfile/{0}/word2vec.model'.format(self.fileInitName)
                sent2vec = Sentence2Vec(linkModel)
                vecSentList = sent2vec.get_vector(newSent).tolist()
                newPoint = Point(vecSentList)
                self.labelLog.setText(' --> {0}'.format(self.kMeans.predict_new_point(newPoint)) )
        elif self.checkDataType == 1:
            if not newSent:
                self.labelLog.setText('Chưa nhập vector.')
            elif self.checkKmeans == 0:
                self.labelLog.setText('Chưa phân lớp.')
            else:
                coordList = list()
                for coord in newSent.split(','):
                    coordList.append(float(coord))
                newPoint = Point(coordList)
                self.labelLog.setText(' --> {0}'.format(self.kMeans.predict_new_point(newPoint)) )
    
    def on_Kmeans_clicked(self):
        self.plainTextCluster.clear()
        k = float(self.spinBox.text())
        ################################################# neu input la text
        if self.checkDataType == 0:
            if k == len(self.listRawSents):
                self.plainTextCluster.insertPlainText('Vì k bằng số dòng dữ liệu, nên mỗi dòng là một lớp.')
            else:
                # dtype = 1 euclid distance, sau này nếu có cosin thì 2....
                start = datetime.now()
                # đọc initData từ Sent2Vect.txt
                sent2vect = read_file.read_lines_to_floatlist('./outfile/{0}/'.format(self.fileInitName), 'Sent2Vect.txt', ', ' )
                toPoints = []
                for vec in sent2vect:
                    toPoints.append(Point(vec))
                self.initData = toPoints
                dType = 1
                # if self.radioButtonCosine.isChecked():
                #     dType = 2
                self.kMeans = Kmeans(self.checkDataType, self.initData, k, dType, self.fileInitName)
                exeTime = (datetime.now() - start).total_seconds()

                # Hiển thị kết quả phân lớp.
                dir = './outfile/' + self.fileInitName + '/kmeans_textinput/'
                fileClusterName = 'last_cluster_index.txt'
                indexClusterStr = open(dir + fileClusterName).read()
                self.plainTextCluster.insertPlainText(indexClusterStr)
            
        ######################## input la vector
        elif self.checkDataType == 1:
            if k == len(self.initData):
                self.plainTextCluster.insertPlainText('Vì k bằng số dòng dữ liệu, nên mỗi dòng là một lớp.')
            else:
                dType = 1
                # if self.radioButtonCosine.isChecked():
                #     dType = 2
                start = datetime.now()
                self.kMeans = Kmeans(self.checkDataType, self.initData, k, dType, self.fileInitName)
                exeTime = (datetime.now() - start).total_seconds()

                # Hiển thị kết quả phân lớp.
                dir = './outfile/' + self.fileInitName + '/kmeans_vectorinput/'
                fileClusterName = 'last_cluster_index.txt'
                indexClusterStr = open(dir + fileClusterName).read()
                self.plainTextCluster.insertPlainText(indexClusterStr)
        
        self.labelLog.setText(str(timedelta(seconds = exeTime)))
        self.checkKmeans = 1
        self.btnPredict.setEnabled(True)
        self.lineEditPredict.setEnabled(True)
        ## 
        hint = 'Nhập tọa độ vector.'
        if self.checkDataType == 0:
            hint = 'Nhập câu.'
        self.lineEditPredict.setPlaceholderText(hint)
            
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MyWindow()
    window.setWindowTitle('K-means clustering')
    window.show()
    sys.exit(app.exec_())


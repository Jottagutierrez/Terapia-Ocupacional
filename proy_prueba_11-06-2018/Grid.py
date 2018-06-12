import sys
from PyQt5.QtWidgets import QSizePolicy, QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QMainWindow, QLabel, QDesktopWidget, QDoubleSpinBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QRect, Qt
from PyQt5 import QtGui
import matplotlib.pyplot as plt
import numpy as npy
import mplcursors
import model_solver_script as mss
import module_export as mexp
import db_processing_script as dbp

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
 
class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Asignación Terapia Ocupacional Universidad de los Andes'
        self.left = 600 #cambia la posicion con respecto a la esquina superior izquierda
        self.top = 300  #cambia la posicion con respecto a la esquina superior izquierda
        self.width = 1000 #cambia el ancho de la ventana
        self.height = 600 #cambia el alto de la ventana
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title) #setea el nombre de la ventana
        self.setGeometry(self.left, self.top, self.width, self.height) #setea el tamaño de la ventana y su posición inicial
        
        #centra la ventana parametricamente segun la geometría de la pantalla
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center() #encuentra el centro de la pantalla
        qr.moveCenter(cp) #hace coincidir el centro de la ventana con el de la pantalla
        self.move(qr.topLeft())
 
        #genera un grid sobre el cual se posicionaran los widgets
        self.createGridLayout() #se llama la función createGridLyout
        #windowLayout = QVBoxLayout()#no tengo idea
        #windowLayout.addWidget(self.horizontalGroupBox)
        #self.setLayout(windowLayout)#no tengo idea
        self.showMaximized()#muestra la ventana en pantalla completa
 
    def createGridLayout(self):
        #self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        self.setLayout(layout)
        #layout.setColumnStretch(0, 300)
        #layout.setColumnStretch(2, 3)
        
        #crea los botones y los relaciona con su respectiva función
        btn1 = QPushButton('Subir Base de Datos')
        #btn1.resize(btn1.sizeHint())#automatiza su tamaño
        layout.addWidget(btn1,2,0) #añade widget en el grid fila, columna
        btn1.setMinimumSize(0,40)
        btn1.clicked.connect(self.upload)
        
        btn2 = QPushButton('Exportar resultados')
        btn2.setMinimumSize(0,40)
        btn2.resize(btn2.sizeHint())
        layout.addWidget(btn2,2,2) 
        btn2.clicked.connect(self.export)
        
        btn3 = QPushButton('Salir')
        btn3.setMinimumSize(0,40)
        btn3.resize(btn3.sizeHint())
        layout.addWidget(btn3,2,4)
        btn3.clicked.connect(self.cancel)
        
        self.figure = plt.figure(figsize = (15,5)) #genera el atributo figura
        self.canvas = FigureCanvas(self.figure) #relaciona la figura (plot) a el canvas
        self.toolbar = NavigationToolbar(self.canvas,self) #relaciona la toolbar con el canvas
        layout.addWidget(self.canvas, 1,1,1,3) #agrega widget (widget, fila, columna, span fila, span columna)
        layout.addWidget(self.toolbar, 0,0,1,3)
 
        #self.horizontalGroupBox.setLayout(layout)
        
    def upload(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"Seleccione Planilla de Datos", "","Hoja de Cálculo (*.xlsx)", options=options)
        if fileName:
            dbp.processing(fileName)
            deltaOptions =[i/100 for i in range(100)]
            DataFrame=mss.correr(deltaOptions)
            self.x=DataFrame[0]
            self.y=DataFrame[1]
            self.deltaOptions=DataFrame[2]
            self.graficar()
        

    def graficar(self):
        plt.cla()
        ax = self.figure.add_subplot(111)
        #self.x = [i for i in range(100)]
        #self.y = [0.95**i for i in self.x]
        #ax.plot(self.x, self.y, '-', color='blue')
        print('Y vale: '+ str(self.y))
        #print('X vale: ' + str(self.x[0]))
        ax.scatter(self.x, self.y, color='blue', picker=1)
        
        plt.xlabel('Costo')
        plt.ylabel('Sobrecarga Total')
        plt.tight_layout(rect=[0, 0, 1, 0.985])
        ax.set_title('Curva Óptima')
        #mplcursors.cursor(hover=False)
        self.highlight, = ax.plot([], [], 'o', color='red')
        self.figure.canvas.mpl_connect('pick_event', self.onPick)
        
        c1 = mplcursors.cursor(hover=False)
        @c1.connect("add")
        def _(sel):
            sel.annotation.set(position=(100-self.ind, self.ind/2))
            # Note: Needs to be set separately due to matplotlib/matplotlib#8956.
            sel.annotation.arrow_patch.set(arrowstyle="simple", fc="white", alpha=.5)
            sel.annotation.get_bbox_patch().set(fc="pink")
        
        self.canvas.draw()
        #pcs.procesar()
        
    def onPick(self, event=None):
        '''this_point = event.artist
        x_value = this_point.get_xdata()
        y_value = this_point.get_ydata()'''
        self.ind = event.ind
        self.highlight.set_data(npy.take(self.x, self.ind),npy.take(self.y, self.ind))
        self.canvas.draw_idle()
        
            
    def export(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,"Guardar Archivo","","Hoja de Cálculo (*.xlsx);;Text Files (*.txt)", options=options)
        if fileName:
            DataFrame =mss.correr(self.ind/100)
            G=DataFrame[3]
            Conj_B=DataFrame[4]#
            Conj_U=DataFrame[5]#
            Conj_S=DataFrame[6]#
            Conj_Lin=DataFrame[7]
            X=DataFrame[8]#
            Y=DataFrame[9]#
            W=DataFrame[10]
            week_keys=DataFrame[11]#
            cent_keys=DataFrame[12]
            cent_info=DataFrame[13]
            mexp.F_export_model_results(G, Conj_B, Conj_U, Conj_S, Conj_Lin, X, Y, W, week_keys, cent_keys, cent_info, fileName)
            print(fileName)
        
    
    def cancel(self):
        self.close()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
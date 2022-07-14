import os
import sys  # 系统参数操作
from os import listdir
from os.path import isfile, join
import PyQt5
import pydicom
from PyQt5 import QtCore
from PyQt5.QtWidgets import *  # 模块包含创造经典桌面风格的用户界面提供了一套UI元素的类
from PyQt5.QtCore import *  # 此模块用于处理时间、文件和目录、各种数据类型、流、URL、MIME类型、线程或进程
from PyQt5.QtGui import *  # 含类窗口系统集成、事件处理、二维图形、基本成像、字体和文本
from scipy import ndimage
import vtkmodules.all as vtk
from vtk.util import numpy_support
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import pyqtgraph as pg
import math as mathh
from vtkmodules.util import numpy_support
from VtkUI import VtkUI
from qt.InformationalUI import InformationalUI
import numpy as np
import json


class VtkUIrealize(QMainWindow):
    def __init__(self):
        super(VtkUIrealize, self).__init__()
        # 项目绘画数据{project:{index:[index]}}
        self.drew_up_data = {}
        self.drew_left_data = {}
        self.drew_front_data = {}

        self.add_project_color_rgb = ""
        self.ui = VtkUI()
        self.ui.setupUi(self)
        self.setWindowTitle("医学影像辅助软件")
        self.setWindowModality(PyQt5.QtCore.Qt.ApplicationModal)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowModality(PyQt5.QtCore.Qt.ApplicationModal)

        uis = [self.ui.up_drew_graphicsview, self.ui.front_drew_graphicsview, self.ui.left_drew_graphicsview]
        for ui in uis:
            ui.viewport().installEventFilter(self)
            ui.setAspectLocked()
            ############hiding the axis##################

            ui.getPlotItem().hideAxis('left')
            ui.getPlotItem().hideAxis('bottom')
            ui.setMouseEnabled(x=False, y=False)

        f = open("project.txt", encoding='utf-8')
        txt = []
        for line in f:
            txt.append(line.strip())
        f.close()
        # 项目路径
        self.path = txt[0]

        f = open(self.path + "/init.txt", encoding='utf-8')
        txt = []
        for line in f:
            txt.append(line.strip())
        f.close()

        # 保存项目名称和颜色信息
        self.project_name = []
        self.project_color_R = []
        self.project_color_G = []
        self.project_color_B = []

        # 添加项目列表 背景底色 rgb
        for i in range(1, len(txt)):
            label = txt[i].split(',')
            self.ui.project_list.addItem(label[0])
            self.project_name.append(label[0])
            self.ui.project_list.item(i - 1).setBackground(QColor(int(label[1]), int(label[2]), int(label[3])))
            self.project_color_R.append(int(label[1]))
            self.project_color_G.append(int(label[2]))
            self.project_color_B.append(int(label[3]))
        # 加载绘画数据
        if os.path.isfile(self.path + "/up_data.json"):
            with open(self.path + "/up_data.json", 'r', encoding='utf8') as fp:
                drew_up_data_temp = json.load(fp)
            for key,value in drew_up_data_temp.items():
                self.drew_up_data[key] = {}
                for index,data in value.items():
                    self.drew_up_data[key][int(index)] = data

        if os.path.isfile(self.path + "/front_data.json"):
            with open(self.path + "/front_data.json", 'r', encoding='utf8') as fp:
                drew_front_data_temp = json.load(fp)
            for key,value in drew_front_data_temp.items():
                self.drew_front_data[key] = {}
                for index, data in value.items():
                    self.drew_front_data[key][int(index)] = data

        if os.path.isfile(self.path + "/left_data.json"):
            with open(self.path + "/left_data.json", 'r', encoding='utf8') as fp:
                drew_left_data_temp = json.load(fp)
            for key,value in drew_left_data_temp.items():
                self.drew_left_data[key] = {}
                for index, data in value.items():
                    self.drew_left_data[key][int(index)] = data

        # 绘制三视图
        self.slices = [pydicom.dcmread(self.path + "/dict" + '/' + s, force=True) for s in
                       os.listdir(self.path + "/dict")]
        self.slices = [s for s in self.slices if 'SliceLocation' in s]
        self.slices.sort(key=lambda x: int(x.InstanceNumber))
        try:
            slice_thickness = np.abs(self.slices[0].ImagePositionPatient[2] - self.slices[1].ImagePositionPatient[2])
        except:
            slice_thickness = np.abs(self.slices[0].SliceLocation - self.slices[1].SliceLocation)
        for s in self.slices:
            s.SliceThickness = slice_thickness
        self.ConstPixelDims = (int(self.slices[0].Rows), int(self.slices[0].Columns), len(self.slices))
        self.ConstPixelSpacing = (
            float(self.slices[0].PixelSpacing[0]), float(self.slices[0].PixelSpacing[1]),
            float(self.slices[0].SliceThickness))

        self.ArrayDicom = np.zeros(self.ConstPixelDims, dtype=self.slices[0].pixel_array.dtype)
        idx = len(self.slices) - 1
        for s in self.slices:
            self.ArrayDicom[:, :, idx] = s.pixel_array
            idx -= 1
        for i in range(3):
            self.ArrayDicom = np.rot90(self.ArrayDicom, 1, axes=(0, 1))
        self.img = self.ArrayDicom[:, :, int(self.ArrayDicom.shape[2] / 2)]
        self.indexOriginal = int(self.ArrayDicom.shape[2] / 2)
        self.image = pg.ImageItem(self.img)
        # Step 1 3D numpy ---> VTK_ARRAY
        NumPy_data_shape = self.ArrayDicom.shape
        VTK_data = numpy_support.numpy_to_vtk(
            num_array=self.ArrayDicom.transpose(2, 1, 0).ravel(),
            # ndarray contains the fitting result from the points. It is a 3D array
            deep=True,
            array_type=vtk.VTK_FLOAT)

        # Step 2 VTK_ARRAY ----> VTK__IMAGE_DATA
        img_vtk2 = vtk.vtkImageData()
        img_vtk2.GetPointData().SetScalars(VTK_data)
        img_vtk2.SetDimensions(NumPy_data_shape)
        img_vtk2.SetSpacing(self.ConstPixelSpacing[0], self.ConstPixelSpacing[1], self.ConstPixelSpacing[2])

        #######################origin of reslicing matrix################
        center = [0 + self.ConstPixelSpacing[0] * 0.5 * (0 + self.ArrayDicom.shape[0]),
                  0 + self.ConstPixelSpacing[1] * 0.5 * (0 + self.ArrayDicom.shape[1]),
                  0 + self.ConstPixelSpacing[2] * 0.5 * (0 + self.ArrayDicom.shape[2])]

        ####################coronal reslicing matrix####################
        coronal = vtk.vtkMatrix4x4()
        coronal.DeepCopy((1, 0, 0, 0,
                          0, 0, 1, 0,
                          0, -1, 0, 1,
                          0, 0, 0, 1))
        ####################sagittal reslicing matrix####################
        sagittal = vtk.vtkMatrix4x4()
        sagittal.DeepCopy((0, 0, -1, center[0],
                           1, 0, 0, center[1],
                           0, -1, 0, center[2],
                           0, 0, 0, 1))
        ####################oblique basic reslicing matrix####################
        oblique = vtk.vtkMatrix4x4()
        oblique.DeepCopy((0.0, -0.515038, 0.857167, center[0],
                          0.0, 0.857167, 0.515038, center[1],
                          -1.0, 0.0, 0.0, center[2],
                          0.0, 0.0, 0.0, 1.0))

        self.sagittalView = self.viewOption(sagittal, img_vtk2)
        self.coronalView = self.viewOption(coronal, img_vtk2)

        self.obliqueView = self.ObliqueReconstruct(self.ArrayDicom, 45)
        self.sagittalView = np.flip(self.sagittalView, axis=0)
        self.sagittalView = self.sagittalView[:, :, ::-1]

        self.left_view = self.sagittalView
        self.left_view_index = int(len(self.left_view) / 2)
        self.ui.left_drew_graphicsview.addItem(pg.ImageItem(self.left_view[:, :, self.left_view_index]))
        data = self.getDrewdata(self.drew_left_data, self.left_view_index)
        self.ui.left_drew_qlabe.data_init = data

        self.front_view = self.coronalView
        self.front_view_index = int(len(self.front_view) / 2)
        self.ui.front_drew_graphicsview.addItem(pg.ImageItem(self.front_view[:, :, self.front_view_index]))
        data = self.getDrewdata(self.drew_front_data, self.front_view_index)
        self.ui.front_drew_qlabe.data_init = data

        for i in range(2):
            self.obliqueView = np.rot90(self.obliqueView, 1, axes=(0, 1))
        ##################################axial view##############################

        self.up_view = self.obliqueView
        self.up_view_index = int(len(self.up_view) / 2)
        self.ui.up_drew_graphicsview.addItem(pg.ImageItem(self.up_view[:, :, self.up_view_index]))
        data = self.getDrewdata(self.drew_up_data, self.up_view_index)
        self.ui.up_drew_qlabe.data_init = data

        # 设置QSpinBox
        self.ui.up_index_spinbox.setRange(len(self.up_view), 1)
        self.ui.up_index_spinbox.setValue(self.up_view_index + 1)
        self.ui.up_index_spinbox.setSingleStep(1)

        self.ui.front_index_spinbox.setRange(len(self.front_view), 1)
        self.ui.front_index_spinbox.setValue(self.front_view_index + 1)
        self.ui.front_index_spinbox.setSingleStep(1)

        self.ui.left_index_spinbox.setRange(len(self.left_view), 1)
        self.ui.left_index_spinbox.setValue(self.up_view_index + 1)
        self.ui.left_index_spinbox.setSingleStep(1)

        # 绘制3d图形
        self.ui.vl = QVBoxLayout()
        self.ui.vtkWidget = QVTKRenderWindowInteractor(self.ui.three_drew_frame)
        self.ui.vl.addWidget(self.ui.vtkWidget)
        self.ui.ren = vtk.vtkRenderer()
        self.ui.vtkWidget.GetRenderWindow().AddRenderer(self.ui.ren)
        self.ui.iren = self.ui.vtkWidget.GetRenderWindow().GetInteractor()

        reader = vtk.vtkDICOMImageReader()
        reader.SetDirectoryName(self.path + "/dict")

        contourfilter = vtk.vtkContourFilter()
        contourfilter.SetInputConnection(reader.GetOutputPort())
        contourfilter.SetValue(0, 300)

        normal = vtk.vtkPolyDataNormals()
        normal.SetInputConnection(contourfilter.GetOutputPort())
        normal.SetFeatureAngle(60)

        conMapper = vtk.vtkPolyDataMapper()
        conMapper.SetInputConnection(normal.GetOutputPort())
        conMapper.ScalarVisibilityOff()

        conActor = vtk.vtkActor()
        conActor.SetMapper(conMapper)

        boxFilter = vtk.vtkOutlineFilter()
        boxFilter.SetInputConnection(reader.GetOutputPort())

        boxMapper = vtk.vtkPolyDataMapper()
        boxMapper.SetInputConnection(boxFilter.GetOutputPort())

        boxActor = vtk.vtkActor()
        boxActor.SetMapper(boxMapper)
        boxActor.GetProperty().SetColor(255, 255, 255)

        camera = vtk.vtkCamera()
        camera.SetViewUp(0, 0, -1)
        camera.SetPosition(0, 1, 0)
        camera.SetFocalPoint(0, 0, 0)
        camera.ComputeViewPlaneNormal()
        camera.Dolly(1.5)

        self.ui.ren.SetActiveCamera(camera)
        self.ui.ren.AddActor(boxActor)
        self.ui.ren.AddActor(conActor)
        self.ui.ren.ResetCamera()
        self.ui.three_drew_frame.setLayout(self.ui.vl)
        self.ui.iren.Initialize()

        # 绑定函数
        # 按钮
        self.ui.add_project_color_button.clicked.connect(self.Button_add_project_color)
        self.ui.add_project_button.clicked.connect(self.Button_add_projectr)
        self.ui.del_project_button.clicked.connect(self.Button_del_projectr)

        self.ui.up_drew_button.clicked.connect(self.Button_up_drew)
        self.ui.up_clear_button.clicked.connect(self.Button_up_clear)

        self.ui.left_drew_button.clicked.connect(self.Button_left_drew)
        self.ui.left_clear_button.clicked.connect(self.Button_left_clear)

        self.ui.front_drew_button.clicked.connect(self.Button_front_drew)
        self.ui.front_clear_button.clicked.connect(self.Button_front_clear)

        self.ui.save_button.clicked.connect(self.Button_save)

    def viewOption(self, vtkResliceMatrix, img_vtk2):
        # Extract a slice in the desired orientation
        reslice = vtk.vtkImageReslice()
        reslice.SetInputData(img_vtk2)
        reslice.SetOutputDimensionality(3)

        # reslice.SetOutputSpacing(img_vtk2.GetSpacing())

        # *************************** #

        reslice.SetResliceAxes(vtkResliceMatrix)
        reslice.SetInterpolationModeToLinear()

        reslice.Update()

        reslicedImg = reslice.GetOutput()

        reslicedNpImg = self.vtkToNumpy(reslicedImg)

        return reslicedNpImg

    def vtkToNumpy(self, data):
        temp = vtk_to_numpy(data.GetPointData().GetScalars())
        dims = data.GetDimensions()
        numpy_data = temp.reshape(dims[2], dims[1], dims[0])
        numpy_data = numpy_data.transpose(2, 1, 0)
        return numpy_data

    def Button_add_project_color(self):
        self.add_project_color_rgb = QColorDialog.getColor().getRgb()

    def Button_add_projectr(self):
        if self.ui.add_project_name_line.text() == "":
            self.informationalUI = InformationalUI("请输入要添加的项目名称！")
            self.informationalUI.show()
            return
        if self.ui.add_project_name_line.text() in self.project_name:
            self.informationalUI = InformationalUI("新建的项目名称重复请重新输入！")
            self.informationalUI.show()
            return
        if self.add_project_color_rgb == "":
            self.informationalUI = InformationalUI("请选择添加项目的颜色！")
            self.informationalUI.show()
            return
        # 获取所有元素的索引
        list_index = [i for i, a in enumerate(self.project_color_R) if a == self.add_project_color_rgb[0]]
        for i in list_index:
            if self.project_color_G[i] == self.add_project_color_rgb[1] and self.project_color_B[i] == \
                    self.add_project_color_rgb[2]:
                self.informationalUI = InformationalUI("项目颜色重复请重新选择！")
                self.informationalUI.show()
                return

        self.ui.project_list.addItem(self.ui.add_project_name_line.text())
        self.project_name.append(self.ui.add_project_name_line.text())
        self.ui.project_list.item(len(self.project_name) - 1).setBackground(QColor(self.add_project_color_rgb[0],
                                                                                   self.add_project_color_rgb[1],
                                                                                   self.add_project_color_rgb[2]))
        self.project_color_R.append(int(self.add_project_color_rgb[0]))
        self.project_color_G.append(int(self.add_project_color_rgb[1]))
        self.project_color_B.append(int(self.add_project_color_rgb[2]))

        self.drew_up_data[self.ui.add_project_name_line.text()] = {}

        self.informationalUI = InformationalUI("项目添加成功！")
        self.informationalUI.show()

    def Button_del_projectr(self):
        project_num = self.project_name.index(self.ui.project_list.currentItem().text())
        self.project_name.pop(project_num)
        self.project_color_R.pop(project_num)
        self.project_color_G.pop(project_num)
        self.project_color_B.pop(project_num)
        self.ui.project_list.takeItem(project_num)

        #
        self.drew_up_data.pop(project_num)
        self.drew_front_data.pop(project_num)
        self.drew_left_data.pop(project_num)
        self.informationalUI = InformationalUI("项目删除成功！")
        self.informationalUI.show()

    # 上视图绘画
    def Button_up_drew(self):
        if not self.ui.up_drew_qlabe.drew_flag:
            self.ui.up_drew_qlabe.drew_flag = True
            data = self.getDrewdata(self.drew_up_data, self.up_view_index)
            project_num = self.project_name.index(self.ui.project_list.currentItem().text())
            self.ui.up_drew_qlabe.color = QColor(self.project_color_R[project_num],
                                                 self.project_color_G[project_num],
                                                 self.project_color_B[project_num])
            self.ui.up_drew_qlabe.data = []
            self.ui.up_drew_qlabe.data_init = data
            self.ui.project_list.setEnabled(False)
            self.ui.up_drew_button.setText("停止绘画")
        else:
            self.ui.up_drew_qlabe.drew_flag = False
            self.ui.up_drew_button.setText("开始绘画")
            if not self.ui.front_drew_qlabe.drew_flag and not self.ui.left_drew_qlabe.drew_flag:
                self.ui.project_list.setEnabled(True)
            if len(self.ui.up_drew_qlabe.data) != 0:
                if self.ui.project_list.currentItem().text() not in self.drew_up_data:
                    self.drew_up_data[self.ui.project_list.currentItem().text()] = {
                        self.up_view_index: self.ui.up_drew_qlabe.data}
                else:
                    if self.up_view_index not in self.drew_up_data[self.ui.project_list.currentItem().text()]:
                        self.drew_up_data[self.ui.project_list.currentItem().text()][
                            self.up_view_index] = self.ui.up_drew_qlabe.data
                    else:
                        self.drew_up_data[self.ui.project_list.currentItem().text()][self.up_view_index].append(
                            (-1, -1))
                        self.drew_up_data[self.ui.project_list.currentItem().text()][self.up_view_index].extend(
                            self.ui.up_drew_qlabe.data)
            data = self.getDrewdata(self.drew_up_data, self.up_view_index)
            self.ui.up_drew_qlabe.data_init = data

    # 上视图绘画清空 两种情况 一个是绘画中删除是删除本次绘画过程中的 非绘画中是彻底删除该项目的
    def Button_up_clear(self):
        # 正在绘画中
        if self.ui.up_drew_qlabe.drew_flag:
            self.ui.up_drew_qlabe.data = []
        else:
            if self.ui.project_list.currentItem().text() in self.drew_up_data:
                if self.up_view_index in self.drew_up_data[self.ui.project_list.currentItem().text()]:
                    self.drew_up_data[self.ui.project_list.currentItem().text()].pop(self.up_view_index)
                    data = self.getDrewdata(self.drew_up_data, self.up_view_index)
                    self.ui.up_drew_qlabe.data_init = data

    # 左视图绘画
    def Button_left_drew(self):
        if not self.ui.left_drew_qlabe.drew_flag:
            self.ui.left_drew_qlabe.drew_flag = True
            data = self.getDrewdata(self.drew_left_data, self.left_view_index)
            project_num = self.project_name.index(self.ui.project_list.currentItem().text())
            self.ui.left_drew_qlabe.color = QColor(self.project_color_R[project_num],
                                                   self.project_color_G[project_num],
                                                   self.project_color_B[project_num])
            self.ui.left_drew_qlabe.data = []
            self.ui.left_drew_qlabe.data_init = data
            self.ui.project_list.setEnabled(False)
            self.ui.left_drew_button.setText("停止绘画")
        else:
            self.ui.left_drew_qlabe.drew_flag = False
            self.ui.left_drew_button.setText("开始绘画")
            if not self.ui.front_drew_qlabe.drew_flag and not self.ui.up_drew_qlabe.drew_flag:
                self.ui.project_list.setEnabled(True)
            if len(self.ui.left_drew_qlabe.data) != 0:
                if self.ui.project_list.currentItem().text() not in self.drew_left_data:
                    self.drew_left_data[self.ui.project_list.currentItem().text()] = {
                        self.left_view_index: self.ui.left_drew_qlabe.data}
                else:
                    if self.left_view_index not in self.drew_left_data[self.ui.project_list.currentItem().text()]:
                        self.drew_left_data[self.ui.project_list.currentItem().text()][
                            self.left_view_index] = self.ui.left_drew_qlabe.data
                    else:
                        self.drew_left_data[self.ui.project_list.currentItem().text()][self.left_view_index].append(
                            (-1, -1))
                        self.drew_left_data[self.ui.project_list.currentItem().text()][self.left_view_index].extend(
                            self.ui.left_drew_qlabe.data)
            data = self.getDrewdata(self.drew_left_data, self.left_view_index)
            self.ui.left_drew_qlabe.data_init = data

    # 左视图绘画清空 两种情况 一个是绘画中删除是删除本次绘画过程中的 非绘画中是彻底删除该项目的
    def Button_left_clear(self):
        # 正在绘画中
        if self.ui.left_drew_qlabe.drew_flag:
            self.ui.left_drew_qlabe.data = []
        else:
            if self.ui.project_list.currentItem().text() in self.drew_left_data:
                if self.left_view_index in self.drew_left_data[self.ui.project_list.currentItem().text()]:
                    self.drew_left_data[self.ui.project_list.currentItem().text()].pop(self.left_view_index)
                    data = self.getDrewdata(self.drew_left_data, self.left_view_index)
                    self.ui.left_drew_qlabe.data_init = data

    # 前视图绘画
    def Button_front_drew(self):
        if not self.ui.front_drew_qlabe.drew_flag:
            self.ui.front_drew_qlabe.drew_flag = True
            data = self.getDrewdata(self.drew_front_data, self.front_view_index)
            project_num = self.project_name.index(self.ui.project_list.currentItem().text())
            self.ui.front_drew_qlabe.color = QColor(self.project_color_R[project_num],
                                                    self.project_color_G[project_num],
                                                    self.project_color_B[project_num])
            self.ui.front_drew_qlabe.data = []
            self.ui.front_drew_qlabe.data_init = data
            self.ui.project_list.setEnabled(False)
            self.ui.front_drew_button.setText("停止绘画")
        else:
            self.ui.front_drew_qlabe.drew_flag = False
            self.ui.front_drew_button.setText("开始绘画")
            if not self.ui.up_drew_qlabe.drew_flag and not self.ui.left_drew_qlabe.drew_flag:
                self.ui.project_list.setEnabled(True)
            if len(self.ui.front_drew_qlabe.data) != 0:
                if self.ui.project_list.currentItem().text() not in self.drew_front_data:
                    self.drew_front_data[self.ui.project_list.currentItem().text()] = {
                        self.front_view_index: self.ui.front_drew_qlabe.data}
                else:
                    if self.front_view_index not in self.drew_front_data[self.ui.project_list.currentItem().text()]:
                        self.drew_front_data[self.ui.project_list.currentItem().text()][
                            self.front_view_index] = self.ui.front_drew_qlabe.data
                    else:
                        self.drew_front_data[self.ui.project_list.currentItem().text()][self.front_view_index].append(
                            (-1, -1))
                        self.drew_front_data[self.ui.project_list.currentItem().text()][self.front_view_index].extend(
                            self.ui.front_drew_qlabe.data)
            data = self.getDrewdata(self.drew_front_data, self.front_view_index)
            self.ui.front_drew_qlabe.data_init = data

    # 前视图绘画清空 两种情况 一个是绘画中删除是删除本次绘画过程中的 非绘画中是彻底删除该项目的
    def Button_front_clear(self):
        # 正在绘画中
        if self.ui.front_drew_qlabe.drew_flag:
            self.ui.front_drew_qlabe.data = []
        else:
            if self.ui.project_list.currentItem().text() in self.drew_front_data:
                if self.front_view_index in self.drew_front_data[self.ui.project_list.currentItem().text()]:
                    self.drew_front_data[self.ui.project_list.currentItem().text()].pop(self.front_view_index)
                    data = self.getDrewdata(self.drew_front_data, self.front_view_index)
                    self.ui.front_drew_qlabe.data_init = data

    # 保存数据
    def Button_save(self):
        with open(self.path + "/init.txt", "w", encoding='utf-8') as f:
            f.write("ykx")
            for i in range(len(self.project_name)):
                f.write("\n")
                f.write(self.project_name[i] + "," + str(self.project_color_R[i]) + "," +
                        str(self.project_color_G[i]) + "," + str(self.project_color_B[i]))
        json_str = json.dumps(self.drew_up_data)
        with open(self.path + '/up_data.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json_str)
        json_str = json.dumps(self.drew_front_data)
        with open(self.path + '/front_data.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json_str)
        json_str = json.dumps(self.drew_left_data)
        with open(self.path + '/left_data.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json_str)
        self.informationalUI = InformationalUI("保存数据成功！")
        self.informationalUI.show()

    def getDrewdata(self, data, index):
        res = {}
        for i in range(len(self.project_name)):
            if self.project_name[i] in data:
                if index in data[self.project_name[i]]:
                    res[str(self.project_color_R[i]) + "_" + str(self.project_color_G[i]) + "_" + str(
                        self.project_color_B[i])] \
                        = data[self.project_name[i]][index]
        return res

    def ObliqueReconstruct(self, Array, Angle, PlaneAngle=90):

        Array2 = Array.copy()
        if (Angle != 0):
            Array2 = ndimage.rotate(Array2, angle=Angle, reshape=True)

        center = [0 + self.ConstPixelSpacing[0] * 0.5 * (0 + Array.shape[0]),
                  0 + self.ConstPixelSpacing[1] * 0.5 * (0 + Array.shape[1]),
                  0 + self.ConstPixelSpacing[2] * 0.5 * (0 + Array.shape[2])]

        # Step 1 3D numpy ---> VTK_ARRAY
        NumPy_data_shape = Array2.shape
        VTK_data = numpy_support.numpy_to_vtk(
            num_array=Array2.transpose(2, 1, 0).ravel(),
            # ndarray contains the fitting result from the points. It is a 3D array
            deep=True,
            array_type=vtk.VTK_FLOAT)

        # Step 2 VTK_ARRAY ----> VTK__IMAGE_DATA
        img_vtk2 = vtk.vtkImageData()
        img_vtk2.GetPointData().SetScalars(VTK_data)
        img_vtk2.SetDimensions(NumPy_data_shape)
        img_vtk2.SetSpacing(self.ConstPixelSpacing[0], self.ConstPixelSpacing[1], self.ConstPixelSpacing[2])

        reslice = vtk.vtkImageReslice()
        reslice.SetInputData(img_vtk2)
        reslice.SetOutputDimensionality(3)

        # reslice.SetOutputSpacing(img_vtk2.GetSpacing())

        # *************************** #

        # reslice.SetResliceAxes(vtkResliceMatrix)

        reslice.SetResliceAxesOrigin(center[0], center[1], center[2])

        reslice.SetResliceAxesDirectionCosines(1, 0, 0,
                                               0, mathh.cos(mathh.radians(PlaneAngle)),
                                               -mathh.sin(mathh.radians(PlaneAngle)),
                                               0, mathh.sin(mathh.radians(PlaneAngle)),
                                               mathh.cos(mathh.radians(PlaneAngle)))

        reslice.SetInterpolationModeToLinear()

        reslice.Update()

        reslicedImg = reslice.GetOutput()

        reslicedNpImg = self.vtkToNumpy(reslicedImg)
        for i in range(2):
            reslicedNpImg = np.rot90(reslicedNpImg, 1, axes=(0, 1))
        # reslicedNpImg = rotate(reslicedNpImg, angle=45)
        return reslicedNpImg

    ################################Handles the scrolling of the mouse####################
    # 滚轮切换图片
    def eventFilter(self, watched, event):
        if (watched == self.ui.up_drew_graphicsview and
                event.type() == QtCore.QEvent.Wheel):
            print(self.ui.up_drew_qlabe.drew_flag)
            if self.ui.up_drew_qlabe.drew_flag:
                return True
            if event.angleDelta().y() > 0:
                self.up_view_index += 1
                if self.up_view_index == len(self.up_view):
                    self.up_view_index = len(self.up_view) - 1
                else:
                    img = self.up_view[:, :, self.up_view_index]
                    self.image = pg.ImageItem(img)
                    self.ui.up_drew_graphicsview.addItem(self.image)
                    data = self.getDrewdata(self.drew_up_data, self.up_view_index)
                    self.ui.up_drew_qlabe.data_init = data
                    self.ui.up_index_spinbox.setValue(self.up_view_index)
            else:
                self.up_view_index -= 1
                if self.up_view_index < 0:
                    self.up_view_index = 0
                else:
                    img = self.up_view[:, :, self.up_view_index]
                    self.image = pg.ImageItem(img)
                    self.ui.up_drew_graphicsview.addItem(self.image)
                    data = self.getDrewdata(self.drew_up_data, self.up_view_index)
                    self.ui.up_drew_qlabe.data_init = data
                    self.ui.up_index_spinbox.setValue(self.up_view_index)
            return True
        elif (watched == self.ui.left_drew_graphicsview.viewport() and
              event.type() == QtCore.QEvent.Wheel):
            if self.ui.left_drew_qlabe.drew_flag:
                return True
            if event.angleDelta().y() > 0:
                self.left_view_index += 1
                if self.left_view_index == len(self.left_view):
                    self.left_view_index = len(self.left_view) - 1
                else:
                    img = self.left_view[:, :, self.left_view_index]
                    self.imageSagittal = pg.ImageItem(img)
                    self.ui.left_drew_graphicsview.addItem(self.imageSagittal)
                    data = self.getDrewdata(self.drew_left_data, self.left_view_index)
                    self.ui.left_drew_qlabe.data_init = data
                    self.ui.left_index_spinbox.setValue(self.left_view_index)
            else:
                self.left_view_index -= 1
                if self.left_view_index < 0:
                    self.left_view_index = 0
                else:
                    img = self.left_view[:, :, self.left_view_index]
                    self.imageSagittal = pg.ImageItem(img)
                    self.ui.left_drew_graphicsview.addItem(self.imageSagittal)
                    data = self.getDrewdata(self.drew_left_data, self.left_view_index)
                    self.ui.left_drew_qlabe.data_init = data
                    self.ui.left_index_spinbox.setValue(self.left_view_index)
            return True
        elif (watched == self.ui.front_drew_graphicsview.viewport() and
              event.type() == QtCore.QEvent.Wheel):
            if self.ui.front_drew_qlabe.drew_flag:
                return True
            if event.angleDelta().y() > 0:
                self.front_view_index += 1
                if self.front_view_index == len(self.front_view):
                    self.front_view_index = len(self.front_view) - 1
                else:
                    img = self.coronalView[:, :, self.front_view_index]
                    self.imageCoronal = pg.ImageItem(img)
                    self.ui.front_drew_graphicsview.addItem(self.imageCoronal)
                    data = self.getDrewdata(self.drew_front_data, self.front_view_index)
                    self.ui.front_drew_qlabe.data_init = data
                    self.ui.front_index_spinbox.setValue(self.front_view_index)
            else:
                self.front_view_index -= 1
                if self.front_view_index < 0:
                    self.front_view_index = 0
                else:
                    img = self.coronalView[:, :, self.front_view_index]
                    self.imageCoronal = pg.ImageItem(img)
                    self.ui.front_drew_graphicsview.addItem(self.imageCoronal)
                    data = self.getDrewdata(self.drew_front_data, self.front_view_index)
                    self.ui.front_drew_qlabe.data_init = data
                    self.ui.front_index_spinbox.setValue(self.front_view_index)
            return True
        return super().eventFilter(watched, event)

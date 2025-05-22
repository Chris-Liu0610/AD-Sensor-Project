import sys
import os
from PyQt6 import QtWidgets, QtCore
import pandas as pd
from widget_helper import label_setup, entry_setup, combobox_setup, date_setup, button_setup

class PersonalWindow(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('個人資料')
        self.setStyleSheet("background-color: rgb(248, 249, 250);")
        self.resize(800, 600)
        self.widgets = {}
        self.save_path_text = {}
        self.ui()

    def ui(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setSpacing(10)
        
        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_layout.setSpacing(10)
        
        #===== Create first gird layout =====#
        grid1_box = QtWidgets.QWidget()
        grid1_box.setStyleSheet("")
        grid1_box.setFixedHeight(40)
        self.grid1_layout = QtWidgets.QGridLayout(grid1_box)
        label_personal_data = label_setup("個人資料", None)
        label_personal_data.setStyleSheet("font-size: 24px; font-family: 微軟正黑體; font-weight: bold; border: 0px;")
        self.grid1_layout.addWidget(label_personal_data, 0, 0)
        self.grid1_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.widgets['label_personal_data'] = label_personal_data
        
        #===== Finish =====#

        #===== Create second gird layout =====#
        grid2_box = QtWidgets.QWidget()
        grid2_box.setStyleSheet("border: 0px;")
        grid2_box.setFixedHeight(40)
        self.grid2_layout = QtWidgets.QGridLayout(grid2_box)
        label_base_information = label_setup("基本資料", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid2_layout.addWidget(label_base_information, 0, 0, 1, 4)
        self.widgets['label_base_information'] = label_base_information
        #===== Finish =====#
        
        #===== Create third gird layout =====#
        grid3_box = QtWidgets.QWidget()
        grid3_box.setStyleSheet("border: 0px;")
        self.grid3_layout = QtWidgets.QGridLayout(grid3_box)
        self.grid3_layout.setSpacing(15)
        label_ID = label_setup("編號 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(label_ID, 0, 0)
        self.entry_ID = entry_setup("請輸入編號", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(self.entry_ID, 0, 1)
        self.widgets['entry_ID'] = self.entry_ID

        label_height = label_setup("身高 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(label_height, 0, 2)
        entry_height = entry_setup("請輸入身高", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(entry_height, 0, 3)
        self.widgets['entry_height'] = entry_height
        
        label_age = label_setup("年齡 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(label_age, 1, 0)
        entry_age = entry_setup("請輸入年齡", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(entry_age, 1, 1)
        self.widgets['entry_age'] = entry_age

        label_weight = label_setup("體重 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(label_weight, 1, 2)
        entry_weight = entry_setup("請輸入體重", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(entry_weight, 1, 3)
        self.widgets['entry_weight'] = entry_weight

        label_gender = label_setup("性別 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(label_gender, 2, 0)
        combobox_gender = combobox_setup(["請選擇性別","男", "女"], "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(combobox_gender, 2, 1)
        self.widgets['combobox_gender'] = combobox_gender

        label_birthday = label_setup("生日 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(label_birthday, 2, 2)
        calender_birthday = date_setup(self, "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(calender_birthday, 2, 3)
        self.widgets['calender_birthday'] = calender_birthday

        label_contact_number = label_setup("聯絡電話 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid3_layout.addWidget(label_contact_number, 3, 0)
        entry_contact_number = entry_setup("請輸入聯絡電話:09xxxxxxxx", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        entry_contact_number.setMaxLength(10)
        self.grid3_layout.addWidget(entry_contact_number, 3, 1, 1, 3)
        self.widgets['entry_contact_number'] = entry_contact_number
        #===== Finish =====#

        #===== Create combine second and third gird layout =====#
        combine_layout2_layout3_box = QtWidgets.QWidget()
        combine_layout2_layout3_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px; border : 2px solid black;")
        self.combine_layout2_layout3 = QtWidgets.QVBoxLayout(combine_layout2_layout3_box)
        self.combine_layout2_layout3.addWidget(grid2_box)
        self.combine_layout2_layout3.addWidget(grid3_box)
        #==== Finish ====#


        #===== Create fourth gird layout =====#
        grid4_box = QtWidgets.QWidget()
        grid4_box.setStyleSheet("border: 0px;")
        self.grid4_layout = QtWidgets.QGridLayout(grid4_box)
        self.grid4_layout.setSpacing(15)

        label_photography_information = label_setup("拍攝資料", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid4_layout.addWidget(label_photography_information, 0, 0, 1, 4)
        self.widgets['label_photography_information'] = label_photography_information
        #==== Finish ====#

        #===== Create fifth gird layout =====#
        grid5_box = QtWidgets.QWidget()
        grid5_box.setStyleSheet("border: 0px;")
        self.grid5_layout = QtWidgets.QGridLayout(grid5_box)
        self.grid5_layout.setSpacing(15)

        label_photography_year = label_setup("拍攝年份 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        label_photography_year.setFixedWidth(80)
        self.grid5_layout.addWidget(label_photography_year, 0, 0)
        calender_photography_year = date_setup(self, "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(calender_photography_year, 0, 1, 1, 3)
        self.widgets['calender_photography_year'] = calender_photography_year

        label_photography_site = label_setup("拍攝地點 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        label_photography_site.setFixedWidth(80)
        self.grid5_layout.addWidget(label_photography_site, 1, 0)
        entry_photography_site = entry_setup("請輸入拍攝地點", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(entry_photography_site, 1, 1, 1, 3)
        self.widgets['entry_photography_site'] = entry_photography_site

        label_photography_reason = label_setup("拍攝原因 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        label_photography_reason.setFixedWidth(80)
        self.grid5_layout.addWidget(label_photography_reason, 2, 0)
        combobox_photography_reason = combobox_setup(["請選擇拍攝原因", "醫療檢查", "健康檢查", "其他"], "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid5_layout.addWidget(combobox_photography_reason, 2, 1, 1, 3)
        self.widgets['combobox_photography_reason'] = combobox_photography_reason
        #===== Finish =====#

        #===== Create combine fourth and fifth gird layout =====#
        combine_layout4_layout5_box = QtWidgets.QWidget()
        combine_layout4_layout5_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px; border : 2px solid black;")
        self.combine_layout4_layout5 = QtWidgets.QVBoxLayout(combine_layout4_layout5_box)
        self.combine_layout4_layout5.addWidget(grid4_box)
        self.combine_layout4_layout5.addWidget(grid5_box)
        #==== Finish ====#

        #===== Create sixth gird layout =====#
        grid6_box = QtWidgets.QWidget()
        grid6_box.setStyleSheet("border: 0px;")
        grid6_box.setFixedHeight(40)
        self.grid6_layout = QtWidgets.QGridLayout(grid6_box)
        label_medical_information = label_setup("醫療資料", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid6_layout.addWidget(label_medical_information, 0, 0, 1, 4)
        self.widgets['label_medical_information'] = label_medical_information
        #==== Finish ====#

        #===== Create seventh gird layout =====#
        grid7_box = QtWidgets.QWidget()
        grid7_box.setStyleSheet("border: 0px;")
        self.grid7_layout = QtWidgets.QGridLayout(grid7_box)
        self.grid7_layout.setSpacing(15)

        label_medical_history = label_setup("病史 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        label_medical_history.setFixedWidth(80)
        self.grid7_layout.addWidget(label_medical_history, 0, 0)
        entry_medical_history = entry_setup("請輸入病史", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid7_layout.addWidget(entry_medical_history, 0, 1, 1, 3)
        self.widgets['entry_medical_history'] = entry_medical_history

        label_allergic_medications = label_setup("過敏藥物 : :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        label_allergic_medications.setFixedWidth(80)
        self.grid7_layout.addWidget(label_allergic_medications, 1, 0)
        entry_medication_allergic_medications = entry_setup("請輸入過敏藥物", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid7_layout.addWidget(entry_medication_allergic_medications, 1, 1, 1, 3)
        self.widgets['entry_medication_allergic_medications'] = entry_medication_allergic_medications

        label_mideication_taken = label_setup("服用藥物 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        label_mideication_taken.setFixedWidth(80)
        self.grid7_layout.addWidget(label_mideication_taken, 2, 0)
        entry_medication_taken = entry_setup("請輸入服用藥物", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid7_layout.addWidget(entry_medication_taken, 2, 1, 1, 3)
        self.widgets['entry_medication_taken'] = entry_medication_taken

        label_caution = label_setup("注意事項 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid7_layout.addWidget(label_caution, 3, 0)
        entry_caution = entry_setup("請輸入注意事項", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid7_layout.addWidget(entry_caution, 3, 1, 1, 3)
        self.widgets['entry_caution'] = entry_caution
        #===== Finish =====#

        #===== Create combine sixth and seventh gird layout =====#
        combine_layout6_layout7_box = QtWidgets.QWidget()
        combine_layout6_layout7_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px; border : 2px solid black;")
        self.combine_layout6_layout7 = QtWidgets.QVBoxLayout(combine_layout6_layout7_box)
        self.combine_layout6_layout7.addWidget(grid6_box)
        self.combine_layout6_layout7.addWidget(grid7_box)
        #==== Finish ====#
        
        #===== Create combine eighth gird layout =====#
        grid8_layout_box = QtWidgets.QWidget()
        grid8_layout_box.setStyleSheet("border: 0px;")
        grid8_layout_box.setFixedHeight(40)
        self.grid8_layout = QtWidgets.QGridLayout(grid8_layout_box)
        label_save_path = label_setup("儲存路徑 :", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;")
        self.grid8_layout.addWidget(label_save_path, 0, 0)
        #==== Finish =====#

        #===== Create ninth gird layout =====#
        grid9_layout_box = QtWidgets.QWidget()
        grid9_layout_box.setStyleSheet("border: 0px;")
        self.grid9_layout = QtWidgets.QGridLayout(grid9_layout_box)
        entry_save_path = entry_setup("請選擇儲存資料夾", "font-size: 16px; font-family: 微軟正黑體; font-weight: bold;") 
        entry_save_path.setReadOnly(True)
        self.grid9_layout.addWidget(entry_save_path, 1, 0, 1, 4)
        self.save_path_text['entry_save_path'] = entry_save_path
        #==== Finish =====#

        #===== Create combine eighth and ninth gird layout =====#
        combine_layout8_layout9_box = QtWidgets.QWidget()
        combine_layout8_layout9_box.setStyleSheet("background-color: rgb(214, 234, 248); border-radius: 20px; border : 2px solid black;")
        self.combine_layout8_layout9 = QtWidgets.QVBoxLayout(combine_layout8_layout9_box)
        self.combine_layout8_layout9.addWidget(grid8_layout_box)
        self.combine_layout8_layout9.addWidget(grid9_layout_box)
        #==== Finish ====#

        #===== Create tenth grid layout =====#
        grid10_box = QtWidgets.QWidget()
        # grid5_box.setFixedHeight(60)
        self.grid10_layout = QtWidgets.QGridLayout(grid10_box)
        self.grid10_layout.setSpacing(15)

        button_save_folder = button_setup("選擇儲存資料夾", self.open_save_folder)
        self.grid10_layout.addWidget(button_save_folder, 0, 0)


        button_clear = button_setup("清除", self.clear_data)
        self.grid10_layout.addWidget(button_clear, 0, 1)
        self.widgets['button_clear'] = button_clear

        button_save = button_setup("儲存", self.save_data)
        self.grid10_layout.addWidget(button_save, 0, 2)
        self.widgets['button_save'] = button_save

        button_next = button_setup("下一步", lambda: print("下一步按鈕被點擊"))
        self.grid10_layout.addWidget(button_next, 0, 3)
        self.widgets['button_next'] = button_next
        #==== Finish =====#    

        #===== Create scroll area =====#
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)
        scroll_area.setStyleSheet("border: 0px;")
        scroll_area.setFixedHeight(650)
        #===== Finish =====#

        #==== Finally, add the grid layout to the main layout ====#
        self.main_layout.addWidget(grid1_box)
        # content_layout.addWidget(grid1_box)
        self.main_layout.addWidget(combine_layout2_layout3_box)
        content_layout.addWidget(combine_layout2_layout3_box)
        self.main_layout.addWidget(combine_layout4_layout5_box)
        content_layout.addWidget(combine_layout4_layout5_box)
        self.main_layout.addWidget(combine_layout6_layout7_box)
        content_layout.addWidget(combine_layout6_layout7_box)
        self.main_layout.addWidget(combine_layout8_layout9_box)
        content_layout.addWidget(combine_layout8_layout9_box)
        self.main_layout.addWidget(grid10_box)
        content_layout.addWidget(grid10_box)
        self.main_layout.addWidget(scroll_area)
        #===== Finish =====#
    
    def connect_next_second_button(self, function):
        self.widgets['button_next'].clicked.connect(function)


    def get_data(self):
        data = {}
        for key, widget in self.widgets.items():
            if isinstance(widget, QtWidgets.QLineEdit):
                data[key] = widget.text()
            elif isinstance(widget, QtWidgets.QComboBox):
                data[key] = widget.currentText()
            elif isinstance(widget, QtWidgets.QDateEdit):
                data[key] = widget.date().toString('yyyy-MM-dd')
            else:
                continue
        return data
    
    def open_save_folder(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory()
        if folder_path:
            print(f"選擇的儲存資料夾: {folder_path}")
            self.save_path_text['save_path'] = folder_path
            self.save_path_text['entry_save_path'].setText(folder_path)
        


    def clear_data(self):
        for key, widget in self.widgets.items():
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.clear()
            elif isinstance(widget, QtWidgets.QComboBox):
                widget.setCurrentIndex(0)
            elif isinstance(widget, QtWidgets.QDateEdit):
                widget.setDate(QtCore.QDate.currentDate())
            else:
                pass

    def save_data(self):
        data = self.get_data()
        df = pd.DataFrame([data])

        if 'save_path' not in self.save_path_text:
            print("請選擇儲存資料夾")
            return
        
        save_path = self.save_path_text['save_path']
        print(save_path)
        file_exists = os.path.isfile(save_path + '/AD_patient_data.csv')

        if file_exists is True:
            df.to_csv(save_path + '/AD_patient_data.csv', mode='a', header=False, index=False, encoding='utf-8-sig')
            print(f'檔案接續儲存在:{save_path}AD_patient_data.csv')
            
        else:
            df.to_csv(save_path + '/AD_patient_data.csv', mode='w', header=True, index=False, encoding='utf-8-sig')
            print(f'檔案第一次儲存在:{save_path}AD_patient_data.csv')
            
    #===== Finish =====#



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    first_window = PersonalWindow()
    first_window.show()
    sys.exit(app.exec())
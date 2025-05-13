from PyQt6 import QtWidgets, QtCore
import sys
import math


#===== 設定文字樣式 =====#
def font_setup(font, font_size, font_weight, text_color_RGB):
    r,g,b = text_color_RGB
    font_Set = f'font-family: "{font}"; font-size: {font_size}px; font-weight:{font_weight}; color:rgb({r}, {g}, {b});'
    return font_Set


#===== 建立標籤 =====#
def label_setup(text, Form, font_Set):
    Label = QtWidgets.QLabel(text, Form)
    Label.setStyleSheet(font_Set)
    Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)  # 設定文字置中
    return Label



#===== 輸入框 =====#
def entry_setup(Form, prompt_text,  font_Set):
    Entry = QtWidgets.QLineEdit(Form)
    Entry.setPlaceholderText(prompt_text)  # 設定提示文字
    Entry.setStyleSheet(f'{font_Set}; background-color: rgb(255, 255, 255); border: 1px solid black; border-radius: 5px')  # 設定字型大小
    Entry.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)  # 設定文字置中
    return Entry

def date_entry_setup(Form, prompt_text,  font_Set):
    Entry = QtWidgets.QDateEdit(Form)
    Entry.setDisplayFormat("yyyy-MM-dd")  # 設定日期格式
    Entry.setCalendarPopup(True)  # 設定彈出日曆
    Entry.setDate(QtCore.QDate.currentDate().addYears(0))
    Entry.setKeyboardTracking(True)
    Entry.setStyleSheet(f'{font_Set}; background-color: rgb(255, 255, 255); border: 1px solid black; border-radius: 5px')  # 設定字型大小
    Entry.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)  # 設定文字置中
    return Entry

def combobox_setup(Form, font_set):
    comboBox = QtWidgets.QComboBox(Form)
    comboBox.setStyleSheet(f'{font_set}; background-color: rgb(255, 255, 255); border: 1px solid black; border-radius: 5px')  # 設定字型大小
    # comboBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)  # 設定文字置中
    comboBox.addItems(['請選擇性別', '男', '女', '其他'])
    comboBox.setCurrentIndex(0)  # 設定預設選項
    return comboBox

#===== 建立放QGrid的容器和grid_layout =====#
def create_grid_container(Form):
    grid_container = QtWidgets.QWidget(Form)
    width = Form.width()-2 # 要比Form window size小
    height = Form.height()-2
    grid_container.resize(width, height)
    grid_container.move(1, 1)
    grid_layout = QtWidgets.QGridLayout(grid_container)
    grid_container.setStyleSheet("border: 1px solid red;") # 設定邊框顏色，用來看grid位置

    return grid_container, grid_layout

# ===== 設定QGridLayout =====#
def grid_setup(grid_layout, widget, row, column):
    grid_layout.addWidget(widget, row, column)  # widget, row, column, rowSpan, columnSpan
    
    column_ratio = [1,2,1,2]  # Label Entry列的比例
    for i, ratio in enumerate(column_ratio):
        grid_layout.setColumnStretch(i, ratio)  # 設定列的比例，維持4 column，比例都不會改變
    
    for j in range(8):
        grid_layout.setRowStretch(j, 1)  # 所有行的比例相同
    
    grid_layout.setContentsMargins(50, 0, 50, 0)  # 設定邊界(left, top, right, bottom)
    grid_layout.setHorizontalSpacing(10)  # 設定水平間距
    grid_layout.setVerticalSpacing(20)  # 設定垂直間距


def main():
    # 視窗程式開始
    app = QtWidgets.QApplication(sys.argv) 

    # 建立基底元件
    Form = QtWidgets.QWidget()               
    Form.setWindowTitle("個人資料")  # 設定視窗標題
    Form.setFixedSize(800, 450)
    Form.setStyleSheet("background-color: rgb(255, 255, 255);")  # 設定背景顏色

    font_Set = font_setup("微軟正黑體", 20, 'bold', [0, 0, 0])

    text = ['編號 :', '性別 :', '拍攝日期 :', '年齡 :', '生日 :', '病史 :', '聯絡電話 :', '注意事項 :']

    grid_container, grid_layout = create_grid_container(Form)


    Title = label_setup('個人資料', grid_container , font_Set)
    grid_layout.addWidget(Title, 0, 0, 1, 4)  # 設定標題的grid位置
    grid_layout.setAlignment(Title, QtCore.Qt.AlignmentFlag.AlignCenter)  # 設定標題置中
    

    Label1 = label_setup(text[0], grid_container, font_Set)
    grid_setup(grid_layout, Label1, 1, 0)  # 設定Label1的grid位置
    Entry1 = entry_setup(grid_container, '請輸入編號', font_Set)
    grid_setup(grid_layout, Entry1, 1, 1)  # 設定Entry1的grid位置

    Label2 = label_setup(text[1], grid_container, font_Set)
    grid_setup(grid_layout, Label2, 2, 0)  # 設定Label2的grid位置
    Combobox2 = combobox_setup(grid_container, font_Set)
    grid_setup(grid_layout, Combobox2, 2, 1)  # 設定Entry2的grid位置
    
    Label3 = label_setup(text[2], grid_container, font_Set)
    grid_setup(grid_layout, Label3, 3, 0)  # 設定Label3的grid位置
    # Entry3 = entry_setup(grid_container, '請輸入拍攝日期', font_Set)
    Entry3 = date_entry_setup(grid_container, '請輸入拍攝日期', font_Set)
    grid_setup(grid_layout, Entry3, 3, 1)  # 設定Entry3的grid位置

    Label4 = label_setup(text[3], grid_container, font_Set)
    grid_setup(grid_layout, Label4, 4, 0)  # 設定Label4的grid位置
    Entry4 = entry_setup(grid_container, '請輸入年齡', font_Set)
    grid_setup(grid_layout, Entry4, 4, 1)  # 設定Entry4的grid位置

    Label5 = label_setup(text[4], grid_container, font_Set)
    grid_setup(grid_layout, Label5, 1, 2)  # 設定Label5的grid位置
    Entry5 = entry_setup(grid_container, '請輸入生日', font_Set)
    grid_setup(grid_layout, Entry5, 1, 3)  # 設定Entry5的grid位置

    Label6 = label_setup(text[5], grid_container, font_Set)
    grid_setup(grid_layout, Label6, 2, 2)  # 設定Label6的grid位置
    Entry6 = entry_setup(grid_container, '請輸入病史', font_Set)
    grid_setup(grid_layout, Entry6, 2, 3)  # 設定Entry6的grid位置

    Label7 = label_setup(text[6], grid_container, font_Set)
    grid_setup(grid_layout, Label7, 3, 2)  # 設定Label7的grid位置
    Entry7 = entry_setup(grid_container, '請輸入聯絡電話', font_Set)
    grid_setup(grid_layout, Entry7, 3, 3)  # 設定Entry7的grid位置

    Label8 = label_setup(text[7], grid_container, font_Set)
    grid_setup(grid_layout, Label8, 4, 2)  # 設定Label8的grid位置
    Entry8 = entry_setup(grid_container, '請輸入注意事項', font_Set)
    grid_setup(grid_layout, Entry8, 4, 3)  # 設定Entry8的grid位置



    Form.show()                             # 顯示基底元件
    sys.exit(app.exec())

    Form.show()                             # 顯示基底元件
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
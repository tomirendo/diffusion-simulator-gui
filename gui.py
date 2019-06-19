
###!/usr/local/bin/python3.5
import sys, os
import json
import threading
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTableView, QTableWidget,QTableWidgetItem,QProgressBar,
    QTextEdit, QCheckBox, QGridLayout, QApplication, QFileDialog, QPushButton, QMessageBox, QErrorMessage)
# from PyQt5.QtGui import QAbstractTableModel
from PyQt5.QtCore import Qt, pyqtSlot, QAbstractTableModel, QObject
from PyQt5 import QtCore
import numpy as np
from simulation import Simulation, NUMBER_OF_FRAMES_KEY, MOLECULES_KEY
from multispecies_simulation import MultiSpeciesSimulation
from last_save import LastSave

MOLECULES_DICTIONARY_KEY = 'molecules'
SECONDS_IN_MILISECOND = 1e-3

COLUMN_CHAR_WIDTH = 7

WINDOW_WIDTH = 770
WINDOW_HEIGHT = 600

ORIGINAL_POSITION_X = 100
ORIGINAL_POSITION_Y = 100

SUBFRAMES_RATIO = 85

NUMBER_OF_ANIMATION_STEPS = 2
STATUS_LABEL_INITAL_VALUE = 'Click `Create Simulation` to begin'



treads = []
default_values = {   
    "total_time_in_seconds": 10.0, 
    "exposure_time_in_ms": 40.0, 
    "number_of_subframes_per_frame" : 100,


    "pixel_length_in_um": 0.117, 
    "z_direction_depth_in_um": 0.5, 

    "screen_size_in_pixels_x": 400, 
    "screen_size_in_pixels_y": 400,

    "psf_sigma_in_um_x_axis" : 0.04,
    "psf_sigma_in_um_y_axis" : 0.04,
    "background_noise_amplitude" : 30
}

molecule_default_values = {
    "number_of_molecules": 5000, 
    "diffusion_coefficient_in_um^2_over_seconds": 0.5,
    "intensity" : 100,
}

def calculated_subframes(gui_object, setup_dictionary):
    pixel_length = setup_dictionary['pixel_length_in_um']
    max_diff_coef = gui_object.molecules_table_model.get_maximal_diffusion_coefficinet(gui_object)
    exposure_time = setup_dictionary['exposure_time_in_ms'] * SECONDS_IN_MILISECOND
    return int(np.sqrt(max_diff_coef*exposure_time)/pixel_length * SUBFRAMES_RATIO) + 1


calculated_values = {
    'number_of_subframes_per_frame' : calculated_subframes
}



last_saved_dir = LastSave()
class MoleculeTableModel():
    def __init__(self, parent = None, *args):
        self.molecule_data = {k:[v] for k,v in molecule_default_values.items()}
        self.keys = sorted(list(molecule_default_values))
        self.types = {k:type(v) for k,v in molecule_default_values.items()}
        self.table_widget = QTableWidget()
        self.init_table()

    def init_table(self):
        self.table_widget.setRowCount(self.row_count())
        self.table_widget.setColumnCount(self.column_count())
        for i, key in enumerate(self.keys):
            for j, value in enumerate(self.molecule_data[key]):
                self.table_widget.setItem(j, i, QTableWidgetItem(str(value)))
            self.table_widget.setColumnWidth(i, len(key) * COLUMN_CHAR_WIDTH)

        self.table_widget.setHorizontalHeaderLabels([k.replace('_',' ').title() 
                                                for k in self.keys])

    def data_to_array(self, data):
        return list([data[k] for k in self.keys])

    def array_to_data(self, array):
        return {k:list(v) for k,v in zip(self.keys, array)}

    def table_to_array(self):
        res = []
        for i, key in enumerate(self.keys):
            res.append([self.table_widget.item(j, i).text() for j in range(self.row_count())])
        return res


    def row_count(self):
        return len(self.molecule_data[self.keys[0]])

    def column_count(self):
        return len(self.molecule_data)

    def update_data(self):
        self.molecule_data = self.array_to_data(self.table_to_array())

    def add_row(self):
        self.update_data()
        for key in self.keys:
            self.molecule_data[key].append(molecule_default_values[key])
        self.init_table()

    def get_molecules(self, gui_object):
        """
            Returns a list of dictionaries for each molecule
        """
        res = []
        for idx in range(self.row_count()): 
            try: 
                molecule_dictionary = {}
                for key in self.keys:
                    molecule_dictionary[key] = self.types[key](self.molecule_data[key][idx])
                res.append(molecule_dictionary)
            except Exception as e:
                gui_object.show_error("Problem parsing {}, \n {}".format(key, str(e)))
                return
        return res

    def get_maximal_diffusion_coefficinet(self,gui_object):
        self.update_data()
        mols = self.get_molecules(gui_object)
        return max([m['diffusion_coefficient_in_um^2_over_seconds'] for m in mols])

    # def headerData(self, col, orientation, role):
    #     if orientation == Qt.Horizontal:
    #         return (self.keys[col].replace('_',' ').title()) #     return None




types_dictionary = {k: type(v) for k,v in default_values.items()}

class GUI(QWidget):
    
    def __init__(self):
        super().__init__()

        self.error_message = QErrorMessage(self)
        self.error_message.setWindowModality(Qt.WindowModal)

        self.gui_dictionary = {key:None for key in default_values}
        self.checkboxes = {}
        self.initUI()
        self.create_setup_dictionary()
        
    def initUI(self):

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(QLabel("Parameter"), 1,0)
        self.grid.addWidget(QLabel("Value"), 1,1)
        self.grid.addWidget(QLabel("Auto"), 1,2)
        ofset = 2
        for idx,(key, value) in enumerate(sorted(default_values.items())):
            text_label = key.replace('_',' ').title()
            value_str = str(value)
            label = QLabel(text_label)
            text_box = QLineEdit(value_str)
            text_box.setAlignment(Qt.AlignCenter)
            text_box.setEnabled(key not in calculated_values)
            self.grid.addWidget(label, idx+ofset, 0)
            self.grid.addWidget(text_box, idx+ofset, 1)

            if key in calculated_values:
                checkbox = QCheckBox()
                checkbox.setChecked(True)
                def toggled(value, key = key):
                    self.gui_dictionary[key].setEnabled(not value)
                    self.create_setup_dictionary()
                checkbox.toggled.connect(toggled)

                self.grid.addWidget(checkbox, idx+ofset, 2)
                self.checkboxes[key] = checkbox

            self.gui_dictionary[key] = text_box

        self.create_video_button = QPushButton('Create Simulation')
        self.add_molecule_type = QPushButton('Add Molecule')

        self.molecules_table_model = MoleculeTableModel()
        self.molecules_table = self.molecules_table_model.table_widget

        self.create_video_button.clicked.connect(self.run_button_clicked)
        self.add_molecule_type.clicked.connect(self.add_molecule)

        self.grid.addWidget(self.add_molecule_type, len(default_values) + 1, 0, 2, 1)
        self.grid.addWidget(self.molecules_table, len(default_values) + 1, 1, 2, 1)
        self.grid.addWidget(self.create_video_button, len(default_values)+3, 0, 1, 2)


        self.progress_bar = QProgressBar()
        self.status_label = QLabel(STATUS_LABEL_INITAL_VALUE)
        self.grid.addWidget(self.progress_bar, len(default_values)+4,1,1,1)
        self.grid.addWidget(self.status_label, len(default_values)+4,0,1,1)

        self.setLayout(self.grid) 
        self.setGeometry(ORIGINAL_POSITION_X, ORIGINAL_POSITION_Y, 
                          WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowTitle('Molecule Magic Mixer')    
        self.show()

    @pyqtSlot()
    def add_molecule(self):
        self.molecules_table_model.add_row()

    @pyqtSlot()
    def run_button_clicked(self):
        self.molecules_table_model.update_data()

        molecules_dictionaries = self.molecules_table_model.get_molecules(self)
        if molecules_dictionaries is None:
            """
                An Error Occurred
            """
            return

        setup_dictionary = self.create_setup_dictionary()
        if setup_dictionary is None:
            return


        options = QFileDialog.Options()
        # options.setDirectory(last_saved_dir.get_dir())
        filename, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()",last_saved_dir.get_dir(),
                                                  "Tiff Files (*.tif)", 
                                                  options=options)



        if not filename:
            return 
            
        last_saved_dir.update_dir(os.path.dirname(filename))
        self.init_progress_bar(len(molecules_dictionaries))
        self.set_enable_status(False)

        def worker():
            self.set_status_label("Running Simulations")
            simulations = []
            for index, molecule_dict in enumerate(molecules_dictionaries):
                simulation_dictionary = dict(setup_dictionary)
                simulation_dictionary.update(molecule_dict)
                simulation = Simulation(simulation_dictionary)
                simulation.run()
                simulations.append(simulation)
                self.progress_bar.setValue(index)

            multispecies_simulation = MultiSpeciesSimulation(*simulations)

            self.progress_bar.setValue(self.progress_bar.value() + 1)
            self.set_status_label("Creating Frames")
            multispecies_simulation.create_frames()

            self.progress_bar.setValue(self.progress_bar.value() + 1)
            self.set_status_label("Saving to file")
            multispecies_simulation.save_frames_to_file(filename)
            self.save_setup(setup_dictionary, molecules_dictionaries, simulations, filename)

            # self.progress_bar.setValue(self.progress_bar.value() + 1)
            self.finish_progress_bar()
            self.set_status_label("Done!")
            self.set_enable_status(True)

        t = threading.Thread(target = worker)
        treads.append(t)
        t.start()


    def show_error(self, message):
        self.error_message.showMessage(message)
        self.set_enable_status(True)

    def set_enable_status(self, status):
        # for value in 
        for key, widget in self.gui_dictionary.items():
            if self.is_calculated_key(key):
                pass
            else:
                widget.setEnabled(status)
        
        for checkbox in self.checkboxes.values():
            checkbox.setEnabled(status)

        self.molecules_table_model.table_widget.setEnabled(status)
        self.create_video_button.setEnabled(status)
        self.add_molecule_type.setEnabled(status)

    def init_progress_bar(self, number_of_molecules):
        self.progress_bar.setValue(0)
        self.progress_bar.setMinimum(0) 
        self.progress_bar.setMaximum(number_of_molecules + NUMBER_OF_ANIMATION_STEPS)

    def finish_progress_bar(self):
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(1)
        self.progress_bar.setValue(1)


    def set_status_label(self, text):
        self.status_label.setText(text)

    def is_calculated_key(self, key):
        if key in calculated_values:
            if self.checkboxes[key].isChecked():
                return True
        return False


    def create_setup_dictionary(self):
        setup_dictionary = {}
        for key, text_box in self.gui_dictionary.items():
            try: 
                setup_dictionary[key] = types_dictionary[key](text_box.text())

            except Exception as e:
                self.show_error("Problem parsing {}, \n {}".format(key, str(e)))
                return

        for key, function in calculated_values.items():
            if self.checkboxes[key].isChecked():
                value = function(self, setup_dictionary)
                setup_dictionary[key] = value
                self.gui_dictionary[key].setText(str(value))
                
        return setup_dictionary

    def create_simulation_dictionary(self, setup_dictionary, molecules_dictionaries, simulations):
        d = dict(setup_dictionary)
        molecules_dictionaries = list([dict(d) for d in molecules_dictionaries])
        for molecule_dict, simulation in zip(molecules_dictionaries, simulations):
            molecule_dict[MOLECULES_KEY] = simulation.to_dict()[MOLECULES_KEY]
        d[MOLECULES_DICTIONARY_KEY] = molecules_dictionaries
        return d

    def save_setup(self, setup_dictionary, molecules_dictionaries, simulations, filename):
        with open(filename + ".json", "w") as f:
            f.write(json.dumps(self.create_simulation_dictionary(setup_dictionary, molecules_dictionaries, simulations)))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())

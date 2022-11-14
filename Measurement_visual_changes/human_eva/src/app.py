import logging
import os
import pandas as pd

from math import log10
from glob import glob
from collections import Counter
from collections import OrderedDict

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,QDateTime
from PyQt5.QtCore import pyqtSlot, QTimer, Qt

from .view import BinaryClassifierViewer


LOGGER = logging.getLogger(__name__)


class BinaryClassifierApp(BinaryClassifierViewer):
    def __init__(self, imgdir, shop_names, outfile, history=None):
        super().__init__()
        self.outfile = outfile
        self.history_file = history
        self.history_label = {}
        self.timeLabel = []
        self.shopnames = shop_names
        #self.shop_name = name
        raw_images = glob(os.path.join(imgdir, "*.jpg"))
        inpaint_images = glob(os.path.join(imgdir, "*.png"))
        self.image_paths = raw_images + inpaint_images
        self.image_index = 0
        self.image_label = {img: None for img in self.image_paths}
        self.timer = QTimer(self)
        self.step = 0.0
        self.timer.start(100)
        #self.lable = QLabel("显示当前时间")
        self.timer.timeout.connect(self.update_func)
        #layout.addWidget(self.lable, 0, 0, 1, 2)
        #self.timer.timeout.connect(self.update_func)
        self.btn_false.clicked.connect(self._on_click_left)
        self.btn_true.clicked.connect(self._on_click_right)
        #self.label_confirm.clicked.connect(self.export)
        self._goto_next_unlabeled_image()
        #self._load_history()
        #self._render_image(self.image_paths[0])


    def update_func(self):
        self.step += 1
        self.label_confirm.setText("Timing: "+str(self.step/10)+' s')

    def _load_history(self):
        if self.history_file and os.path.isfile(self.history_file):
            LOGGER.info('Load history file - {}'.format(self.history_file))
            df = pd.read_csv(self.history_file)
            df = df.fillna('')
            history_label = df.to_dict('split')['data']
            history_label = {img: int(label) for img, label in history_label if not isinstance(label, str)}
            self.history_label = history_label
            self.image_label.update(history_label)
            self._goto_next_unlabeled_image()

    def _render_image(self,image_name):
        assert 0 <= self.image_index < len(self.image_paths)
        image = QPixmap(self.image_paths[self.image_index])
        #print(self.image_paths[self.image_index])
        #print(image.width())
        #print(image.height())
        resize_width = min(image.width(), self.screen.width()*0.2)
        resize_height = min(image.height(), self.screen.height()*0.2)
        image = image.scaled(resize_width*3, resize_height*3, Qt.KeepAspectRatio)
        self.label_head.setPixmap(image)
        self.label_head.resize(resize_width, resize_height)
        self._render_status(image_name)
        self.show()

    def _render_status(self,image_name):
        image_name = os.path.basename(self.image_paths[self.image_index])
        counter = Counter(self.image_label.values())
        labeled = self.image_label[self.image_paths[self.image_index]]
        pad_zero = int(log10(len(self.image_paths))) + 1
        #self.label_status.setText('Can you find'+ self.shop_name +' ?')
        shop_object = self.shopnames[image_name]
        self.label_status.setText('Can you find' + shop_object+ ' ?')
        '''
        if labeled is not None:
            self.label_status.setText('({}/{}) {} => Labeled as {}'.format(
                str(self.image_index+1).zfill(pad_zero), len(self.image_paths), image_name, labeled
            ))
        else:
            self.label_status.setText('({}/{}) {}'.format(
                str(self.image_index+1).zfill(pad_zero), len(self.image_paths), image_name
            ))
        '''
        #self.btn_false.setText('Not Found ({})'.format(counter[0]))
        #self.btn_true.setText('Found ({}) >'.format(counter[1]))
        self.btn_false.setText('Not Found')
        self.btn_true.setText('Found >')
    def _undo_image(self):
        if self.image_index == 0:
            QMessageBox.warning(self, 'Warning', 'Reach the top of images')
        else:
            self.image_index = max(self.image_index - 1, 0)
            self._render_image()

    def _goto_prev_unlabeled_image(self):
        if self.image_index == 0:
            QMessageBox.warning(self, 'Warning', 'Reach the top of images')
        else:
            prev_image_index = self.image_index
            for idx in range(self.image_index-1, 0, -1):
                # label could be the value in [0, 1, None]
                if self.image_label[self.image_paths[idx]] is None:
                    prev_image_index = idx
                    break
            if prev_image_index == self.image_index:
                QMessageBox.information(self, 'Information', 'No more prev unlabeled image')
            else:
                self.image_index = prev_image_index
                self._render_image()

    def _goto_next_unlabeled_image(self):
        if self.image_index == len(self.image_paths) -1:
            QMessageBox.warning(self, 'Warning', 'Reach the end of images')
        else:
            next_image_index = self.image_index
            for idx in range(self.image_index+1, len(self.image_paths)):
                # label could be the value in [0, 1, None]
                if self.image_label[self.image_paths[idx]] is None:
                    next_image_index = idx
                    break
            if next_image_index == self.image_index:
                QMessageBox.information(self, 'Information', 'No more next unlabeled image')
            else:

                self._render_image(self.image_paths[idx-1])
                #self.image_index = next_image_index

    @pyqtSlot()
    def _on_click_left(self):
        if self.image_index == len(self.image_paths)-1:
            import csv
            self.timeLabel.append([self.image_paths[self.image_index], self.label_confirm.text()])
            with open("csvfile.csv", "a", newline='', encoding='utf-8') as f:
                for line in self.timeLabel:
                    writer = csv.writer(f, delimiter=',')
                    writer.writerow(line)
            QMessageBox.warning(self, 'Warning', 'Reach the end of images')
        else:
            self.image_label[self.image_paths[self.image_index]] = 1
            self.image_index = min(self.image_index+1, len(self.image_paths) - 1)
            #image_name = self.image_paths[self.image_index - 1]
            self._render_image(self.image_paths[self.image_index])
            self.timeLabel.append([self.image_paths[self.image_index-1],self.label_confirm.text()])
            self.timer.stop()
            self.step = 0.0
            self.timer.start(100)

    @pyqtSlot()
    def _on_click_right(self):
        if self.image_index == len(self.image_paths)-1:
            self.timeLabel.append([self.image_paths[self.image_index], self.label_confirm.text()])

            import csv
            with open("csvfile.csv", "a", newline='', encoding='utf-8') as f:
                for line in self.timeLabel:
                    writer = csv.writer(f, delimiter=',')
                    writer.writerow(line)
            QMessageBox.warning(self, 'Warning', 'Reach the end of images')
        else:
            self.image_label[self.image_paths[self.image_index]] = 1
            self.image_index = min(self.image_index+1, len(self.image_paths) - 1)
            image_name = self.image_paths[self.image_index]

            self.timeLabel.append([self.image_paths[self.image_index-1],self.label_confirm.text()])
            self._render_image(image_name)
            self.timer.stop()
            self.step = 0.0
            self.timer.start(100)

    @pyqtSlot()
    def export(self):
        orderdict = OrderedDict(sorted(self.image_label.items(), key=lambda x: x[0]))
        df = pd.DataFrame(data={'image': list(orderdict.keys()), 'label': list(orderdict.values())}, dtype='uint8')
        df.to_csv(self.outfile, index=False)
        LOGGER.info('Export label result {}'.format(self.outfile))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left or event.key() == Qt.Key_A:
            self.btn_false.click()
        elif event.key() == Qt.Key_Right or event.key() == Qt.Key_D:
            self.btn_true.click()
        elif event.key() == Qt.Key_U:
            self._undo_image()
        elif event.key() == Qt.Key_PageUp:
            self._goto_prev_unlabeled_image()
        elif event.key() == Qt.Key_PageDown:
            self._goto_next_unlabeled_image()
        else:
            LOGGER.debug('You Clicked {} but nothing happened...'.format(event.key()))

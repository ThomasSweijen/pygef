import pygef.gef
import pygef.manual_soil_classification.list_default_soil_types as default
import logging
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import pandas as pd
import numpy


class ManualSoilInterpretation:
    def __init__(self, classification=None, df=None):
        if isinstance(classification, ManualSoilClassification) is False:
            logging.error(f'soil classification is not of class ManualSoilClassification')
            return
        self.s = classification
        self.df = df
        self.lith = []
        self.classify()
        self.df = pd.concat([self.df.copy(), pd.Series(self.lith).rename("lithology_manual")], axis=1, sort=False)

    def classify(self):
        for i in self.df.index:
            if self.df["qc"][i] > 998 or self.df["friction_number"][i] > 998 or self.df["fs"][i] > 9.98:
                self.lith.append(None)
            else:
                j = self.which_lithology(self.df["friction_number"][i], self.df["qc"][i])
                self.lith.append(self.s.classification[j].name)

    def which_lithology(self, fn, qc):
        lithology = []
        for i in range(0, len(self.s.classification)):
            if self.s.classification[i].qc_min <= qc < self.s.classification[i].qc_max:
                if self.s.classification[i].fn_min <= fn < self.s.classification[i].fn_max:
                    lithology.append(i)
        if len(lithology) == 1:
            return lithology[0]
        elif len(lithology) > 1:
            for i in lithology:
                if self.s.overlay_other_lithology[i]:
                    return i
        else:
            logging.error(f'could not determine soil type by cpt data: fn: {fn}, qc: {qc}')


class ManualSoilClassification:
    def __init__(self):
        self.classification = None
        self.global_qc_max = None
        self.global_qc_min = None
        self.global_fn_max = None
        self.global_fn_min = None
        self.global_level_max = None
        self.global_level_min = None
        self.overlay_other_lithology = []

    def define_soil_classification(self, soil_types=None):
        if self.classification is None:
            self.classification = default.default_soil_types
        else:
            self.classification = soil_types
        self.set_array_overlay()
        self.is_soil_classification_correct()

    def check_status_classification(self):
        if self.classification is None:
            logging.error(f'soil classification not defined! use: self.verify_existence_soil_classification()')
            return False
        return True

    def set_array_overlay(self):
        for i in range(0, len(self.classification)):
            self.overlay_other_lithology.append(False)

    def get_bounding_values_soil_classification(self):
        self.global_qc_max = max([self.classification[i].qc_max for i in range(0, len(self.classification))])
        self.global_qc_min = min([self.classification[i].qc_min for i in range(0, len(self.classification))])
        self.global_fn_max = max([self.classification[i].fn_max for i in range(0, len(self.classification))])
        self.global_fn_min = min([self.classification[i].fn_min for i in range(0, len(self.classification))])

    def plot_soil_classification_diagram(self, qc_max=None, random_color=None):
        if self.check_status_classification() is False:
            raise ValueError("A classification has not been selected")
        self.get_bounding_values_soil_classification()
        if qc_max is None:
            qc_max = self.global_qc_max
        plt.xlabel('Wrijvingsgetal [%]')
        plt.ylabel('Conusweerstand [MPa]')
        plt.axis([self.global_fn_min, self.global_fn_max, self.global_qc_min, qc_max])
        ax = plt.gca()
        color = 'r'
        for i in self.classification:
            if random_color:
                color = numpy.random.random(3)
            x = self.classification[i].fn_min
            y = self.classification[i].qc_min
            w = self.classification[i].fn_max - self.classification[i].fn_min
            h = self.classification[i].qc_max - self.classification[i].qc_min
            if self.overlay_other_lithology[i]:
                rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='w', facecolor='w', fill=True)
                ax.add_patch(rect)
            rect = patches.Rectangle((x, y), w, h, alpha=0.5, linewidth=1, edgecolor='black', facecolor=color, fill=True)
            ax.add_patch(rect)
            if self.classification[i].qc_max > qc_max:
                h = qc_max - self.classification[i].qc_min
            rot = math.degrees(math.atan2(h, w))
            plt.text(x+0.3*w, y+0.3*h, self.classification[i].name, rotation=rot, rotation_mode ='anchor', fontsize=6)
        return plt

    def is_soil_classification_correct(self):
        self.get_bounding_values_soil_classification()
        area = 0.0
        total_area = (self.global_qc_max - self.global_qc_min) * (self.global_fn_max - self.global_fn_min)
        for i in self.classification:
            w = self.classification[i].fn_max - self.classification[i].fn_min
            h = self.classification[i].qc_max - self.classification[i].qc_min
            area = area + w*h

        if abs(area - total_area)/total_area < 0.0001:
            return True
        if area < total_area:
            logging.error(f'soil classification does not cover all possiblities')
            return False
        if area > total_area:
            logging.error(f'soil classification has duplicates')
            self.detect_overlapping_soil_classification()
            return True

    def make_list_corners(self, i):
        point = [[self.classification[i].fn_max, self.classification[i].qc_max],
                 [self.classification[i].fn_max, self.classification[i].qc_min],
                 [self.classification[i].fn_min, self.classification[i].qc_max],
                 [self.classification[i].fn_min, self.classification[i].qc_min]]
        return point

    def detect_overlapping_soil_classification(self):
        for i in range(0, len(self.classification)):
            point_i = self.make_list_corners(i)
            for j in range(0, len(self.classification)):
                if self.classification[i].level_max is not None and self.classification[j].level_max is not None:
                    if self.classification[i].level_max > self.classification[j].level_min or  \
                            self.classification[j].level_max > self.classification[i].level_min:
                        break
                for p in point_i:
                    check = [False,False,False,False]
                    check[0] = self.classification[j].fn_min < p[0]
                    check[1] = self.classification[j].fn_max > p[0]
                    check[2] = self.classification[j].qc_min < p[1]
                    check[3] = self.classification[j].qc_max > p[1]
                    if sum(check) > 3:
                        self.fix_overlapping_soil_classification(i, j)

    def fix_overlapping_soil_classification(self, i, j):
        area_i = (self.classification[i].qc_max - self.classification[i].qc_min)*(self.classification[i].fn_max -
                                                                                  self.classification[i].fn_min)
        area_j = (self.classification[j].qc_max - self.classification[j].qc_min)*(self.classification[j].fn_max -
                                                                                  self.classification[j].fn_min)
        if area_i > area_j:
            logging.error(
                f'Overlay between types, smallest domain chosen as dominant: thus '
                f' type: {self.classification[j].name} dominant over {self.classification[i].name})')
            self.overlay_other_lithology[int(j)] = True
            if i > j:
                a = self.classification[i]
                b = self.classification[j]
                self.classification[i] = b
                self.classification[j] = a
                self.overlay_other_lithology[int(i)] = self.overlay_other_lithology[int(j)]
                self.overlay_other_lithology[int(j)] = False
        if area_i < area_j:
            self.overlay_other_lithology[int(i)] = True
            logging.error(
                f'Overlay between types, smallest domain chosen as dominant: thus'
                f' type: {self.classification[i].name} dominant over {self.classification[j].name})')
            self.overlay_other_lithology[int(i)] = True
            if i < j:
                a = self.classification[i]
                b = self.classification[j]
                self.classification[i] = b
                self.classification[j] = a
                self.overlay_other_lithology[int(j)] = self.overlay_other_lithology[int(i)]
                self.overlay_other_lithology[int(i)] = False

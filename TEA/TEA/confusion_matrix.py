# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 15:26:55 2020

@author: Melissa Gray
"""

#%% VAIABLES AND IMPORTS

import numpy as np
import pandas as pd
import TEA.comparator as comp

'''
 matrix -> Tax_ID: [ TP | FN | FP | TN]
             
# one matrix for each tax_id
    {tax_id : np.array([TP, FN, FP, TN])}

Data Tree:
    - {sample number : dict}
                    - {tax_id : vector}
                                - np.array([TP, FN, FP, TN])
'''


#%% CLASS

class Confusion():
    def __init__(self, tru, fn):
        self.truth = tru
        self.file_name = fn
        return
    
    # GETTERS
    def get_file_name(self):
        return self.file_name
    def get_truth(self):
        return self.truth
    
    # SETTERS
    def set_file_name(self, fn):
        self.file_name = fn
        return
    def set_truth(self, tru):
        self.truth = tru
        return
    
    def dictionary_to_set(self, d):
        '''

        Parameters
        ----------
        d : dictionary
            where sample number is the key and a set of tax_IDs is the value

        Returns
        -------
        dict_set : set
            of all the tax_IDs in d (repeats not included)

        '''
        dict_set = set()
    
        for sample_num in d:
            for tax_id in d[sample_num]:
                dict_set.add(tax_id)
        return dict_set

    def _check_true_positives(self, tax_id, truth, predicted):
        '''

        Parameters
        ----------
        tax_id : integer
            a tax_id from a sample
        truth : dictionary
            where sample number is the key and a set of tax_IDs is the value
            Used as the gold standard
        predicted : dictionary
            where sample number is the key and a set of tax_IDs is the value

        Returns
        -------
        true_positive : integer
            the number of true positives (when it appears where it's supposed to) for the tax_id in Parameters

        '''
        true_positive = 0
    
        for sample_num in predicted:
            if (tax_id in predicted[sample_num]) and (tax_id in truth[sample_num]):
                true_positive += 1
        return true_positive

    def check_true_positives(self, truth, predicted, combined_set):
        '''

        Parameters
        ----------
        truth : dictionary
            where sample number is the key and a set of tax_IDs is the value
            Used as the gold standard
        predicted : dictionary
            where sample number is the key and a set of tax_IDs is the value
        common : dictionary
            where sample number is the key and a set of tax_IDs found in both 
            truth and predicted is the value
        combined: dictionary
            where sample number is the key and a set of tax_IDs from both 
            truth and predicted is the value

        Returns
        -------
        true_positives : dictionary
            where a tax_id is the key and the number of true positives (integer) 
            for that tax_id is the value

        '''
        true_positives = {}
    
        for tax_id in combined_set:
            true_positives[tax_id] = self._check_true_positives(tax_id, truth, predicted)
        return true_positives

    def _check_false_negatives(self, tax_id, truth, predicted):
        '''

        Parameters
        ----------
        tax_id : integer
            a tax_id from a sample
        truth : dictionary
            where sample number is the key and a set of tax_IDs is the value
            Used as the gold standard
        predicted : dictionary
            where sample number is the key and a set of tax_IDs is the value

        Returns
        -------
        false_negative : integer
            the number of false positives for the tax_id

        '''
        false_negative = 0
    
        for sample_num in predicted:
            if (tax_id not in predicted[sample_num]) and (tax_id in truth[sample_num]):
                false_negative += 1
        return false_negative

    def check_false_negatives(self, truth, predicted, combined_set):
        '''

        Parameters
        ----------
        truth : dictionary
            where sample number is the key and a set of tax_IDs is the value
            Used as the gold standard
        predicted : dictionary
            where sample number is the key and a set of tax_IDs is the value
        common : dictionary
            where sample number is the key and a set of tax_IDs found in both 
            truth and predicted is the value
        combined: dictionary
            where sample number is the key and a set of tax_IDs from both 
            truth and predicted is the value

        Returns
        -------
        false_negatives : dictionary
            where tax_id is the key and the number of false negatives is the value

        '''
        # FN = when the tax_id is supposed to be there but it's not
    
        false_negatives = {}
    
        for tax_id in combined_set:
            false_negatives[tax_id] = self._check_false_negatives(tax_id, truth, predicted)
        return false_negatives

    def _check_false_positives(self, tax_id, truth, predicted):
        '''

        Parameters
        ----------
        tax_id : integer
            a tax_id from a sample
        truth : dictionary
            where sample number is the key and a set of tax_IDs is the value
            Used as the gold standard
        predicted : dictionary
            where sample number is the key and a set of tax_IDs is the value

        Returns
        -------
        false_positive : integer
            the number of false positives for the tax_id

        '''
        false_positive = 0
    
        for sample_num in predicted:
            if (tax_id not in truth[sample_num]) and (tax_id in predicted[sample_num]):
                false_positive += 1
        return false_positive

    def check_false_positives(self, truth, predicted, combined_set):
        '''

        Parameters
        ----------
        truth : dictionary
            where sample number is the key and a set of tax_IDs is the value
            Used as the gold standard
        predicted : dictionary
            where sample number is the key and a set of tax_IDs is the value
        combined_set : set
            containing all the tax_ids from truth and predicted.

        Returns
        -------
        false_positives : dictionary
            where tax_id is the key and the number of false postives for that 
            tax_id

        '''
        # FP = when tax_id is there but it's not supposed to be
        false_positives = {}
    
        for tax_id in combined_set:
            false_positives[tax_id] = self. _check_false_positives(tax_id, truth, predicted)
        return false_positives

    def _check_true_negatives(self, tax_id, truth, predicted):
        '''

        Parameters
        ----------
        tax_id : integer
            a tax_id from a sample
        truth : dictionary
            where sample number is the key and a set of tax_IDs is the value
            Used as the gold standard
        predicted : dictionary
            where sample number is the key and a set of tax_IDs is the value

        Returns
        -------
        true_negative : integer
            the number of true positives for the tax_id

        '''
        true_negative = 0
    
        for sample_num in truth:
            if (tax_id not in truth[sample_num]) and (tax_id not in predicted[sample_num]):
                true_negative += 1
        return true_negative

    def check_true_negatives(self, truth, predicted, combined_set):
        '''

        Parameters
        ----------
        truth : dictionary
            where sample number is the key and a set of tax_IDs is the value
            Used as the gold standard
        predicted : dictionary
            where sample number is the key and a set of tax_IDs is the value
        combined_set : set
            containing all the tax_ids from truth and predicted.

        Returns
        -------
        true_negatives : dictionary
            where tax_id is the key and the number of true negatives for that 
            tax_id is the value

        '''
        # TN = when tax_id is not there and it's supposed to not be there
    
        true_negatives = {}
        #truth_set = dictionary_to_set(truth)
    
        for tax_id in combined_set:
            true_negatives[tax_id] = self._check_true_negatives(tax_id, truth, predicted)
        return true_negatives

    def confusion_matrix(self, truth, predicted, common, combined):
        '''
    
        Parameters
        ----------
        truth : dictionary
            where sample number is the key and a set of tax_IDs is the value
            Used as the gold standard
        predicted : dictionary
            where sample number is the key and a set of tax_IDs is the value
        common : dictionary
            where sample number is the key and a set of tax_IDs found in both 
            truth and predicted is the value
        combined: dictionary
            where sample number is the key and a set of tax_IDs from both 
            truth and predicted is the value

        Returns
        -------
        matrix : dictionary
            where tax_id is the key and an array of its true positives, false 
            negatives, false positives, and true negatives is the value

        '''
        matrix = {}
    
        combined_set = self.dictionary_to_set(combined)      # universal set
    
        True_Pos = self.check_true_positives(truth, predicted, combined_set)
        False_Neg = self.check_false_negatives(truth, predicted, combined_set)
        False_Pos = self.check_false_positives(truth, predicted, combined_set)
        True_Neg = self.check_true_negatives(truth, predicted, combined_set)
    
        for tax_id in True_Pos:
            m = np.array([True_Pos[tax_id], False_Neg[tax_id], False_Pos[tax_id], True_Neg[tax_id]])
            matrix[int(tax_id)] = m
        return matrix

    def main(self, csv="yes", t=0):
        Tea = comp.Comparator()
        Chai = comp.pp.Parser()
        '''

        Parameters
        ----------
        pred : string
            first part of the profile file name (don't include the ".profile" part, 
                                             ie. "A_1" or "C_3")
        t : integer, optional
            to toggle the type of parsing. 0 (default) and 1 are the options

        Returns
        -------
        matrix : dictionary
            where tax_id is the key and an array of its true positives, false 
            negatives, false positives, and true negatives is the value

        '''
        truth = Tea.save_tax_ID(Chai.main(self.truth, t))
        predicted = Tea.save_tax_ID(Chai.main(self.file_name, t))
        
        files = self.truth + " " + self.file_name
        common = Tea.common_tax_ID(truth, predicted)
        combined = Tea.combine_tax_ID(truth, predicted)
    
        matrix = self.confusion_matrix(truth, predicted, common, combined)
        
        if csv.lower() == "yes":
            self.save_matrix_table(self.create_matrix_table(self.reformat_matrix(self.add_other_info(matrix))), files)
        return matrix
    
    def matrix_sum(self):
        Chai = comp.pp.Parser()
        truth_sample_sum = len(Chai.divide_content(Chai.get_file(self.truth)))
        return truth_sample_sum
    def check_matrix_error(self, matrix):
        tax_ID_error_over = []
        tax_ID_error_under = []
        truth_sample_sum = self.matrix_sum()
        
        for tax_id in matrix:
            confusion_sum = np.sum(matrix[tax_id])
            if confusion_sum < truth_sample_sum:
                tax_ID_error_under.append(tax_id)
            elif confusion_sum > truth_sample_sum:
                tax_ID_error_over.append(tax_id)
        return tax_ID_error_over, tax_ID_error_under

    def print_matrix_chart(self, matrix):
        '''

        Parameters
        ----------
        matrix : dictionary
            where tax_id is the key and an array of its true positives, false 
            negatives, false positives, and true negatives is the value

        Returns
        -------
        None.

        '''
        # For viewing
        # [TP, FN, FP, TN]
    
        list_tid = []
        for tax_id in matrix:
            list_tid.append(tax_id)
    
        list_tid.sort()
    
        for e in list_tid:
            print("Tax ID:", e)
            print("\t\t\t\tPREDICTED")
            print("\t\t\t\t(+)\t(-)")
            print("\t\t\t(T)\t{}\t{}".format(matrix[e][0], matrix[e][3]))
            print("\tTRUTH")
            print("\t\t\t(F)\t{}\t{}\n".format(matrix[e][2], matrix[e][1]))
        return

    def add_other_info(self, matrix):
        Chai = comp.pp.Parser()
        '''

        Parameters
        ----------
        matrix : dictionary
            where tax_id is the key and an array of its true positives, false 
            negatives, false positives, and true negatives is the value

        Returns
        -------
        whole_matrix : dictionary
            where tax_id is the key and a list of 
            [rank, name, abundance, TP, FN, FP, TN] is the value

        '''
        truth_other = Chai.main(self.truth, 1)
        this_other = Chai.main(self.file_name, 1)
        other_info = {}
        whole_matrix = {}
        
        for sample in this_other:
            for tax_id in this_other[sample]:
                other_info[tax_id] = this_other[sample][tax_id]
            for tax_id in truth_other[sample]:
                if tax_id not in other_info:
                    other_info[tax_id] = truth_other[sample][tax_id]
        
        for tax_id in matrix:
            whole_matrix[tax_id] = np.array((other_info[tax_id]) + list(matrix[tax_id]))
        
        return whole_matrix

    def reformat_matrix(self, whole_matrix):
        reformatted_matrix = {}
        sorted_matrix_table = {}
        rank_list = []
        name_list = []
        TP_list = []
        FN_list = []
        FP_list = []
        TN_list = []
    
        m_t_keys = sorted(whole_matrix)
        for k in m_t_keys:
            sorted_matrix_table[k] = whole_matrix[k]
    
        # saving tax_ids
        reformatted_matrix["Tax ID"] = list(sorted_matrix_table.keys())
        #saving other info
        for k in sorted_matrix_table:
            rank_list.append(sorted_matrix_table[k][0])
            name_list.append(sorted_matrix_table[k][1])
            TP_list.append(sorted_matrix_table[k][2])
            FN_list.append(sorted_matrix_table[k][3])
            FP_list.append(sorted_matrix_table[k][4])
            TN_list.append(sorted_matrix_table[k][5])
    
        reformatted_matrix["Rank"] = rank_list
        reformatted_matrix["Name"] = name_list
        reformatted_matrix["TP"] = TP_list
        reformatted_matrix["FN"] = FN_list
        reformatted_matrix["FP"] = FP_list
        reformatted_matrix["TN"] = TN_list
        return reformatted_matrix

    def create_matrix_table(self, reformatted_matrix):
        '''

        Parameters
        ----------
        matrix_table : list
            containing {tax_id : [rank, name, TP, FN, FP, TN]}

        Returns
        -------
        None.

        '''
        m = pd.DataFrame.from_dict(reformatted_matrix)
        return m

    def save_matrix_table(self, matrix_table, csv_name):
        export_file_path = ''
        s_list = []
        for l in csv_name:
            s_list.append(l)
        s_list.reverse()
        for l in range(len(s_list)):
            if s_list[l] == " ":
                s_list[l] = "--"
                break
        s_list.reverse()
        for l in s_list:
            export_file_path += l
        matrix_table.to_csv (export_file_path+".csv", index = False, header=True)
        return

def example1():
    Tea = comp.Comparator()
    Juice = Confusion("truth", "pred")
    
    a = {1: {1,2,3}, 2: {4,5,6}}    #example truth
    b = {1: {1,2}, 2: {3,5,6,7}}      #example predicted
    print("truth: \t\t{}\npredicted: \t{}\n".format(a, b))
    
    common_AB = Tea.common_tax_ID(a, b)
    combined_AB = Tea.combine_tax_ID(a, b)
    combined_AB_set = Juice.dictionary_to_set(combined_AB)
    print("True Positives:", Juice.check_true_positives(a, b, common_AB, combined_AB))
    print("False Negatives:", Juice.check_false_negatives(a, b, common_AB, combined_AB_set))
    print("False Positives:", Juice.check_false_positives(a, b, combined_AB_set))
    print("True Negatives:", Juice.check_true_negatives(a, b, combined_AB_set))
    return

def example2():
    Tea = comp.Comparator()
    Juice = Confusion("truth", "pred")
    
    a = {1: {1,2,3}, 2: {4,5,6}, 3 : {7,8,9}}    #example truth
    b = {1: {1,2,8}, 2: {3,5,6,7}, 3: {9,10}}      #example predicted
    print("truth: \t\t{}\npredicted: \t{}\n".format(a, b))
    
    common_AB = Tea.common_tax_ID(a, b)
    combined_AB = Tea.combine_tax_ID(a, b)
    
    Juice.print_matrix_chart(Juice.confusion_matrix(a, b, common_AB, combined_AB))
    return

def example3():
    Juice = Confusion("truth", "pred")
    
    m1 = Juice.main()
    m2 = Juice.main()
    
    print("PREDICTED:\n")
    Juice.print_matrix_chart(m1)
    
    print()
    
    print("Predicted:")
    print(Juice.create_matrix_table(Juice.add_other_info(m1)))
    print("\nTruth:")
    print(Juice.create_matrix_table(Juice.add_other_info(m2)))
    return

def example4():
    Juice = Confusion("truth", "pred")
    
    matrix = Juice.main()
    matrix_plus = Juice.add_other_info(matrix)
    reformated_matrix_plus = Juice.reformat_matrix(matrix_plus)
    re_matrix_plus_table = Juice.create_matrix_table(reformated_matrix_plus)
    
    Juice.save_matrix_table(re_matrix_plus_table)
    return

def example5():
    Juice2 = Confusion("A_1", "B_1")
    j2_matrix = Juice2.main()
    
    over, under = Juice2.check_matrix_error(j2_matrix)
    print(over[:10], "\n\n", under[:10])
    return


#%% MAIN

if __name__ == "__main__":
    '''
    Juice = Confusion("truth", "pred")
    
    m = Juice.main("yes")
    
    print(Juice.check_matrix_error(m))
    '''
    
    

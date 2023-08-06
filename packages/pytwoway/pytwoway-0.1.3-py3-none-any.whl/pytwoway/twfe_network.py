'''
Class for a two-way fixed effect network
'''
import logging
from pathlib import Path
import pytwoway as tw
import bipartitepandas as bpd

class TwoWay():
    '''
    Class of TwoWay, where TwoWay gives a network of firms and workers. Inherits from bipartitepandas.
    '''

    def __init__(self, data, formatting='long', col_dict=None):
        '''
        Arguments:
            data (Pandas DataFrame): data giving firms, workers, and compensation
            formatting (str): if 'long', then data in long format; if 'long_collapsed' then in collapsed long format; if 'es', then data in event study format; if 'es_collapsed' then in collapsed event study format. If simulating data, keep default value of 'long'
            col_dict (dict): make data columns readable (requires:
                if long: wid (worker id), comp (compensation), fid (firm id), year;
                if event study: wid (worker id), y1 (compensation 1), y2 (compensation 2), f1i (firm id 1), f2i (firm id 2), m (0 if stayer, 1 if mover);
                    optionally include: year_end_1 (last year of observation 1), year_end_2 (last year of observation 2), w1 (weight 1), w2 (weight 2)).
                Keep None if column names already correct
        '''
        # Start logger
        bpd.logger_init(self)
        # self.logger.info('initializing TwoWay object')

        if formatting == 'long':
            self.data = bpd.BipartiteLong(data, col_dict=col_dict)
        elif formatting == 'long_collapsed':
            self.data = bpd.BipartiteLongCollapsed(data, col_dict=col_dict)
        if formatting == 'es':
            self.data = bpd.BipartiteEventStudy(data, col_dict=col_dict)
        elif formatting == 'es_collapsed':
            self.data = bpd.BipartiteEventStudyCollapsed(data, col_dict=col_dict)

        self.formatting = formatting
        self.clean = False # Whether data is clean

        # Define default parameter dictionaries
        self.default_fe = {'ncore': 1, 'batch': 1, 'ndraw_pii': 50, 'levfile': '', 'ndraw_tr': 5, 'h2': False, 'out': 'res_fe.json', 'statsonly': False, 'Q': 'cov(alpha, psi)', 'con': False, 'logfile': '', 'check': False} # Do not define 'data' because will be updated later

        self.default_cre = {'ncore': 1, 'ndraw_tr': 5, 'ndp': 50, 'out': 'res_cre.json', 'posterior': False, 'wo_btw': False} # Do not define 'data' because will be updated later

        # self.logger.info('TwoWay object initialized')

    def __prep_fe(self):
        '''
        Prepare bipartite network for running fit_fe.

        Returns:
            frame (BipartitePandas): prepared data
        '''
        if not self.clean:
            self.data = self.data.clean_data()
            self.clean = True

        frame = self.data.copy()

        if self.formatting == 'es':
            frame = frame.get_long()
        if self.formatting in ['es', 'long']:
            frame = frame.get_collapsed_long()
        if self.formatting in ['es', 'long', 'long_collapsed']:
            frame = frame.get_es()

        return frame

    def __prep_cre(self, user_cluster={}):
        '''
        Prepare bipartite network for running fit_cre.

        Arguments:
            user_cluster (dict): dictionary of parameters for clustering

                Dictionary parameters:

                    cdf_resolution (int): how many values to use to approximate the cdf

                    grouping (str): how to group the cdfs ('quantile_all' to get quantiles from entire set of data, then have firm-level values between 0 and 1; 'quantile_firm_small' to get quantiles at the firm-level and have values be compensations if small data; 'quantile_firm_large' to get quantiles at the firm-level and have values be compensations if large data, note that this is up to 50 times slower than 'quantile_firm_small' and should only be used if the dataset is too large to copy into a dictionary)

                    year (int or None): if None, uses entire dataset; if int, gives year of data to consider

                    user_KMeans (dict): use parameters defined in KMeans_dict for KMeans estimation (for more information on what parameters can be used, visit https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html), and use default parameters defined in class attribute default_KMeans for any parameters not specified

        Returns:
            frame (BipartitePandas): prepared data
        '''
        if not self.clean:
            self.data = self.data.clean_data()
            self.clean = True

        frame = self.data.copy()

        if self.formatting == 'es':
            frame = frame.get_long()
        if self.formatting in ['es', 'long']:
            frame = frame.get_collapsed_long()
        if self.formatting in ['es', 'long', 'long_collapsed']:
            frame = frame.get_es()
        frame = frame.cluster(user_cluster=user_cluster)

        return frame

    def fit_fe(self, user_fe={}):
        '''
        Fit the bias-corrected FE estimator. Saves two dictionary attributes: self.fe_res (complete results) and self.fe_summary (summary results).

        Arguments:
            user_fe (dict): dictionary of parameters for bias-corrected FE estimation

                Dictionary parameters:

                    ncore (int): number of cores to use

                    batch (int): batch size to send in parallel

                    ndraw_pii (int): number of draws to use in approximation for leverages

                    levfile (str): file to load precomputed leverages

                    ndraw_tr (int): number of draws to use in approximation for traces

                    h2 (bool): if True, compute h2 correction

                    out (str): outputfile where results are saved

                    statsonly (bool): if True, return only basic statistics

                    Q (str): which Q matrix to consider. Options include 'cov(alpha, psi)' and 'cov(psi_t, psi_{t+1})'

                    con (str): computes the smallest eigen values, this is the filepath where these results are saved @ FIXME I don't think this is used

                    logfile (str): log output to a logfile @ FIXME I don't think this is used

                    check (bool): whether to compute the non-approximated estimates as well @ FIXME I don't think this is used
        '''
        frame = self.__prep_fe()
        fe_params = bpd.update_dict(self.default_fe, user_fe)

        fe_params['data'] = frame.get_cs() # Make sure to use up-to-date bipartite network

        fe_solver = tw.FEEstimator(fe_params)
        fe_solver.fit_1()
        fe_solver.construct_Q() # Comment out this line and manually create Q if you want a custom Q matrix
        fe_solver.fit_2()

        self.fe_res = fe_solver.res
        self.fe_summary = fe_solver.summary

    def fit_cre(self, user_cre={}, user_cluster={}):
        '''
        Fit the CRE estimator. Saves two dictionary attributes: self.cre_res (complete results) and self.cre_summary (summary results).

        Arguments:
            user_cre (dict): dictionary of parameters for CRE estimation

                Dictionary parameters:

                    ncore (int): number of cores to use

                    ndraw_tr (int): number of draws to use in approximation for traces

                    ndp (int): number of draw to use in approximation for leverages

                    out (str): outputfile

                    posterior (bool): compute posterior variance

                    wo_btw (bool): sets between variation to 0, pure RE

            user_cluster (dict): dictionary of parameters for clustering

                Dictionary parameters:

                    cdf_resolution (int): how many values to use to approximate the cdf

                    grouping (str): how to group the cdfs ('quantile_all' to get quantiles from entire set of data, then have firm-level values between 0 and 1; 'quantile_firm_small' to get quantiles at the firm-level and have values be compensations if small data; 'quantile_firm_large' to get quantiles at the firm-level and have values be compensations if large data, note that this is up to 50 times slower than 'quantile_firm_small' and should only be used if the dataset is too large to copy into a dictionary)

                    year (int or None): if None, uses entire dataset; if int, gives year of data to consider

                    user_KMeans (dict): use parameters defined in KMeans_dict for KMeans estimation (for more information on what parameters can be used, visit https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html), and use default parameters defined in class attribute default_KMeans for any parameters not specified
        '''
        frame = self.__prep_cre(user_cluster=user_cluster)
        cre_params = bpd.update_dict(self.default_cre, user_cre)

        cre_params['data'] = frame.get_cs() # Make sure to use up-to-date data

        cre_solver = tw.CREEstimator(cre_params)
        cre_solver.fit()

        self.cre_res = cre_solver.res
        self.cre_summary = cre_solver.summary

    def summary_fe(self):
        '''
        Return summary results for FE estimator.

        Returns:
            self.fe_summary (dict): dictionary of FE summary results
        '''
        return self.fe_summary

    def summary_cre(self):
        '''
        Return summary results for CRE estimator.

        Returns:
            self.cre_summary (dict): dictionary of CRE summary results
        '''
        return self.cre_summary

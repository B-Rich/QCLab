# This file is part of Bika LIMS
#
# Copyright 2011-2016 by it's authors.
# Some rights reserved. See LICENSE.txt, AUTHORS.txt.

""" Generic controller for instrument results import view
"""
import json
import traceback
from bika.lims.exportimport.instruments.resultsimport import AnalysisResultsImporter

def getFileFormat(request):
    return request.form['instrument_results_file_format']

def getResultsInputFile(request):
    return request.form['instrument_results_file']


def GenericImport(context, request, parser, importer=None):
    infile = getResultsInputFile(request)
    fileformat = getFileFormat(request)
    artoapply = request.form['artoapply']
    override = request.form['results_override']
    sample = request.form.get('sample', 'requestid')
    instrument = request.form.get('qcinstrument', None)
    errors = []
    logs = []
    warns = []
    # Load the most suitable parser according to file extension/options/etc...
    if not hasattr(infile, 'filename'):
        errors.append(_("No file selected"))

    if parser:
        # Load the importer
        status = ['sample_received', 'attachment_due', 'to_be_verified']
        if artoapply == 'received':
            status = ['sample_received']
        elif artoapply == 'received_tobeverified':
            status = ['sample_received', 'attachment_due', 'to_be_verified']

        over = [False, False]
        if override == 'nooverride':
            over = [False, False]
        elif override == 'override':
            over = [True, False]
        elif override == 'overrideempty':
            over = [True, True]

        sam = ['getRequestID', 'getSampleID', 'getClientSampleID']
        if sample == 'requestid':
            sam = ['getRequestID']
        if sample == 'sampleid':
            sam = ['getSampleID']
        elif sample == 'clientsid':
            sam = ['getClientSampleID']
        elif sample == 'sample_clientsid':
            sam = ['getSampleID', 'getClientSampleID']

        imp = importer
        if not imp:
            imp = AnalysisResultsImporter(parser=parser,
                                          context=context,
                                          idsearchcriteria=sam,
                                          allowed_ar_states=status,
                                          allowed_analysis_states=None,
                                          override=over,
                                          instrument_uid=instrument)

        tbex = ''
        try:
            imp.process()
        except:
            tbex = traceback.format_exc()
        errors = imp.errors
        logs = imp.logs
        warns = imp.warns
        if tbex:
            errors.append(tbex)

    results = {'errors': errors, 'log': logs, 'warns': warns}

    return json.dumps(results)

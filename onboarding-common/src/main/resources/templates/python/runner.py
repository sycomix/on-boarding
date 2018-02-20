#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Provides a model runner application for Acumos Python models
'''
import argparse
import json
from functools import partial

import requests
from flask import Flask, request, current_app
from google.protobuf import json_format

from acumos.wrapped import load_model


def invoke_method(model_method, downstream):
    '''Consumes and produces protobuf binary data'''
    app = current_app
    # print("[{:}] JSON I/O Flag: {:}".format(model_method, app.json_io))
    bytes_in = request.data
    if not bytes_in:
        if request.form:
            bytes_in = dict(request.form)
        elif request.args:
            bytes_in = dict(request.args)
    if type(bytes_in) == dict:  # attempt to push arguments into JSON for more tolerant parsing
        bytes_in = json.dumps(bytes_in)
    try:
        if app.json_io:
            msg_in = json_format.Parse(bytes_in, model_method.pb_input_type())  # attempt to decode JSON
            msg_out = model_method.from_pb_msg(msg_in)
        else:
            msg_out = model_method.from_pb_bytes(bytes_in)  # default from-bytes method

        if app.json_io:
            bytes_out = json_format.MessageToJson(msg_out.as_pb_msg())
        else:
            bytes_out = msg_out.as_pb_bytes()
    except json_format.ParseError as e:
        type_input = list(model_method.pb_input_type.DESCRIPTOR.fields_by_name.keys())
        return "Value specification error, expected  {:}, {:}".format(type_input, e), 400
    except (ValueError, TypeError) as e:
        return "Value conversion error: {}".format(e), 400

    for url in downstream:
        try:
            requests.post(url, data=bytes_out)
        except Exception as e:
            print("Failed to publish to downstream url {} : {}".format(url, e))
    if app.return_output:
        return bytes_out, 201
    return 'OK', 201


if __name__ == '__main__':
    '''Main'''
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=3330)
    parser.add_argument("--modeldir", type=str, default='model', help='specify the model directory to load')
    parser.add_argument("--json_io", action='store_true', help='input+output rich JSON instead of protobuf')
    parser.add_argument("--return_output", action='store_true',
                        help='return output in response instead of just downstream')
    pargs = parser.parse_args()

    try:
        with open('runtime.json') as f:
            runtime = json.load(f)  # ad-hoc way of giving the app runtime parameters

        downstream = runtime['downstream']  # list of IP:port/path urls
    except:
        print ("No runtime.json file--ignoring")
        downstream = []

    model = load_model(pargs.modeldir)  # refers to ./model dir in current directory

    app = Flask(__name__)
    app.json_io = pargs.json_io  # store io flag
    app.return_output = pargs.return_output  # store output

    # dynamically add handlers depending on model capabilities
    for method_name, method in model.methods.items():
        handler = partial(invoke_method, model_method=method, downstream=downstream)
        url = "/{}".format(method_name)
        app.add_url_rule(url, method_name, handler, methods=['POST', 'GET'])

        # render down the input in few forms
        typeInput = list(method.pb_input_type.DESCRIPTOR.fields_by_name.keys())
        msgInput = method.pb_input_type()
        jsonInput = json_format.MessageToDict(msgInput)

        # render down the output in few forms
        typeOutput = list(method.pb_output_type.DESCRIPTOR.fields_by_name.keys())
        msgOutput = method.pb_output_type()
        jsonOutput = json_format.MessageToDict(msgOutput)

        print("Adding route {} [input:{:}, output:{:}]".format(url, typeInput, typeOutput))

    print("Running Flask server on port {}".format(pargs.port))
    app.run(port=pargs.port)
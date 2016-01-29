#!/usr/bin/env python
# encoding: utf-8
'''
generateCmake.py

@author:     Damian Abalo Miron <damian.abalo@cern.ch>
@author:     Piotr Nikiel <piotr@nikiel.info>

@copyright:  2015 CERN

@license:
Copyright (c) 2015, CERN, Universidad de Oviedo.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

@contact:    damian.abalo@cern.ch
'''

import os
import sys
import subprocess
import platform
from transformDesign import transformDesignVerbose

def generateCmake(BUILD_TYPE="Release", CMAKE_TOOLCHAIN_FILE="default_configuration.cmake"):
	"""Generates CMake header lists in various directories, and then calls cmake.
	
	Keyword arguments:
	BUILD_TYPE -- Optional parameter to specify Debug or Release build. If it is not specified it will default to Release.
	"""	
	returnCode = transformDesignVerbose("AddressSpace" + os.path.sep + "designToGeneratedCmakeAddressSpace.xslt", "AddressSpace" + os.path.sep + "cmake_generated.cmake", 0, 0)
	returnCode = transformDesignVerbose("Device" + os.path.sep + "designToGeneratedCmakeDevice.xslt", "Device" + os.path.sep + "generated" + os.path.sep + "cmake_header.cmake", 0, 0)
	print("Build type ["+BUILD_TYPE+"], Toolchain file [" + CMAKE_TOOLCHAIN_FILE + "]")

	print("Calling CMake")
	if platform.system() == "Windows":
		returnCode = subprocess.call("cmake -DCMAKE_BUILD_TYPE=" + BUILD_TYPE + " -DCMAKE_TOOLCHAIN_FILE=" + CMAKE_TOOLCHAIN_FILE + " -G \"Visual Studio 12 Win64\" .", shell=True)
	elif platform.system() == "Linux":
		returnCode = subprocess.call("cmake -DCMAKE_BUILD_TYPE=" + BUILD_TYPE + " -DCMAKE_TOOLCHAIN_FILE=" + CMAKE_TOOLCHAIN_FILE + " .", shell=True)
	if returnCode != 0:
		print("There was a problem calling cmake; Return code = " + str(returnCode))
		return returnCode
	return 0#return code 0 if everything went well.
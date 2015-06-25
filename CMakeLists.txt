CMAKE_MINIMUM_REQUIRED(VERSION 3.1.0 FATAL_ERROR)

# BTKPython: Python binding for the C++ library Biomechanical ToolKit
PROJECT(BTKPython)

# BTKPython version number.
SET(BTKPython_VERSION_MAJOR 1)
SET(BTKPython_VERSION_MINOR 0)
SET(BTKPython_VERSION_PATCH 0)
SET(BTKPython_VERSION "${BTKPython_VERSION_MAJOR}.${BTKPython_VERSION_MINOR}.${BTKPython_VERSION_PATCH}")
SET(BTKPython_VERSION_STRING ${BTKPython_VERSION})
# The major.minor is enough to distinguish available features of the toolkit. Moreover, 
# this variable is used to create lib/share/include folders where the patch number does 
# not need to be included.
SET(BTKPython_LIBRARY_VERSION_STRING "${BTKPython_VERSION_MAJOR}.${BTKPython_VERSION_MINOR}")

# ------------------------------------------------------------------------
# CMAKE GENERAL CONFIGURATION
# ------------------------------------------------------------------------

SET(CMAKE_INCLUDE_CURRENT_DIR ON)
SET(CMAKE_INCLUDE_CURRENT_DIR_IN_INTERFACE ON)
SET(CMAKE_CXX_STANDARD 11)
SET(CMAKE_CXX_STANDARD_REQUIRED ON)

IF((CMAKE_SYSTEM_NAME STREQUAL "Darwin") AND (CMAKE_CXX_COMPILER_ID STREQUAL "AppleClang"))
  SET(CMAKE_CXX_FLAGS "-stdlib=libc++")
  # CMake 3.1 complains it does not know how to set the compile flag to enable C++11 with (Apple) Clang
  SET(CMAKE_CXX11_STANDARD_COMPILE_OPTION "-std=c++11")
  SET(CMAKE_CXX11_EXTENSION_COMPILE_OPTION "-std=gnu++11")
ELSEIF((CMAKE_SYSTEM_NAME STREQUAL "Windows") AND MSVC)
  # CMake 3.1 complains it does not know how to set the compile flag to enable C++11 with MSVC
  SET(CMAKE_CXX11_STANDARD_COMPILE_OPTION "")
  SET(CMAKE_CXX11_EXTENSION_COMPILE_OPTION "")
  # CXX Flag details
  #  - EHsc: enable exception handling for C++ object
  #  - D_SCL_SECURE_NO_WARNINGS: disable function call with unsafe parameters warning
  SET(CMAKE_CXX_FLAGS "/EHsc -D_SCL_SECURE_NO_WARNINGS")
ENDIF()

SET(BTKPython_CMAKE_MODULE_PATH "${BTKPython_SOURCE_DIR}/CMake")
SET(CMAKE_MODULE_PATH "${BTKPython_CMAKE_MODULE_PATH}")

# ------------------------------------------------------------------------
# COMPILATION INSTRUCTIONS
# ------------------------------------------------------------------------

# Using the configuration "Always full RPATH"
# from http://www.cmake.org/Wiki/CMake_RPATH_handling
#             --------------------------
# use, i.e. don't skip the full RPATH for the build tree
SET(CMAKE_SKIP_BUILD_RPATH  FALSE)
# when building, don't use the install RPATH already
# (but later on when installing)
SET(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE) 
# the RPATH to be used when installing
SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib/btk-${BTKPython_LIBRARY_VERSION_STRING}")
# add the automatically determined parts of the RPATH
# which point to directories outside the build tree to the install RPATH
SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

# Output directories.
SET(LIBRARY_OUTPUT_PATH ${BTKPython_BINARY_DIR}/bin CACHE INTERNAL "Single output directory for building all libraries.")
SET(BTKPython_LIBRARY_PATH "${LIBRARY_OUTPUT_PATH}")
SET(EXECUTABLE_OUTPUT_PATH ${BTKPython_BINARY_DIR}/bin CACHE INTERNAL "Single output directory for building all executables.")
SET(BTKPython_EXECUTABLE_PATH "${EXECUTABLE_OUTPUT_PATH}")

# Load some CMake macros.
INCLUDE(GenerateExportHeader)
INCLUDE(CMakePackageConfigHelpers)

# By default BTK is compiled in Release mode
IF(NOT CMAKE_BUILD_TYPE)
  MESSAGE(STATUS "Setting build type to 'Release' as none was specified.")
  SET(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  # Set the possible values of build type for cmake-gui
  SET_PROPERTY(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
ENDIF()

# BTK build configuration option (SHARED by default).
OPTION(BUILD_SHARED_LIBS "Build BTK with shared libraries." ON)
SET(BTKPython_BUILD_SHARED_LIBS ${BUILD_SHARED_LIBS})
IF(WIN32)
   IF(BUILD_SHARED_LIBS)
     SET(BTKPython_LIBS_BUILD_TYPE "SHARED")
   ELSE(BUILD_SHARED_LIBS)
     SET(BTKPython_LIBS_BUILD_TYPE "STATIC")
   ENDIF(BUILD_SHARED_LIBS)
ENDIF()

IF(WIN32)
  SET(BTKPython_LIBRARY_PREFIX "btk")
ELSE()
  SET(BTKPython_LIBRARY_PREFIX "libbtk")
ENDIF()
SET(BTKPython_LIBRARY_PROPERTIES 
  VERSION   "${BTKPython_VERSION_MAJOR}.${BTKPython_VERSION_MINOR}.${BTKPython_VERSION_PATCH}"
  SOVERSION "${BTKPython_VERSION_MAJOR}.${BTKPython_VERSION_MINOR}"
  PREFIX    "${BTKPython_LIBRARY_PREFIX}"
  DEBUG_POSTFIX _debug)

# ------------------------------------------------------------------------
# PROJECT'S SUBDIRECTORIES
# ------------------------------------------------------------------------

# Code
ADD_SUBDIRECTORY(Code)

# TDD (Test-driven development) code
OPTION(BUILD_TESTING "Build BTK unit and regression tests." OFF)
IF(BUILD_TESTING)
  ENABLE_TESTING()
  ADD_SUBDIRECTORY(Testing)
ENDIF(BUILD_TESTING)
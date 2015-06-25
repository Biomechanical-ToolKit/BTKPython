SET(CMAKE_AUTOMOC ON)
SET(CMAKE_INCLUDE_CURRENT_DIR ON)

FIND_PACKAGE(BTK REQUIRED)
FIND_PACKAGE(PythonLibs REQUIRED)
FIND_PACKAGE(PythonQt REQUIRED)
FIND_PACKAGE(Qt5_ROOT_PATH REQUIRED)
FIND_PACKAGE(Qt5 5.4 COMPONENTS Core REQUIRED)

# --------------------------------------------------------------------------- #
#                                 Library
# --------------------------------------------------------------------------- #

INCLUDE_DIRECTORIES(
  ${PYTHON_INCLUDE_PATH}
  ${PythonQt_INCLUDE_DIRS}
)

SET(btkPythonBinding_SRCS
  btkPythonBinding.cpp
  # btkBase
  btkBase/btk_python_init_btkBase.cpp
  btkBase/btkNode_pyq.cpp
  # btkIO
  btkIO/btk_python_init_btkIO.cpp
  # btkModel
  btkModel/btk_python_init_btkModel.cpp
  # btkTrial
  btkTrial/btk_python_init_btkTrial.cpp
)

ADD_LIBRARY(Python SHARED ${btkPythonBinding_SRCS})

TARGET_INCLUDE_DIRECTORIES(Python PUBLIC
  $<BUILD_INTERFACE:${BTKPython_SOURCE_DIR}>
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/btkBase>
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/btkIO>
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/btkModel>
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/btkTrial>
  # $<INSTALL_INTERFACE:include/...>  # FIXME : Installation path?
)

GENERATE_EXPORT_HEADER(Python
                       BASE_NAME BTK_PYTHON
                       EXPORT_FILE_NAME btkPythonExport.h)
                       
SET_TARGET_PROPERTIES(Python PROPERTIES ${BTKPython_LIBRARY_PROPERTIES})
IF (NOT ${BTKPython_BUILD_SHARED_LIBS})
  SET_TARGET_PROPERTIES(Python PROPERTIES COMPILE_FLAGS -DBTK_PYTHON_STATIC_DEFINE)
ENDIF()

TARGET_LINK_LIBRARIES(Python BTK::Base Qt5::Core ${PythonQt_LIBRARIES})

# --------------------------------------------------------------------------- #
#                                  Module
# --------------------------------------------------------------------------- #

SET(btkPythonModule_SRCS
  btkPythonModule.cpp
)

ADD_LIBRARY(_btk MODULE ${btkPythonModule_SRCS})
SET_TARGET_PROPERTIES(_btk PROPERTIES
  LINKER_LANGUAGE C
  PREFIX "")

TARGET_LINK_LIBRARIES(_btk Python)
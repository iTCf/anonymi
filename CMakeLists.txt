cmake_minimum_required(VERSION 3.5)

project(Anonymi)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/Anonymi")
set(EXTENSION_CATEGORY "Anonymi")
set(EXTENSION_CONTRIBUTORS "Ezequiel Mikulan (UNIMI)")
set(EXTENSION_DESCRIPTION "Anonymize MRI")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/Anonymi.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/Anonymi/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a space separated string, a list or 'NA' if any

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(Anonymi)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})

cmake_minimum_required(VERSION 3.10)
project(HERON_gs_server)

include(GNUInstallDirs)

file(GLOB trx_files "${CMAKE_SOURCE_DIR}/transceivers/*.grc")
configure_file(doppler.service.in doppler.service @ONLY)
configure_file(HERON_gs.service.in HERON_gs.service @ONLY)

# install(FILES ${trx_files} DESTINATION "${CMAKE_INSTALL_DATADIR}/${PROJECT_NAME}/transceivers/")
install(DIRECTORY
    transceivers
    DESTINATION "${CMAKE_INSTALL_LIBDIR}/${PROJECT_NAME}")
install(FILES
    doppler.py
    HERON_gs.py
    DESTINATION "${CMAKE_INSTALL_LIBDIR}/${PROJECT_NAME}/")
install(FILES
    ${CMAKE_BINARY_DIR}/doppler.service
    ${CMAKE_BINARY_DIR}/HERON_gs.service
    DESTINATION "${CMAKE_INSTALL_LIBDIR}/systemd/system/")


set(CPACK_DEBIAN_PACKAGE_DEPENDS "python3")
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "Swarnava Ghosh")
include(CPack)


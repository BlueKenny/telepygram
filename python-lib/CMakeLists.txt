execute_process(
    COMMAND dpkg-architecture -qDEB_HOST_MULTIARCH
    OUTPUT_VARIABLE ARCH_TRIPLET
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

set(LIB_DIR "/lib/${ARCH_TRIPLET}")
set(BIN_DIR "/bin")

#install(DIRECTORY ${ARCH_TRIPLET}/io DESTINATION ${LIB_DIR})
#install(FILES ${ARCH_TRIPLET}/libpython3.4m.so.1 DESTINATION ${LIB_DIR})
#install(FILES ${ARCH_TRIPLET}/libpython3.4m.so.1.0 DESTINATION ${LIB_DIR})

install(DIRECTORY ${ARCH_TRIPLET}/QtQuick DESTINATION ${LIB_DIR})
install(DIRECTORY ${ARCH_TRIPLET}/Dekko DESTINATION ${LIB_DIR})

#install(DIRECTORY ${ARCH_TRIPLET}/valgrind DESTINATION /lib/)

#install(DIRECTORY ${ARCH_TRIPLET}/bin/pdb3 DESTINATION ${BIN_DIR})
#install(DIRECTORY ${ARCH_TRIPLET}/bin/pydoc3 DESTINATION ${BIN_DIR})
#install(DIRECTORY ${ARCH_TRIPLET}/bin/pygettext3 DESTINATION ${BIN_DIR})


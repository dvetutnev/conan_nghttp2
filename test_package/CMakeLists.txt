project(PackageTest CXX C)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

include_directories(${CONAN_INCLUDE_DIRS})

add_executable(server server.cpp)
target_link_libraries(server ${CONAN_LIBS})

#add_executable(client client.cpp)
#target_link_libraries(client ${CONAN_LIBS})

file(COPY selfsigned.crt selfsigned.key index.html DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/bin)

enable_testing()

add_test(
    NAME server
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin
    COMMAND server
    )

#add_test(
#    NAME client
#    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/bin
#    COMMAND client
#    )

from conans import ConanFile, CMake


class Nghttp2Conan(ConanFile):
    name = "nghttp2"
    version = "1.27.90"
    license = "MIT"
    url = "https://github.com/nghttp2/nghttp2"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    requires = "zlib/[>1.2.3]@odant/stable", \
               "openssl/1.1.0f@odant/prebuild", \
               "boost_libraries/[>1.65.0]@odant/prebuild"
    exports_sources = "src/*", \
                      "CMakeLists.txt"
    build_policy = "missing"

    def build(self):
        cmake = CMake(self)
        if (
                self.settings.os == "Windows" and self.settings.compiler == "Visual Studio" and
                self.settings.compiler.toolset is not None and self.settings.compiler.toolset != "None"
           ):
            self.output.info("MSVC toolset: %s" % self.settings.compiler.toolset)
            self.run('cmake %s -T %s %s' % (self.source_folder, self.settings.compiler.toolset, cmake.command_line))
        else:
            self.run('cmake %s %s' % (self.source_folder, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="src/src/includes")
        self.copy("*.h", dst="include", src="src/lib/includes")
        self.copy("*.lib", dst="lib", keep_path=False, excludes="*http-parser*")
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.pdb", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False, excludes="*http-parser*")

        if self.settings.os == "Windows" and self.settings.build_type == "Release":
            signtool = '"C:\\Program Files (x86)\\Microsoft SDKs\\Windows\\v7.1A\\bin\\signtool"'
            params =  "sign /a /t http://timestamp.verisign.com/scripts/timstamp.dll"
            self.run("{} {} {}\\bin\\{}".format(signtool, params, self.package_folder, "nghttp2.dll"))
            self.run("{} {} {}\\bin\\{}".format(signtool, params, self.package_folder, "nghttp2_asio.dll"))
        
    def package_info(self):
        self.cpp_info.libs = ["nghttp2", "nghttp2_asio"]

        if (self.settings.os == "Windows" and self.settings.compiler == "Visual Studio"):
            self.cpp_info.defines = ["NOMINMAX", "ssize_t=int"]
            if self.settings.build_type == "Debug":
                self.cpp_info.libs[0] += "d"
                self.cpp_info.libs[1] += "d"


from conans import ConanFile, CMake


class Nghttp2TestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        if (
                self.settings.os == "Windows" and self.settings.compiler == "Visual Studio" and
                self.settings.compiler.toolset is not None and self.settings.compiler.toolset != "None"
           ):
            self.run('cmake %s -T %s %s' % (self.source_folder, self.settings.compiler.toolset, cmake.command_line))
        else:
            self.run('cmake %s %s' % (self.source_folder, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        self.run("ctest --output-on-failure --build-config %s" % self.settings.build_type)

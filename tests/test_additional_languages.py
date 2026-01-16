# File: tests/test_additional_languages.py
# pylint: disable=duplicate-code

"""Tests for additional programming language support."""

from pathlib import Path

import pytest

from annot8.annotate_headers import _get_comment_style, process_file
from tests.test_utils import cleanup_test_directory, create_temp_test_directory

# Directory for temporary test files
TEST_DIR = Path("tests/sample_files")


@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    """Setup test environment and cleanup after tests."""
    create_temp_test_directory(TEST_DIR)
    yield
    cleanup_test_directory(TEST_DIR)


class TestObjectiveC:
    """Test Objective-C file support."""

    def test_objective_c_comment_style(self):
        """Test Objective-C comment style detection."""
        objc_file = TEST_DIR / "test.m"
        objc_file.write_text("@interface TestClass : NSObject\n@end")
        comment_style = _get_comment_style(objc_file)
        assert comment_style == ("//", ""), "Incorrect comment style for Objective-C"

    def test_objective_cpp_comment_style(self):
        """Test Objective-C++ comment style detection."""
        objcpp_file = TEST_DIR / "test.mm"
        objcpp_file.write_text("#include <iostream>\nclass Test {};")
        comment_style = _get_comment_style(objcpp_file)
        assert comment_style == ("//", ""), "Incorrect comment style for Objective-C++"


class TestGroovy:
    """Test Groovy file support."""

    def test_groovy_comment_style(self):
        """Test Groovy comment style detection."""
        groovy_file = TEST_DIR / "test.groovy"
        groovy_file.write_text("def hello() { println 'Hello' }")
        comment_style = _get_comment_style(groovy_file)
        assert comment_style == ("//", ""), "Incorrect comment style for Groovy"

    def test_groovy_file_processing(self):
        """Test processing Groovy files."""
        groovy_file = TEST_DIR / "test.groovy"
        groovy_file.write_text("def hello() { println 'Hello' }")
        process_file(groovy_file, TEST_DIR)
        content = groovy_file.read_text()
        assert content.startswith("// File: test.groovy"), "Header not added correctly for Groovy"


class TestClojure:
    """Test Clojure file support."""

    def test_clojure_comment_style(self):
        """Test Clojure comment style detection."""
        clj_file = TEST_DIR / "test.clj"
        clj_file.write_text('(defn hello [] (println "Hello"))')
        comment_style = _get_comment_style(clj_file)
        assert comment_style == (";;", ""), "Incorrect comment style for Clojure"

    def test_clojure_file_processing(self):
        """Test processing Clojure files."""
        clj_file = TEST_DIR / "test.clj"
        clj_file.write_text('(defn hello [] (println "Hello"))')
        process_file(clj_file, TEST_DIR)
        content = clj_file.read_text()
        assert content.startswith(";; File: test.clj"), "Header not added correctly for Clojure"


class TestFSharp:
    """Test F# file support."""

    def test_fsharp_comment_style(self):
        """Test F# comment style detection."""
        fs_file = TEST_DIR / "test.fs"
        fs_file.write_text('let hello = printfn "Hello"')
        comment_style = _get_comment_style(fs_file)
        assert comment_style == ("//", ""), "Incorrect comment style for F#"

    def test_fsharp_file_processing(self):
        """Test processing F# files."""
        fs_file = TEST_DIR / "test.fs"
        fs_file.write_text('let hello = printfn "Hello"')
        process_file(fs_file, TEST_DIR)
        content = fs_file.read_text()
        assert content.startswith("// File: test.fs"), "Header not added correctly for F#"


class TestNim:
    """Test Nim file support."""

    def test_nim_comment_style(self):
        """Test Nim comment style detection."""
        nim_file = TEST_DIR / "test.nim"
        nim_file.write_text('echo "Hello, World!"')
        comment_style = _get_comment_style(nim_file)
        assert comment_style == ("#", ""), "Incorrect comment style for Nim"

    def test_nim_file_processing(self):
        """Test processing Nim files."""
        nim_file = TEST_DIR / "test.nim"
        nim_file.write_text('echo "Hello, World!"')
        process_file(nim_file, TEST_DIR)
        content = nim_file.read_text()
        assert content.startswith("# File: test.nim"), "Header not added correctly for Nim"


class TestCrystal:
    """Test Crystal file support."""

    def test_crystal_comment_style(self):
        """Test Crystal comment style detection."""
        crystal_file = TEST_DIR / "test.cr"
        crystal_file.write_text('puts "Hello, World!"')
        comment_style = _get_comment_style(crystal_file)
        assert comment_style == ("#", ""), "Incorrect comment style for Crystal"

    def test_crystal_file_processing(self):
        """Test processing Crystal files."""
        crystal_file = TEST_DIR / "test.cr"
        crystal_file.write_text('puts "Hello, World!"')
        process_file(crystal_file, TEST_DIR)
        content = crystal_file.read_text()
        assert content.startswith("# File: test.cr"), "Header not added correctly for Crystal"


class TestTerraform:
    """Test Terraform file support."""

    def test_terraform_comment_style(self):
        """Test Terraform comment style detection."""
        tf_file = TEST_DIR / "test.tf"
        tf_file.write_text('resource "aws_instance" "example" {}')
        comment_style = _get_comment_style(tf_file)
        assert comment_style == ("#", ""), "Incorrect comment style for Terraform"

    def test_terraform_file_processing(self):
        """Test processing Terraform files."""
        tf_file = TEST_DIR / "test.tf"
        tf_file.write_text('resource "aws_instance" "example" {}')
        process_file(tf_file, TEST_DIR)
        content = tf_file.read_text()
        assert content.startswith("# File: test.tf"), "Header not added correctly for Terraform"


class TestOCaml:
    """Test OCaml file support."""

    def test_ocaml_comment_style(self):
        """Test OCaml comment style detection."""
        ml_file = TEST_DIR / "test.ml"
        ml_file.write_text('let hello = print_endline "Hello"')
        comment_style = _get_comment_style(ml_file)
        assert comment_style == ("(*", "*)"), "Incorrect comment style for OCaml"

    def test_ocaml_file_processing(self):
        """Test processing OCaml files."""
        ml_file = TEST_DIR / "test.ml"
        ml_file.write_text('let hello = print_endline "Hello"')
        process_file(ml_file, TEST_DIR)
        content = ml_file.read_text()
        assert content.startswith("(* File: test.ml *)"), "Header not added correctly for OCaml"


class TestVHDL:
    """Test VHDL file support."""

    def test_vhdl_comment_style(self):
        """Test VHDL comment style detection."""
        vhd_file = TEST_DIR / "test.vhd"
        vhd_file.write_text("entity test is end entity;")
        comment_style = _get_comment_style(vhd_file)
        assert comment_style == ("--", ""), "Incorrect comment style for VHDL"

    def test_vhdl_file_processing(self):
        """Test processing VHDL files."""
        vhd_file = TEST_DIR / "test.vhd"
        vhd_file.write_text("entity test is end entity;")
        process_file(vhd_file, TEST_DIR)
        content = vhd_file.read_text()
        assert content.startswith("-- File: test.vhd"), "Header not added correctly for VHDL"


class TestAda:
    """Test Ada file support."""

    def test_ada_comment_style(self):
        """Test Ada comment style detection."""
        adb_file = TEST_DIR / "test.adb"
        adb_file.write_text("procedure Test is begin null; end Test;")
        comment_style = _get_comment_style(adb_file)
        assert comment_style == ("--", ""), "Incorrect comment style for Ada"

    def test_ada_file_processing(self):
        """Test processing Ada files."""
        adb_file = TEST_DIR / "test.adb"
        adb_file.write_text("procedure Test is begin null; end Test;")
        process_file(adb_file, TEST_DIR)
        content = adb_file.read_text()
        assert content.startswith("-- File: test.adb"), "Header not added correctly for Ada"


class TestAssembly:
    """Test Assembly file support."""

    def test_assembly_comment_style(self):
        """Test Assembly comment style detection."""
        asm_file = TEST_DIR / "test.asm"
        asm_file.write_text("mov eax, 1")
        comment_style = _get_comment_style(asm_file)
        assert comment_style == (";", ""), "Incorrect comment style for Assembly"

    def test_assembly_file_processing(self):
        """Test processing Assembly files."""
        asm_file = TEST_DIR / "test.asm"
        asm_file.write_text("mov eax, 1")
        process_file(asm_file, TEST_DIR)
        content = asm_file.read_text()
        assert content.startswith("; File: test.asm"), "Header not added correctly for Assembly"


class TestVBNet:
    """Test VB.NET file support."""

    def test_vbnet_comment_style(self):
        """Test VB.NET comment style detection."""
        vb_file = TEST_DIR / "test.vb"
        vb_file.write_text("Module Test\nEnd Module")
        comment_style = _get_comment_style(vb_file)
        assert comment_style == ("'", ""), "Incorrect comment style for VB.NET"

    def test_vbnet_file_processing(self):
        """Test processing VB.NET files."""
        vb_file = TEST_DIR / "test.vb"
        vb_file.write_text("Module Test\nEnd Module")
        process_file(vb_file, TEST_DIR)
        content = vb_file.read_text()
        assert content.startswith("' File: test.vb"), "Header not added correctly for VB.NET"


class TestVLanguage:
    """Test V language support."""

    def test_v_comment_style(self):
        """Test V comment style detection."""
        v_file = TEST_DIR / "test.v"
        v_file.write_text("fn main() { println('Hello') }")
        comment_style = _get_comment_style(v_file)
        assert comment_style == ("//", ""), "Incorrect comment style for V"

    def test_v_file_processing(self):
        """Test processing V files."""
        v_file = TEST_DIR / "test.v"
        v_file.write_text("fn main() { println('Hello') }")
        process_file(v_file, TEST_DIR)
        content = v_file.read_text()
        assert content.startswith("// File: test.v"), "Header not added correctly for V"


class TestFortran:
    """Test Fortran file support."""

    def test_fortran_comment_style(self):
        """Test Fortran comment style detection."""
        f90_file = TEST_DIR / "test.f90"
        f90_file.write_text("program test\nend program")
        comment_style = _get_comment_style(f90_file)
        assert comment_style == ("!", ""), "Incorrect comment style for Fortran"

    def test_fortran_file_processing(self):
        """Test processing Fortran files."""
        f90_file = TEST_DIR / "test.f90"
        f90_file.write_text("program test\nend program")
        process_file(f90_file, TEST_DIR)
        content = f90_file.read_text()
        assert content.startswith("! File: test.f90"), "Header not added correctly for Fortran"


class TestCOBOL:
    """Test COBOL file support."""

    def test_cobol_comment_style(self):
        """Test COBOL comment style detection."""
        cob_file = TEST_DIR / "test.cob"
        cob_file.write_text("IDENTIFICATION DIVISION.\nPROGRAM-ID. TEST.")
        comment_style = _get_comment_style(cob_file)
        assert comment_style == ("*", ""), "Incorrect comment style for COBOL"

    def test_cobol_file_processing(self):
        """Test processing COBOL files."""
        cob_file = TEST_DIR / "test.cob"
        cob_file.write_text("IDENTIFICATION DIVISION.\nPROGRAM-ID. TEST.")
        process_file(cob_file, TEST_DIR)
        content = cob_file.read_text()
        assert content.startswith("* File: test.cob"), "Header not added correctly for COBOL"


class TestHCL:
    """Test HCL file support."""

    def test_hcl_comment_style(self):
        """Test HCL comment style detection."""
        hcl_file = TEST_DIR / "test.hcl"
        hcl_file.write_text('variable "example" {}')
        comment_style = _get_comment_style(hcl_file)
        assert comment_style == ("#", ""), "Incorrect comment style for HCL"

    def test_hcl_file_processing(self):
        """Test processing HCL files."""
        hcl_file = TEST_DIR / "test.hcl"
        hcl_file.write_text('variable "example" {}')
        process_file(hcl_file, TEST_DIR)
        content = hcl_file.read_text()
        assert content.startswith("# File: test.hcl"), "Header not added correctly for HCL"


class TestNix:
    """Test Nix file support."""

    def test_nix_comment_style(self):
        """Test Nix comment style detection."""
        nix_file = TEST_DIR / "test.nix"
        nix_file.write_text("{ pkgs }: pkgs.hello")
        comment_style = _get_comment_style(nix_file)
        assert comment_style == ("#", ""), "Incorrect comment style for Nix"

    def test_nix_file_processing(self):
        """Test processing Nix files."""
        nix_file = TEST_DIR / "test.nix"
        nix_file.write_text("{ pkgs }: pkgs.hello")
        process_file(nix_file, TEST_DIR)
        content = nix_file.read_text()
        assert content.startswith("# File: test.nix"), "Header not added correctly for Nix"


class TestPascal:
    """Test Pascal/Delphi file support."""

    def test_pascal_comment_style(self):
        """Test Pascal comment style detection."""
        pas_file = TEST_DIR / "test.pas"
        pas_file.write_text("program Test;\nbegin\nend.")
        comment_style = _get_comment_style(pas_file)
        assert comment_style == ("//", ""), "Incorrect comment style for Pascal"

    def test_pascal_file_processing(self):
        """Test processing Pascal files."""
        pas_file = TEST_DIR / "test.pas"
        pas_file.write_text("program Test;\nbegin\nend.")
        process_file(pas_file, TEST_DIR)
        content = pas_file.read_text()
        assert content.startswith("// File: test.pas"), "Header not added correctly for Pascal"

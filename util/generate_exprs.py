# Dingus program

from os import path
import os
import sys


def wl(file, line, indent=0):
    file.write(f"{' ' * indent * 4}{line}\n")


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_exprs.py [output_dir] [grammar]")
        exit(1)

    print("Generating ast...")

    with open(sys.argv[2]) as infile:
        with open(path.join(sys.argv[1], "expr.py"), 'w') as outfile:
            wl(outfile, "from dataclasses import dataclass")
            wl(outfile, "from scanner.token import Token")

            wl(outfile, "class Expr:")
            wl(outfile, "def accept(self, visitor):", 1)
            wl(outfile, "pass", 2)

            for line in infile.readlines():
                if line.strip().startswith("#"):
                    continue

                if line.strip().startswith(">"):
                    wl(outfile, line.lstrip(">"))
                    continue
                
                prod, fields = [l.strip() for l in line.split("|")]

                wl(outfile, "@dataclass")
                wl(outfile, f"class {prod}(Expr):")

                for field in fields.split("  "):
                    wl(outfile, f"{field}", 1)

                wl(outfile, "def accept(self, visitor):", 1)
                wl(outfile,
                   f"return visitor.visit_{prod.lower()}_expr(self)", 2)

            infile.seek(0)

            wl(outfile, "class Visitor:")
            for line in infile.readlines():
                if line.strip().startswith("#"):
                    continue
                
                if line.strip().startswith(">"):
                    continue

                prod, fields = [l.strip() for l in line.split("|")]

                wl(outfile,
                   f"def visit_{prod.lower()}_expr(self, expr: {prod}):", 1)
                wl(outfile, "pass", 2)

    print("Formatting with autopep8...")
    os.system(f"autopep8 {path.join(sys.argv[1], 'expr.py')} -i")

    print("Done!")


if __name__ == "__main__":
    main()
